from db.Operations import UserOperation
from config.DBConfigManager import DBConfigManager
from models.UserModel import User

class Neo4jUserOperation(UserOperation):
    def __init__(self):
        self.config = DBConfigManager.load_neo4j_config()

    async def save_user(self, user: User):
        query = """
        CREATE (u:User {uuid: $uuid, name: $name, email: $email})
        RETURN u
        """
        parameters = {"uuid": user.uuid, "name": user.name, "email": user.email}
        with self.config.driver.session() as session:
            result = session.write_transaction(lambda tx: tx.run(query, parameters))
            return [record for record in result]

    async def find_user(self, identifier: str):
        query = """
        MATCH (u:User)
        WHERE u.uuid = $identifier OR u.email = $identifier
        RETURN u
        """
        parameters = {"identifier": identifier}
        with self.config.driver.session() as session:
            result = session.read_transaction(lambda tx: tx.run(query, parameters))
            return [record for record in result]