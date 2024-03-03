import secrets
import smtplib
import urllib.parse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi import HTTPException

class EmailService:
    def __init__(self, postgresql_user_op, redis_session_op, sender_email, sender_password):
        self.postgresql_user_op = postgresql_user_op
        self.redis_session_op = redis_session_op
        self.sender_email = sender_email
        self.sender_password = sender_password

    def generate_and_save_verification_code(self, email):

        sql = "SELECT * FROM \"user\".users WHERE email = %s LIMIT 1;"
        result = self.postgresql_user_op.db_config.select(sql, (email,))
        if len(result) > 0:
            raise HTTPException(status_code=400, detail="此信箱已被註冊")

        if self.redis_session_op.redis_config.find_a_set(email):
            raise HTTPException(status_code=400, detail="此信箱已認證，請直接跳過驗證步驟")
        
        verification_code = ''.join([str(secrets.randbelow(10)) for _ in range(6)])
        # 過期時間 10 分鐘
        self.redis_session_op.redis_config.set_value_with_expiration(f"verification:{email}", verification_code, 600)
        return verification_code
    
    def send_email(self, receiver_email, subject, body, is_html=False):
        # 建立 MIME 多部分訊息對象
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = receiver_email
        message["Subject"] = subject

        if is_html:
            # 新增郵件內文為HTML
            message.attach(MIMEText(body, "html"))
        else:
            # 新增郵件內文為純文字
            message.attach(MIMEText(body, "plain"))

        try:
            # 建立 SMTP 會話並傳送郵件
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, receiver_email, message.as_string())
            print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")

    def verify_email_code(self, email, user_code):
        stored_code = self.redis_session_op.redis_config.get_value(f"verification:{email}")
        if stored_code and stored_code == user_code:
            self.redis_session_op.redis_config.set_a_set("verified_emails", email)
            return True
        else:
            return False
        
    def send_password_reset_email(self, email):
        # 產生一個安全的令牌
        token = secrets.token_urlsafe(16)
        # 保存令牌和郵箱的對應到Redis，過期時間為10分鐘
        self.redis_session_op.redis_config.set_value_with_expiration(f"reset_password_token:{token}", email, 600)
        # 建立重設密碼的URL
        reset_password_url = f"http://localhost:8000/reset-password?token={urllib.parse.quote_plus(token)}"

        # 郵件主題和正文
        subject = "重設您的密碼"
        body = f"請點擊以下連結重設您的密碼: <a href='{reset_password_url}'>{reset_password_url}</a>"

        # 發送郵件
        self.send_email(receiver_email=email, subject=subject, body=body, is_html=True)
        

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv(".env.test")
    sender_email = os.getenv("GMAIL_USER")
    sender_password = os.getenv("GMAIL_PASSWORD")
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from Config import *
    redis_config = RedisConfig(host='localhost', port=6379, password='brainconnect', db=0)
    email_service = EmailService(redis_config, sender_email, sender_password)
    email = "yhocotw31016@gmail.com"
    verification_code = email_service.generate_and_save_verification_code(email)
    subject = "Your Verification Code"
    body = f"Your verification code is: {verification_code}\nPlease use this code to complete your email verification."
    email_service.send_email(receiver_email=email, subject=subject, body=body)