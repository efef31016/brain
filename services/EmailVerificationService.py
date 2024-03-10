import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from shared.BaseVerificationService import BaseVerificationService
from config_manager import ConfigManager

class EmailVerificationService(BaseVerificationService):
    def __init__(self, redis_op, postgresql_op, neo4j_op):
        super().__init__(redis_op, postgresql_op, neo4j_op)
        self.sender_email = ConfigManager.SENDER_EMAIL
        self.sender_password = ConfigManager.SENDER_PASSWORD
        self.smtp_server = ConfigManager.SMTP_SERVER
        self.smtp_port = ConfigManager.SMTP_PORT

    async def send_verification(self, receiver_email: str, code: str):
        subject = "驗證信"
        body = f"您的驗證碼為: {code}\n請使用以上驗證碼完成信箱認證。"
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # 異步發送電子郵件
        # 創建了一個客戶端，用於與SMTP伺服器通訊
        async with aiosmtplib.SMTP(hostname=self.smtp_server, port=self.smtp_port, use_tls=True) as smtp:
            await smtp.login(self.sender_email, self.sender_password)
            await smtp.send_message(message)
