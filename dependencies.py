# dependencies.py
from fastapi import Depends
from config.RedisConfig import get_redis_pool

from config_manager import ConfigManager
from db.Neo4jOperation import Neo4jUserOperation
from db.RedisOperation import RedisSessionOperation
from db.PostgresqlOperation import PostgresqlUserOperation
from services.RegisterService import RegisterService
from services.EmailVerificationService import EmailVerificationService
from services.EmailService import EmailService

def get_neo4j_user_op():
    return Neo4jUserOperation()

def get_redis_session_op(redis_pool=Depends(get_redis_pool)):
    return RedisSessionOperation(redis_pool)

def get_postgresql_user_op():
    return PostgresqlUserOperation()

def get_email_service():
    return EmailService(ConfigManager.SENDER_EMAIL, ConfigManager.SENDER_PASSWORD, ConfigManager.SMTP_SERVER, ConfigManager.SMTP_PORT)

def get_email_verification_service():
    neo4j_op = get_neo4j_user_op()
    redis_op = get_redis_session_op()
    pg_op = get_postgresql_user_op()
    return EmailVerificationService(redis_op, pg_op, neo4j_op)

def get_register_service():
    neo4j_op = get_neo4j_user_op()
    redis_op = get_redis_session_op()
    pg_op = get_postgresql_user_op()
    return RegisterService(neo4j_op, pg_op, redis_op)
