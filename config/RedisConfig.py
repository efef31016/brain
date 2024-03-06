# https://developer.redis.com/create/windows/
import redis

class RedisConfig:
    def __init__(self, host, port, password, db, decode_responses=True):
        self.redis_connection = redis.Redis(host=host, port=port, password=password, db=db, decode_responses=decode_responses)

    def get_connection(self):
        return self.redis_connection