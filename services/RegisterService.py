import re
import uuid
import hashlib
from fastapi import HTTPException

class RegisterService:
    def __init__(self, neo4j_user_op, redis_session_op):
        self.neo4j_user_op = neo4j_user_op
        self.redis_session_op = redis_session_op
        self.initial_verify_code = self._generate_initial_verify_code()

    def _generate_initial_verify_code(self):
        # 初始邀請碼
        initial_code = hashlib.sha256("FalseIssue".encode('utf-8')).hexdigest()
        # 使用 redis_session_op 初始化第一代邀請碼使用次數
        self.redis_session_op.redis_config.set_value("verify_usage:" + initial_code, 0) 
        return 
    
    def register(self, snick, pwd, email, verify):
        print(snick)
        # 驗證使用者名稱
        if not re.match(r'^[a-zA-Z0-9_\u4e00-\u9fff]{1,20}$', snick):
            raise HTTPException(status_code=400, detail="Invalid username. Username should be 3-20 characters long and can contain letters, numbers, and underscores.")
    
        # 驗證密碼長度
        if len(pwd) < 8:
            raise HTTPException(status_code=400, detail="Password must be at least 8 characters long.")
        
        # 驗證電子信箱
        if not self.redis_session_op.redis_config.find_a_set(email):
            raise HTTPException(status_code=400, detail="Please verify your email.")

        # 驗證邀請碼
        self._validate_token(verify)
    
        # 加密密碼
        hashed_password = hashlib.sha256(pwd.encode()).hexdigest()
    
        # 為新用戶設定新的邀請碼和使用次數
        person_uuid, invited_token = self._generate_uuid_and_token()
    
        # 儲存使用者資訊到 Neo4j
        try:
            self.neo4j_user_op.save_user(snick, email, hashed_password, person_uuid, token=invited_token, verify=verify)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to save user: {e}")
   
        return {"new_verify_code": invited_token}

    def _validate_token(self, verify):
        # 邀請碼使用次數檢查
        usage_count = self.redis_session_op.redis_config.get_value("verify_usage:" + verify)
        if usage_count is None:
            raise HTTPException(status_code=400, detail="Verification code not found.")
        if int(usage_count) >= 5:
            raise HTTPException(status_code=400, detail="Verification code has been used too many times.")
        # 更新邀請碼使用次屬
        self.redis_session_op.redis_config.r.hincrby("verify_usage", verify, 1)

    def _generate_uuid_and_token(self):
        person_uuid = str(uuid.uuid4())
        token = hashlib.sha256(person_uuid.encode('utf-8')).hexdigest()
        # 初始化新 token 的使用次數
        self.redis_session_op.redis_config.set_value("verify_usage:" + token, 0)
        return person_uuid, token

    def _validate_input(self, value, pattern, field_name):
        if not re.match(pattern, value):
            raise HTTPException(status_code=400, detail=f"{field_name} input is invalid.")