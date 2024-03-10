class Neo4jUser:
    def __init__(self, uuid, get_invited, throw_invited):
        self.uuid = uuid
        self.get_invited = get_invited
        self.throw_invited = throw_invited


class PostgresqlUser:
    def __init__(self, uuid, name, email, password):
        self.uuid = uuid
        self.name = name
        self.email = email
        self.password = password