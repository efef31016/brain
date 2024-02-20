# https://developer.redis.com/create/windows/
from neo4j import GraphDatabase
import redis

class Neo4jConfig:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))  # neo4j_driver

    def close(self):
        self.driver.close()

    def run_query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record for record in result]
        
class RedisConfig:
    def __init__(self, host, port, password, db, decode_responses=True):
        self.r = redis.Redis(host=host, port=port, password=password, db=db, decode_responses=decode_responses)

    def set_value(self, key, value):
        self.r.set(key, value)

    def get_value(self, key):
        return self.r.get(key)
    
    def set_value_with_expiration(self, key, value, time_in_seconds):
        self.r.setex(key, time_in_seconds, value)

    def set_a_set(self, key, value):
        self.r.sadd(key, value)

    def find_a_set(self, value):
        return self.r.sismember("verified_emails", value)



if __name__ == "__main__":
    from datetime import timedelta

    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "brainconnect"
    neo4j_config = Neo4jConfig(uri, user, password)
    query_result = neo4j_config.run_query("MATCH (n) RETURN n")
    neo4j_config.close()

    host = "localhost"
    port = "6379"
    password = "brainconnect"
    redis_config = RedisConfig(host, port, password, 0)
    # redis_config.set_value("key", "value")
    # print(redis_config.get_value("key"))

    # expiration_duration = timedelta(minutes=30)
    # redis_config.set_value_with_expiration("token123", "user@example.com", expiration_duration)
