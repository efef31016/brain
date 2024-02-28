from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from dependencies import get_login_service
from schemas.LoginSchema import LoginRequest

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/login-form")  
async def get_form(request: Request):
    return templates.TemplateResponse("loginform.html", {"request": request})
    
@router.post("/api/login")
async def login(request: LoginRequest, login_service = Depends(get_login_service)):
    return login_service.login(request.login_identifier, request.password)