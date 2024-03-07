from db.Operations import UserOperation
from config.DBConfigManager import DBConfigManager
import uuid

class RedisSessionOperation(UserOperation):
    def __init__(self):
        self.config = DBConfigManager.load_redis_config()

    async def save_user(self, user):
        session_token = str(uuid.uuid4())
        self.config.r.setex(f"user_session:{user.name}", 3600, session_token)
        return session_token

    async def find_user(self, identifier: str):
        session_token = self.config.r.get(f"user_session:{identifier}")
        return session_token