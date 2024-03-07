from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker

class PostgresqlConfig:
    def __init__(self, uri):
        try:
            self.engine = create_engine(uri, pool_pre_ping=True)
            self.session_factory = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            self.Session = scoped_session(self.session_factory)
        except exc.SQLAlchemyError as e:
            raise ConnectionError(f"Failed to connect to PostgreSQL database: {e}")

    def get_session(self):
        return self.Session()

    def close(self):
        self.Session.remove()
        self.engine.dispose()
