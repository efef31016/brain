import os
from dotenv import load_dotenv

load_dotenv()

class ConfigManager:
    NEO4J_URI = os.getenv("NEO4J_URI", "check .env")
    NEO4J_USER = os.getenv("NEO4J_USER", "check .env")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "check .env")

    REDIS_HOST = os.getenv("REDIS_HOST", "check .env")
    REDIS_PORT = int(os.getenv("REDIS_PORT", "check .env"))
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "check .env")
    REDIS_DB = int(os.getenv("REDIS_DB", "check .env"))

    POSTGRESQL_URI = os.getenv("POSTGRESQL_URI", "check .env")

    SENDER_EMAIL = os.getenv("SENDER_EMAIL", "check .env")
    SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "check .env")
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 465))
