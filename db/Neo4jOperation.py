from config.DBConfigManager import DBConfigManager
from db.Operations import UserOperation
from models.UserModel import Neo4jUser
import logging
from neo4j.exceptions import Neo4jError

logger = logging.getLogger(__name__)

class Neo4jUserOperation(UserOperation):
    def __init__(self):
        self.driver = DBConfigManager.load_neo4j_config()

    async def save_user(self, user: Neo4jUser):
        query = """
        CREATE (u:User {uuid: $uuid, get_invited: $get_invited, throw_invited: $throw_invited})
        RETURN u
        """
        try:
            return await self._run_query(query, **user.dict())
        except Neo4jError as e:
            logger.error("Failed to save user in Neo4j: %s", e, exc_info=True)
            raise

    async def find_user(self, identifier: str):
        query = """
        MATCH (u:User)
        WHERE u.uuid = $identifier
        RETURN u
        """
        try:
            return await self._run_query(query, identifier=identifier)
        except Neo4jError as e:
            logger.error("Failed to find user in Neo4j: %s", e, exc_info=True)
            raise

    async def _run_query(self, query, **parameters):
        async with self.driver.session() as session:
            result = await session.run(query, **parameters)
            return [record async for record in result]
