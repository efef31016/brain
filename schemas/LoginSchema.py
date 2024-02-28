from pydantic import BaseModel

class LoginRequest(BaseModel):
    login_identifier: str
    password: str
    device_id: str