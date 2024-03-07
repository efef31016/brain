# 調整匯入路徑以符合專案結構
from config.Neo4jConfig import Neo4jConfig
from config.RedisConfig import RedisConfig
from config.PostgresqlConfig import PostgresqlConfig
from services.RegisterService import RegisterService
from services.LoginService import LoginService
from services.LogoutService import LogoutService
from services.VoteCountsService import VoteCountsService
from services.EmailService import EmailService
from services.MyAccountService import MyAccountService
from services.ResetPasswordService import ResetPasswordService
from db.Neo4jOperation import Neo4jUserOperation
from db.RedisOperation import RedisSessionOperation
from db.PostgresqlOperation import PostgresqlUserOperation

import os
from dotenv import load_dotenv
load_dotenv()

# 環境變數
# Environment variables for database credentials
NEO4J_URI = os.getenv("NEO4J_URI", "check .env")
NEO4J_USER = os.getenv("NEO4J_USER", "check .env")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "check .env")

REDIS_HOST = os.getenv("REDIS_HOST", "check .env")
REDIS_PORT = int(os.getenv("REDIS_PORT", "check .env"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "check .env")
REDIS_DB = int(os.getenv("REDIS_DB", "check .env"))

POSTGRESQL_URI = os.getenv("POSTGRESQL_URI", "check .env")

# Email configuration
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "check .env")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "check .env")
SMTP_SERVER=os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT=int(os.getenv('SMTP_PORT', 465))

# 配置實例化
neo4j_config = Neo4jConfig(uri=NEO4J_URI, user=NEO4J_USER, password=NEO4J_PASSWORD)
redis_config = RedisConfig(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB, decode_responses=True)
postgresql_config = PostgresqlConfig(uri=POSTGRESQL_URI)

# 資料存取操作實例
neo4j_user_op = Neo4jUserOperation()
redis_session_op = RedisSessionOperation()
postgresql_user_op = PostgresqlUserOperation()

# 服務實例化，確保傳遞正確的依賴項