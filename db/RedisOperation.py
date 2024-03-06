from db.operations import UserOperation
from config.db_config_manager import DBConfigManager
import uuid

class RedisSessionOperation(UserOperation):
    def __init__(self):
        self.config = DBConfigManager.load_redis_config()

    async def save_user(self, user):
        # 在这里，我们将使用 Redis 来保存用户会话，而不是用户信息
        session_token = str(uuid.uuid4())
        self.config.r.setex(f"user_session:{user.name}", 3600, session_token)
        return session_token

    async def find_user(self, identifier: str):
        # 在这个场景中，查找用户可能意味着查找用户的会话信息
        session_token = self.config.r.get(f"user_session:{identifier}")
        return session_token