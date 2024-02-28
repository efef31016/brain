from services.AuthService import AuthService
from typing import Dict

class LoginService:
    def __init__(self, postgresql_user_op):
        self.postgresql_user_op = postgresql_user_op
        self.auth = AuthService(postgresql_user_op)

    def login(self, login_identifier: str, password: str, device_id: str) -> Dict[str, str]:
        try:
            user = self.postgresql_user_op.find_user(login_identifier)
            if user and AuthService.verify_password(password, user["password"]):
                self.auth.remove_from_blacklist(user["user_id"], device_id)
                return {
                    "status": "success",
                    "message": "登入成功 (與前端分離，前端顯示前端定義的)",
                    "access_token": AuthService.generate_token(user),
                    "token_type": "bearer"
                    }
            else:
                return {
                        "status": "error",
                        "message": "登入失敗，請檢查您的使用者名稱或密碼。"
                        }
        except Exception as e:
            return {"message": f'/api/login error:{e}'}