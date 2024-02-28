from argon2 import PasswordHasher
import jwt
import datetime
from contextlib import closing


ph = PasswordHasher(
    time_cost=4,  # 執行時間
    memory_cost=1024 * 20,  # 內存量(Kib)
    parallelism=2,  # 並行度
    hash_len=32,  # hash 長度
    salt_len=16  # salt 長度
)

class AuthService:
    def __init__(self, postgresql_user_op):
        self.postgresql_user_op = postgresql_user_op

    @staticmethod
    def verify_password(plain_password, hashed_password):
        try:
            ph.verify(hashed_password, plain_password)
            return True
        except:
            return False

    @staticmethod
    def generate_token(user, aud="login_service"):

        payload = {
            "sub": user["user_id"],
            "iat": datetime.datetime.utcnow(), # Issued At
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
            # "aud": aud,
            # "name": user["user_name"],
            # "first_login": False
        }

        secret = "FakeIssue"

        token = jwt.encode(payload, secret, algorithm='HS256')
        
        return token
    
    def add_token_to_blacklist(self, user_id: str, token: str, device_id: str):
        '''
        將使用者的JWT令牌和裝置ID新增至黑名單。
        '''
        query = """
            INSERT INTO \"user\".token_blacklist (user_id, token, device_id)
            VALUES (%s, %s, %s)
        """
        # 注意傳遞user_id和device_id作為參數
        return self.postgresql_user_op.db_config.insert(query, (user_id, token, device_id))

    def is_token_blacklisted(self, token: str) -> bool:
        '''
        檢查JWT令牌是否在黑名單中。
        '''
        query = """
            SELECT 1 FROM "user".token_blacklist
            WHERE token = %s
        """
        result = self.postgresql_user_op.db_config.select(query, (token,))
        return len(result) > 0
    
    def remove_from_blacklist(self, user_id, device_id):
        # 這裡的SQL查詢需要根據您的資料庫結構進行調整
        query = """
        DELETE FROM \"user\".token_blacklist
        WHERE user_id = %s AND device_id = %s;
        """
        parameters = (user_id, device_id)
        with closing(self.postgresql_user_op.db_config.get_connection()) as conn, conn.cursor() as cur:
            cur.execute(query, parameters)
            conn.commit()


if __name__ == "__main__":
    secret = "FakeIssue"
    user = {"user_id": "123", "user_name": "chienyao"}
    a = AuthService.generate_token(user)
    print(a)
    import jwt
    payload = jwt.decode(a, secret, algorithms=['HS256'], audience="debate_service")
    print(payload.get("sub"))