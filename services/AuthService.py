from argon2 import PasswordHasher
import jwt
import datetime
import random

def sub_secret(user):

    insert_str = user["uuid"]
    uuid = list(insert_str)
    for char in "user":
        pos = random.randint(0, len(uuid))
        uuid.insert(pos, char)

    uuid = ''.join(uuid)

    return uuid

def secret_secret(str1, str2):

    secret_0 = str1*50
    selected_chars_0 = random.sample(secret_0, 128)
    secret_1 = str2*50
    selected_chars_1 = random.sample(secret_1, 128)

    secret = ''.join(selected_chars_0)
    secret += ''.join(selected_chars_1)

    return secret

ph = PasswordHasher(
    time_cost=4,  # 執行時間
    memory_cost=1024 * 20,  # 內存量(Kib)
    parallelism=2,  # 並行度
    hash_len=32,  # hash 長度
    salt_len=16  # salt 長度
)

class AuthService:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return ph.hash(plain_password) == hashed_password
    
    @staticmethod
    def generate_token(user):
        '''
        為加強安全性做一些修改
        '''

        uuid = sub_secret(user)

        aud = "debate_service"

        payload = {
            'sub': uuid,
            'iat': datetime.datetime.utcnow(), # Issued At
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'aud': aud,
            'name': user["username"],
            'first_login': False
        }

        secret = secret_secret("FakeIssue", "IsNotFake")

        return jwt.encode(payload, secret, algorithm='HS256')