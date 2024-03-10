import asyncpg
from config.DBConfigManager import DBConfigManager
from db.Operations import UserOperation
from models.UserModel import PostgresqlUser

class PostgresqlUserOperation(UserOperation):
    def __init__(self):
        self.config = DBConfigManager.load_postgresql_config()

    async def save_user(self, user: PostgresqlUser):
        query = """
        INSERT INTO users (uuid, name, email, password)
        VALUES ($1, $2, $3, $4)
        """
        async with asyncpg.create_pool(self.config.uri) as pool:
            async with pool.acquire() as connection:
                await connection.execute(query, user.uuid, user.name, user.email, user.password)

    async def find_user(self, identifier: str, user: PostgresqlUser):
        query = """
        SELECT * FROM users
        WHERE name = $1 OR email = $1
        """
        async with asyncpg.create_pool(self.config.uri) as pool:
            async with pool.acquire() as connection:
                result = await connection.fetchrow(query, identifier)
                if result:
                    return user(uuid=result['uuid'], name=result['name'], email=result['email'], password=result['password'])
                return None
