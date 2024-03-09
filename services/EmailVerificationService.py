import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from shared.BaseVerificationService import BaseVerificationService
from Config import redis_config, SENDER_EMAIL, SENDER_PASSWORD, SMTP_SERVER, SMTP_PORT

class EmailVerificationService(BaseVerificationService):
    def __init__(self,):
        super().__init__()
        self.sender_email = SENDER_EMAIL
        self.sender_password = SENDER_PASSWORD
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT

    async def send_verification(self, receiver_email: str, code: str):
        subject = "驗證信"
        body = f"您的驗證碼為: {code}\n請使用以上驗證碼完成信箱認證"
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        async with aiosmtplib.SMTP(hostname=self.smtp_server, port=self.smtp_port, use_tls=True) as smtp:
            await smtp.login(self.sender_email, self.sender_password)
            await smtp.send_message(message)


if __name__ == "__main__":
    import asyncio

    async def send_test_email():
        service = EmailVerificationService()
        
        test_email = "yhocotw31016@gmail.com"
        verification_code = "test"
        await service.send_verification(test_email, verification_code)
        print(f"Verification email sent to {test_email} with code {verification_code}")
        await service.generate_verification_code(verification_code, test_email)
    asyncio.run(send_test_email())