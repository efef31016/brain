from services.AuthService import AuthService
from typing import Dict

class LoginService:
    def __init__(self, neo4j_user_op):
        self.neo4j_user_op = neo4j_user_op

    def login(self, login_identifier, password) -> Dict[str, str]:
        try:
            user = self.neo4j_user_op.find_user(login_identifier)[0]["u"]
            if user and AuthService.verify_password(password, user["password"]):
                return {
                    "status": "success",
                    "message": "登入成功 (與前端分離，前端顯示前端定義的)",
                    "token": AuthService.generate_token(user)
                    }
            else:
                return {
                        "status": "error",
                        "message": "登入失敗，請檢查您的使用者名稱或密碼。"
                        }
        except Exception as e:
            return {"message": e}