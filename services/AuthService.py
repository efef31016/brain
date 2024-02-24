import bcrypt
import jwt

class AuthService:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    @staticmethod
    def generate_token(user):
        # JWT token
        return jwt.encode({'username': user['username']}, 'secret', algorithm='HS256')