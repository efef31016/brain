from abc import ABC, abstractmethod
import secrets
import aioredis
from Config import redis_config, postgresql_user_op, neo4j_user_op

class BaseVerificationService(ABC):
    def __init__(self):
        redis_url = redis_config.get_url()
        self.redis = aioredis.from_url(redis_url, decode_responses=True)
        self.postgresql_op = postgresql_user_op
        self.neo4j_op = neo4j_user_op

    async def generate_verification_code(self, identifier: str, namespace: str) -> str:
        verification_code = ''.join([str(secrets.randbelow(10)) for _ in range(6)])
        key = f"{namespace}:{identifier}"
        await self.redis.setex(key, 600, verification_code)  # 10 分鐘過期
        return verification_code

    @abstractmethod
    async def send_verification(self, identifier: str, code: str):
        pass

    async def verify_code(self, identifier: str, code: str, namespace: str) -> bool:
        key = f"{namespace}:{identifier}"
        stored_code = await self.redis.get(key)
        if stored_code == code:
            await self.redis.delete(key)
            return True
        return False