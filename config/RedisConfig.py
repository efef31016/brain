# https://developer.redis.com/create/windows/
import aioredis
from fastapi import Depends, BackgroundTasks
import os

class RedisConfig:
    def __init__(self, host: str, port: int, password: str, db: int, decode_responses: bool = True):
        self.redis_url = f"redis://{host}:{port}"
        self.password = password
        self.db = db
        self.decode_responses = decode_responses

    async def create_redis_pool(self):
        return await aioredis.create_redis_pool(
            self.redis_url,
            password=self.password,
            db=self.db,
            decode_responses=self.decode_responses
        )

def load_redis_config():
    return RedisConfig(
        host=os.getenv('REDIS_HOST', 'localhost'),
        port=int(os.getenv('REDIS_PORT', 6379)),
        password=os.getenv('REDIS_PASSWORD', ''),
        db=int(os.getenv('REDIS_DB', 0))
    )

async def get_redis_pool(background_tasks: BackgroundTasks, redis_config: RedisConfig = Depends(load_redis_config)) -> aioredis.Redis:
    pool = await redis_config.create_redis_pool()
    background_tasks.add_task(pool.close)
    return pool