import psycopg2

class PostgreSQLConfig:
    def __init__(self, dbname, user, password, host):
        self.connection_string = f"dbname='{dbname}' user='{user}' password='{password}' host='{host}'"

    def get_connection(self):
        try:
            return psycopg2.connect(self.connection_string)
        except psycopg2.DatabaseError as error:
            print(f"Database connection error: {error}")
            raise error
