# https://developer.redis.com/create/windows/
import redis

class RedisConfig:
    def __init__(self, host, port, password, db, decode_responses=True):
        self.host = host
        self.port = port
        self.password = password
        self.db = db

        try:
            self.pool = redis.ConnectionPool(host=host, port=port, password=password, db=db, decode_responses=decode_responses)
            self.redis = redis.Redis(connection_pool=self.pool)
        except redis.RedisError as e:
            raise ConnectionError(f"Failed to connect to Redis: {e}")

    def get_connection(self):
        return self.redis
    
    def get_url(self):
        return f"redis://:{self.password}@{self.host}:{self.port}/{self.db}"
