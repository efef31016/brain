import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

class EmailService:
    def __init__(self):
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 465))

    async def send_email(self, receiver_email, subject, body, is_html=False):
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "html" if is_html else "plain"))

        async with aiosmtplib.SMTP(hostname=self.smtp_server, port=self.smtp_port, use_tls=True) as smtp:
            await smtp.login(self.sender_email, self.sender_password)
            await smtp.send_message(message)