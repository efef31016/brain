import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

class EmailVerificationService(BaseVerificationService):
    def __init__(self, redis_url: str):
        super().__init__(redis_url)
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 465))

    async def send_verification(self, receiver_email: str, code: str):
        subject = "Your Verification Code"
        body = f"Your verification code is: {code}\nPlease use this code to complete your email verification."
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        async with aiosmtplib.SMTP(hostname=self.smtp_server, port=self.smtp_port, use_tls=True) as smtp:
            await smtp.login(self.sender_email, self.sender_password)
            await smtp.send_message(message)


import asyncio

async def main():
    redis_url = "redis://localhost:6379/0"
    email_verification_service = EmailVerificationService(redis_url)
    email = "example@example.com"
    code = await email_verification_service.generate_verification_code(email, "email")
    await email_verification_service.send_verification(email, code)

if __name__ == "__main__":
    asyncio.run(main())