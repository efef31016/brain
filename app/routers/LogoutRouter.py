from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from dependencies import get_logout_service
from schemas.LogoutSchema import LogoutRequest
import jwt
import os
from dotenv import load_dotenv
load_dotenv(r"D:\brain\.env")

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

@router.post("/logout")
async def logout(request: LogoutRequest, logout_service=Depends(get_logout_service), token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, os.getenv("SECRET"), algorithms=['HS256'])
    user_id = payload.get("sub")
    return logout_service.logout(user_id, token, request.device_id)