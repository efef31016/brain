from fastapi import APIRouter, Request, Depends, Form, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from dependencies import get_register_service, get_email_service, get_email_verify_service
from schemas.EmailSchema import EmailSchema
from schemas.VerifyEmailSchema import VerifyEmailRequest

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/register-form")
async def get_form(request: Request):
    # 直接返回註冊表單頁面，非同步操作確保處理請求時不會阻塞
    return templates.TemplateResponse("registerform.html", {"request": request})

@router.post("/api/send-verification-email")
async def send_verification_email(email_data: EmailSchema, email_service=Depends(get_email_service),
                                email_verify_service=Depends(get_email_verify_service)):
    # 非同步發送驗證郵件，提高郵件處理效率
    email = email_data.email
    try:
        verification_code = await email_verify_service.generate_verification_code(email)
        subject = "[Let\'s Debate] 信箱驗證"
        body = f"請利用下列驗證碼完成電子信箱認證:\n{verification_code}"
        await email_service.send_email(receiver_email=email, subject=subject, body=body)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"message": str(e.detail)})
    except Exception as e:
        # 對其他可能的異常進行捕獲，避免服務中斷
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": str(e)})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "驗證信箱已寄出"})

@router.post("/api/verify-email-code")
async def verify_email(request: VerifyEmailRequest, email_service=Depends(get_email_service)):
    # 非同步驗證電子郵件驗證碼
    if await email_service.verify_email_code(request.email, request.code):
        success_msg = "電子信箱通過驗證"
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": success_msg})
    else:
        error_msg = "Invalid verification code."
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": error_msg})
    
@router.post("/api/register-submit-form")
async def register_submit_form(snick: str = Form(...), pwd: str = Form(...),
                            email: str = Form(...), verify: str = Form(...),
                            register_service=Depends(get_register_service)):
    # 非同步處理註冊表單提交
    try:
        await register_service.register(snick, pwd, email, verify)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "註冊成功!"})
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"message": str(e.detail)})
    except Exception as e:
        # 處理可能的未知異常，提高系統的健全性
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": str(e)})