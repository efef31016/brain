import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailService:
    def __init__(self, sender_email, sender_pwd, smtp_server, smtp_port):
        self.sender_email = sender_email
        self.sender_password = sender_pwd
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    async def send_email(self, receiver_email, subject, body, is_html=False):
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "html" if is_html else "plain"))

        async with aiosmtplib.SMTP(hostname=self.smtp_server, port=self.smtp_port, use_tls=True) as smtp:
            await smtp.login(self.sender_email, self.sender_password)
            await smtp.send_message(message)