import os
import redis
import psycopg2
from neo4j import GraphDatabase

class DBConfigManager:
    @staticmethod
    def load_redis_config():
        return RedisConfig(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            password=os.getenv('REDIS_PASSWORD', ''),
            db=int(os.getenv('REDIS_DB', 0))
        )

    @staticmethod
    def load_neo4j_config():
        return Neo4jConfig(
            uri=os.getenv('NEO4J_URI', 'bolt://localhost:7687'),
            user=os.getenv('NEO4J_USER', 'neo4j'),
            password=os.getenv('NEO4J_PASSWORD', 'password')
        )

    @staticmethod
    def load_postgresql_config():
        return PostgreSQLConfig(
            dbname=os.getenv('POSTGRESQL_DBNAME', 'dbname'),
            user=os.getenv('POSTGRESQL_USER', 'user'),
            password=os.getenv('POSTGRESQL_PASSWORD', 'password'),
            host=os.getenv('POSTGRESQL_HOST', 'localhost')
        )