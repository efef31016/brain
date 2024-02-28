class LogoutService:
    def __init__(self, neo4j_user_op):
        self.neo4j_user_op = neo4j_user_op

    def add_token_to_user_blacklist(self, user_id, token):

        check_token_query = """
        MATCH (u:User {uuid: $user_id})
        RETURN u.blacklistedToken = $token AS isBlacklisted
        """
        result = self.neo4j_user_op.neo4j_config.run_query(check_token_query, parameters={"user_id": user_id, "token": token})
        return result[0]["isBlacklisted"] if result else False