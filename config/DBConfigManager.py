import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from dotenv import load_dotenv
from RedisConfig import RedisConfig
from Neo4jConfig import Neo4jConfig
from PostgresqlConfig import PostgresqlConfig

load_dotenv()

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
        return PostgresqlConfig(
            uri=os.getenv('POSTGRESQL_URI', '')
        )
    

if __name__ == "__main__":
    redis_config = DBConfigManager.load_redis_config()
    redis_connection = redis_config.get_connection()

    neo4j_config = DBConfigManager.load_neo4j_config()
    neo4j_driver = neo4j_config.get_driver()

    neo4j_config.close()

    postgresql_config = DBConfigManager.load_postgresql_config()
    postgresql_connection = postgresql_config.get_session()

    postgresql_connection.close()