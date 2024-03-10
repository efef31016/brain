from db.Operations import UserOperation
import uuid
import aioredis

class RedisSessionOperation(UserOperation):
    def __init__(self, redis_pool: aioredis.Redis):
        self.redis_pool = redis_pool

    async def save_user(self, user):
        session_token = str(uuid.uuid4())
        await self.redis_pool.setex(f"user_session:{user.name}", 3600, session_token)
        return session_token

    async def find_user(self, identifier: str):
        session_token = await self.redis_pool.get(f"user_session:{identifier}")
        return session_token
    
    async def set_with_expiration(self, key: str, value: str, expiration: int):
        await self.redis_pool.setex(key, expiration, value)

    async def get(self, key: str) -> str:
        return await self.redis_pool.get(key)

    async def delete(self, key: str):
        await self.redis_pool.delete(key)
