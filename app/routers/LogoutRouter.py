from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from dependencies import get_logout_service

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/logout")
async def logout():