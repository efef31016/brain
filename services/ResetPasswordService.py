from services.AuthService import ph

class ResetPasswordService:
    def __init__(self, postgresql_user_op, redis_session_op):
        self.postgresql_user_op = postgresql_user_op
        self.redis_session_op = redis_session_op

    def valid_token(self, token):
        email = self.redis_session_op.redis_config.get_value(f"reset_password_token:{token}")
        if not email:
            return {
                "status": "error",
                "message": "invalid reset password URL."
                }
        else:
            return {
                "status": "success",
                "mwssage": "ready to update password."
            }

    def update_user_password(self, email, new_password):

        new_password = ph.hash(new_password)
        
        query = "UPDATE \"user\".users SET password = %s WHERE email = %s"
        parameters = (new_password, email)
        
        rows_affected = self.postgresql_user_op.db_config.update(query, parameters)
        
        if rows_affected > 0:
            return True, f"已成功更改 {email} 的密碼。"
        else:
            return False, f"{email} 此信箱未註冊。"