from services.AuthService import AuthService
from typing import Dict

class LogoutService:
    def __init__(self, postgresql_user_op):
        self.auth = AuthService(postgresql_user_op)

    def logout(self, user_id: str, token: str, device_id: str) -> Dict[str, str]:
        try:
            self.auth.add_token_to_blacklist(user_id, token, device_id)
            return {
                "status": "success",
                "message": "您已成功登出。"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"登出失敗：{e}"
            }