import secrets
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi import HTTPException

class EmailService:
     def __init__(self, redis_session_op, sender_email, sender_password):
        self.redis_session_op = redis_session_op
        self.sender_email = sender_email
        self.sender_password = sender_password

     def generate_and_save_verification_code(self, email):

        if self.redis_session_op.redis_config.find_a_set(email):
            raise HTTPException(status_code=400, detail="Invalid email. This email has already been registered")
        
        verification_code = secrets.token_urlsafe()
        # 過期時間 10 分鐘
        self.redis_session_op.redis_config.set_value_with_expiration(f"verification:{email}", verification_code, 600)
        return verification_code
    
     def send_email(self, receiver_email, subject, body):
        # 建構 MIME 多部分訊息對象
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = receiver_email
        message["Subject"] = subject

        # 新增郵件正文
        message.attach(MIMEText(body, "plain"))

        try:
            # 建立 SMTP 會話並傳送郵件
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.sender_email, self.sender_password)
                text = message.as_string()
                server.sendmail(self.sender_email, receiver_email, text)
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
    