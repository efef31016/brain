# from fastapi import APIRouter, Request, Depends
# from fastapi.templating import Jinja2Templates
# from dependencies import get_myaccount_service

# router = APIRouter()

# templates = Jinja2Templates(directory="templates")

# @router.get("/my-account")  
# async def get_form(request: Request):
#     return templates.TemplateResponse("myaccount.html", {"request": request})