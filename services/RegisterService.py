import re
import uuid
from services.AuthService import ph
from fastapi import HTTPException

class RegisterService:
    username_pattern = r'^[a-zA-Z0-9_\u4e00-\u9fff]{1,20}$'
    password_min_length = 8

    def __init__(self, neo4j_user_op, postgresql_user_op, redis_session_op):
        self.neo4j_user_op = neo4j_user_op
        self.postgresql_user_op = postgresql_user_op
        self.redis_session_op = redis_session_op

    async def generate_initial_invite_code(self):
        invite_code = str(uuid.uuid4())[:8].upper()
        await self.redis_session_op.redis_config.set_value("verification_usage:" + invite_code, 0, expire=86400)
        await self.redis_session_op.redis_config.set_value("initial_invite_code", invite_code)
        print(f"Initial invite code: {invite_code}")

    async def register(self, username, password, email, verification_code):
        await self._validate_username(username)
        self._validate_password(password)  # 同步運行，因為它不涉及IO操作
        await self._validate_email(email)
        await self._validate_verification_code(verification_code)

        hashed_password = ph.hash(password)
        person_uuid, new_verification_code = self._generate_uuid_and_verification_code()

        try:
            await self._save_user_info(username, email, hashed_password, person_uuid, new_verification_code, verification_code)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f'User data saving failed: {e}')

        return {"new_verification_code": new_verification_code}

    async def _validate_username(self, username):
        if not re.match(self.username_pattern, username):
            raise HTTPException(status_code=400, detail="Username must be 1-20 characters long, including letters, numbers, underscores, and Chinese characters.")

    async def _validate_email(self, email):
        if not await self.redis_session_op.redis_config.find_a_set(email):
            raise HTTPException(status_code=400, detail="Please verify your email.")

        if await self.postgresql_user_op.user_exists(email):
            raise HTTPException(status_code=400, detail="This email is already registered.")

    async def _validate_verification_code(self, verification_code):
        usage_count = await self.redis_session_op.redis_config.get_value("verification_usage:" + verification_code)
        if usage_count is None or int(usage_count) >= 5:
            raise HTTPException(status_code=400, detail="Verification code is invalid or has been used too many times.")

        await self.redis_session_op.redis_config.increment_value("verification_usage:" + verification_code)

    async def _save_user_info(self, username, email, hashed_password, person_uuid, new_verification_code, verification_code):
        await self.postgresql_user_op.save_user(username, email, hashed_password, person_uuid)
        await self.neo4j_user_op.save_user(person_uuid, new_verification_code, verification_code)
        await self.redis_session_op.redis_config.set_value("verification_usage:" + verification_code, 1)
