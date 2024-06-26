from abc import ABC, abstractmethod
from models.User import User
from config.DatabaseConfig import Neo4jConfig, RedisConfig
import uuid

class DatabaseOperation(ABC):
    @abstractmethod
    def save_user(self, user: User):
        pass

    @abstractmethod
    def find_user(self, username):
        pass

class Neo4jUserOperation(DatabaseOperation):
    def __init__(self, neo4j_config: Neo4jConfig):
        self.neo4j_config = neo4j_config

    def save_user(self, username, email, password, person_uuid, token, verify):
        # 建立用戶節點
        create_user_query = """
        CREATE (u:User {uuid: $uuid, username: $username, email: $email, password: $password, token: $token})
        RETURN u
        """
        self.neo4j_config.run_query(create_user_query, parameters={
            "uuid": person_uuid, "username": username, "email": email, 
            "password": password, "token": token})

        # 建立連結
        create_relation_query = """
        MATCH (inviter:User {token: $verify}), (invitee:User {uuid: $uuid})
        CREATE (inviter)-[:INVITED]->(invitee)
        """
        self.neo4j_config.run_query(create_relation_query, parameters={"verify": verify, "uuid": person_uuid})

    def find_user(self, username):
        query = "MATCH (u:User {username: $username}) RETURN u"
        parameters = {"username": username}
        result = self.neo4j_config.run_query(query, parameters)
        return result

class RedisSessionOperation:
    def __init__(self, redis_config: RedisConfig):
        self.redis_config = redis_config

    def create_session(self, username):
        session_token = self._generate_session_token()
        self.redis_config.set_value_with_expiration(session_token, username, 3600)  # 例: 一小時過期
        return session_token

    def get_session(self, session_token):
        return self.redis_config.get_value(session_token)
    
    def _generate_session_token(self):
        return str(uuid.uuid4())