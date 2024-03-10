from abc import ABC, abstractmethod
import secrets
from db.RedisOperation import RedisSessionOperation

class BaseVerificationService(ABC):
    def __init__(self, redis_op: RedisSessionOperation, postgresql_op, neo4j_op):
        self.redis_op = redis_op
        self.postgresql_op = postgresql_op
        self.neo4j_op = neo4j_op

    async def generate_verification_code(self, identifier: str, namespace: str) -> str:
        verification_code = ''.join([str(secrets.randbelow(10)) for _ in range(6)])
        key = f"{namespace}:{identifier}"
        await self.redis_op.set_with_expiration(key, verification_code, 600)  # 10 minutes expiration
        return verification_code

    @abstractmethod
    async def send_verification(self, identifier: str, code: str):
        pass

    async def verify_code(self, identifier: str, code: str, namespace: str) -> bool:
        key = f"{namespace}:{identifier}"
        stored_code = await self.redis_op.get(key)
        if stored_code == code:
            await self.redis_op.delete(key)
            return True
        return False