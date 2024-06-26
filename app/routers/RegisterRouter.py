from fastapi import APIRouter, Request, Depends, Form, HTTPException, status
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from dependencies import get_register_service, get_email_service
from schemas.EmailSchema import EmailSchema
from schemas.VerifyEmailSchema import VerifyEmailRequest

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/register-form")
async def get_form(request: Request):
    return templates.TemplateResponse("registerform.html", {"request": request})

@router.post("/api/send-verification-email")
async def send_verification_email(email_data: EmailSchema, email_service=Depends(get_email_service)):
    email = email_data.email

    try:
        verification_code = email_service.generate_and_save_verification_code(email)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"error": str(e.detail)})

    subject = "[Let\'s Debate]Email Verification"
    body = f"請利用以下驗證碼完成電子信箱認證:\n{verification_code}"
    email_service.send_email(receiver_email=email, subject=subject, body=body)
    
    return {"message": "Verification email sent."}

@router.post("/api/verify-email-code")
async def verify_email_code(request: VerifyEmailRequest, email_service=Depends(get_email_service)):
    if email_service.verify_email_code(request.email, request.code):
        success_msg = "Email verified successfully."
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": success_msg})
    else:
        error_msg = "Invalid verification code."
        raise HTTPException(status_code=400, detail=error_msg)
    
@router.post("/api/register-submit-form")
async def register_submit_form(snick: str = Form(...), pwd: str = Form(...), 
                               email: str = Form(...), verify: str = Form(...), 
                               register_service=Depends(get_register_service)):
    try:
        result = register_service.register(snick, pwd, email, verify)
        return RedirectResponse(url="/", status_code=303)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"error": str(e.detail)})