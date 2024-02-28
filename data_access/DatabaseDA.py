from abc import ABC, abstractmethod
from models.UserModel import User
from config.DatabaseConfig import Neo4jConfig, RedisConfig, PostgreSQLConfig
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

    def find_user(self, login_identifier):
        """
        尋找用戶，login_identifier 可以是用戶名或電子郵件。
        """
        query = """
        MATCH (u:User)
        WHERE u.username = $login_identifier OR u.email = $login_identifier
        RETURN u
        """
        parameters = {"login_identifier": login_identifier}
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
    
class PostgresqlUserOperation:
    def __init__(self, db_config: PostgreSQLConfig):
        self.db_config = db_config

    def save_user(self, username, email, password, person_uuid):
        conn = self.db_config.get_connection()
        cursor = conn.cursor()

        # 插入使用者資訊
        cursor.execute("""
            INSERT INTO users (uuid, username, email, password)
            VALUES (%s, %s, %s, %s, %s)
        """, (person_uuid, username, email, password))

        conn.commit()
        cursor.close()
        conn.close()

    def find_user(self, login_identifier):
        conn = self.db_config.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM users
            WHERE username = %s OR email = %s
        """, (login_identifier, login_identifier))

        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user