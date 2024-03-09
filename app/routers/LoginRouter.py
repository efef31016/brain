# from fastapi import APIRouter, Request, Depends, HTTPException, Query
# from fastapi.templating import Jinja2Templates
# from dependencies import get_login_service, get_reset_password_service, get_email_service
# from schemas.LoginSchema import LoginRequest
# from schemas.ResetPassword import PasswordResetRequest, PasswordReset

# router = APIRouter()

# templates = Jinja2Templates(directory="templates")

# @router.get("/login-form")  
# async def get_form(request: Request):
#     return templates.TemplateResponse("loginform.html", {"request": request})
    
# @router.post("/api/login")
# async def login(request: LoginRequest, login_service = Depends(get_login_service)):
#     return login_service.login(request.login_identifier, request.password, request.device_id)


# @router.post("/api/request-reset-password")
# async def request_reset_password(request: PasswordResetRequest,
#                                 email_service = Depends(get_email_service)):
#     try:
#         email_service.send_password_reset_email(request.email)
#         return {"message": "重設密碼郵件已傳送，請檢查您的信箱。"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @router.get("/reset-password")
# async def get_form(request: Request):
#     return templates.TemplateResponse("resetpassword.html", {"request": request})

# @router.post("/api/reset-password")
# async def reset_password(reset_request: PasswordReset,
#                         reset_password_service = Depends(get_reset_password_service)):
    
#     validation_result = reset_password_service.valid_token(reset_request.token)
#     if validation_result["status"] == "error":
#         raise HTTPException(status_code=400, detail=validation_result["message"])
    
#     email = reset_password_service.redis_session_op.redis_config.get_value(f"reset_password_token:{reset_request.token}")
#     update_result = reset_password_service.update_user_password(email, reset_request.new_password)
#     if update_result[0]:
#         return {"message": update_result[1]}
#     else:
#         raise HTTPException(status_code=400, detail=update_result[1])