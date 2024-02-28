from pydantic import BaseModel

class LogoutRequest(BaseModel):
    device_id: str