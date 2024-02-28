# 調整匯入路徑以符合專案結構
from config.DatabaseConfig import Neo4jConfig, RedisConfig, PostgreSQLConfig
from services.RegisterService import RegisterService
from services.LoginService import LoginService
from services.LogoutService import LogoutService
from services.VoteCountsService import VoteCountsService
from services.EmailService import EmailService
from data_access.DatabaseDA import Neo4jUserOperation, RedisSessionOperation, PostgresqlUserOperation
import os
from dotenv import load_dotenv
load_dotenv()

# 環境變數
sender_email = os.getenv("GMAIL_USER")
sender_password = os.getenv("GMAIL_PASSWORD")

# 配置實例化
neo4j_config = Neo4jConfig(uri="bolt://localhost:7687", user="neo4j", password="brainconnect")
redis_config = RedisConfig(host="localhost", port=6379, password="brainconnect", db=0, decode_responses=True)
postgresql_config = PostgreSQLConfig(dbname="brain", user="postgres", password="learnsome")

# 資料存取操作實例化
neo4j_user_op = Neo4jUserOperation(neo4j_config)
redis_session_op = RedisSessionOperation(redis_config)
postgresql_user_op = PostgresqlUserOperation(postgresql_config)

# 服務實例化，確保傳遞正確的依賴項
email_service = EmailService(neo4j_user_op, redis_session_op, sender_email, sender_password)
register_service = RegisterService(neo4j_user_op, redis_session_op)
vote_counts_service = VoteCountsService(redis_session_op)
login_service = LoginService(neo4j_user_op)
logout_service = LogoutService(neo4j_user_op)