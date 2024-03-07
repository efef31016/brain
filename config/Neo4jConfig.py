from neo4j import GraphDatabase, exceptions

class Neo4jConfig:
    _instance = None

    def __new__(cls, uri, user, password):
        if cls._instance is None:
            try:
                cls._instance = super(Neo4jConfig, cls).__new__(cls)
                cls._instance.driver = GraphDatabase.driver(uri, auth=(user, password))
            except exceptions.Neo4jError as e:
                raise ConnectionError(f"Failed to connect to Neo4j database: {e}")
        return cls._instance

    @classmethod
    def get_driver(cls):
        return cls._instance.driver

    @classmethod
    def close(cls):
        cls._instance.driver.close()
