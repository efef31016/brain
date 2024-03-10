from neo4j import GraphDatabase, exceptions

class Neo4jConfig:
    _instance = None

    def __new__(cls, uri=None, user=None, password=None):
        if cls._instance is None and uri and user and password:
            try:
                cls._instance = super().__new__(cls)  # 使用super().__new__(cls)而不是super(Neo4jConfig, cls).__new__(cls)
                cls._instance.driver = GraphDatabase.driver(uri, auth=(user, password))
            except exceptions.Neo4jError as e:
                raise ConnectionError(f"Failed to connect to Neo4j database: {e}")
        return cls._instance

    @classmethod
    def initialize(cls, uri, user, password):
        if cls._instance is None:
            cls(uri, user, password)

    @classmethod
    def get_driver(cls):
        if cls._instance is None:
            raise Exception("Neo4jConfig has not been initialized. Call Neo4jConfig.initialize(uri, user, password) first.")
        return cls._instance.driver

    @classmethod
    def close(cls):
        if cls._instance and cls._instance.driver:
            cls._instance.driver.close()
            cls._instance = None  # Reset _instance to allow re-initialization if needed
