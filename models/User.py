class User:
    def __init__(self, username, email, password, inviter_token):
        self.username = username
        self.email = email
        self.password = password  # 須加密
        self.inviter_token = inviter_token
