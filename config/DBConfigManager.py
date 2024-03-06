import os
from config import RedisConfig, Neo4jConfig, PostgresqlConfig

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
            dbname=os.getenv('POSTGRESQL_DBNAME', 'dbname'),
            user=os.getenv('POSTGRESQL_USER', 'user'),
            password=os.getenv('POSTGRESQL_PASSWORD', 'password'),
            host=os.getenv('POSTGRESQL_HOST', 'localhost')
        )
    

if __name__ == "__main__":
    redis_config = DBConfigManager.load_redis_config()
    redis_connection = redis_config.get_connection()

    # 加载Neo4j配置并获取驱动
    neo4j_config = DBConfigManager.load_neo4j_config()
    neo4j_driver = neo4j_config.get_driver()

    # 使用完后关闭Neo4j连接
    neo4j_config.close()

    # 加载PostgreSQL配置并获取连接
    postgresql_config = DBConfigManager.load_postgresql_config()
    postgresql_connection = postgresql_config.get_connection()

    # 使用完后确保关闭PostgreSQL连接
    postgresql_connection.close()