import re
import uuid
from AuthService import ph
from fastapi import HTTPException

class RegisterService:
    def __init__(self, neo4j_user_op, redis_session_op):
        self.neo4j_user_op = neo4j_user_op
        self.redis_session_op = redis_session_op
        self.initial_verify_code = self._generate_initial_verify_code()

    def _generate_initial_verify_code(self):
        # 初始邀請碼
        init_token = "FakeIssue"
        initial_code = ph.hash(init_token)
        # 使用 redis_session_op 初始化第一代邀請碼使用次數
        self.redis_session_op.redis_config.set_value("verify_usage:" + initial_code, 0) 
        return 
    
    def register(self, snick, pwd, email, verify):

        # 驗證帳號
        if not re.match(r'^[a-zA-Z0-9_\u4e00-\u9fff]{1,20}$', snick):
            raise HTTPException(status_code=400, detail="使用者名稱僅支援1-20位的字母、數字、底線和中文字元。")
        
        # 驗證密碼
        if len(pwd) < 8:
            raise HTTPException(status_code=400, detail="密碼需超過8位數。")

        # 驗證電子信箱
        if not self.redis_session_op.redis_config.find_a_set(email):
            raise HTTPException(status_code=400, detail="請認證電子信箱。")
        
        query = "MATCH (n {email: $email}) RETURN n LIMIT 1"
        parameters = {"email": email}
        result = self.neo4j_user_op.neo4j_config.run_query(query, parameters)
        if len(result) > 0:
            raise HTTPException(status_code=400, detail="此信箱已被註冊")

        # 驗證邀請碼
        self._validate_token(verify)
    
        # 加密密碼
        hashed_password = ph.hash(pwd)
    
        # 為新用戶設定新的邀請碼和使用次數
        person_uuid, invited_token = self._generate_uuid_and_token()
    
        # 儲存使用者資訊到 Neo4j
        try:
            self.neo4j_user_op.save_user(snick, email, hashed_password, person_uuid, token=invited_token, verify=verify)
            self.redis_session_op.redis_config.set_value("verify_usage:" + verify, 1)
        except:
            raise HTTPException(status_code=400, detail = "用戶資料儲存失敗")
   
        return {"new_verify_code": invited_token}

    def _validate_token(self, verify):
        # 邀請碼使用次數檢查
        usage_count = self.redis_session_op.redis_config.get_value("verify_usage:" + verify)
        if usage_count is None:
            raise HTTPException(status_code=400, detail="邀請碼不存在.")
        if int(usage_count) >= 5:
            raise HTTPException(status_code=400, detail="邀請碼無法使用(原因: 超過使用次數)")
        # 更新邀請碼使用次屬
        self.redis_session_op.redis_config.r.hincrby("verify_usage", verify, 1)

    def _generate_uuid_and_token(self):
        person_uuid = str(uuid.uuid4())
        token = ph.hash(person_uuid)
        # 初始化新 token 的使用次數
        self.redis_session_op.redis_config.set_value("verify_usage:" + token, 0)
        return person_uuid, token

    def _validate_input(self, value, pattern, field_name):
        if not re.match(pattern, value):
            raise HTTPException(status_code=400, detail=f"{field_name} input is invalid.")