from db.Operations import UserOperation
from config.DBConfigManager import DBConfigManager
from contextlib import closing
from models.UserModel import User

class PostgresqlUserOperation(UserOperation):
    def __init__(self):
        self.config = DBConfigManager.load_postgresql_config()

    async def save_user(self, user: User):
        query = """
        INSERT INTO users (uuid, name, email, password)
        VALUES (%s, %s, %s, %s)
        """
        parameters = (user.uuid, user.name, user.email, user.password)
        with closing(self.config.get_connection()) as conn, conn.cursor() as cur:
            cur.execute(query, parameters)
            conn.commit()

    async def find_user(self, identifier: str):
        query = """
        SELECT * FROM users
        WHERE name = %s OR email = %s
        """
        with closing(self.config.get_connection()) as conn, conn.cursor() as cur:
            cur.execute(query, (identifier, identifier))
            result = cur.fetchone()
            if result:
                return User(uuid=result[0], name=result[1], email=result[2], password=result[3])
            return None