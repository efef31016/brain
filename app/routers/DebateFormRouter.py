# from fastapi import APIRouter, Depends, Form, HTTPException
# from fastapi.responses import RedirectResponse
# from dependencies import get_debate_service

# router = APIRouter()

# @router.post("/debate-form")

# @router.post("/api/debate-submit-form")
# async def submit_form(snick: str = Form(...), pwd: str = Form(...), email: str = Form(...),
#                       name: str = Form(...), job: str = Form(...), age: int = Form(...),
#                       verify: str = Form(...), person_service=Depends(get_debate_service)):
#     try:
#         person_service.register(snick, pwd, email, name, age, job, verify)
#     except HTTPException as e:
#         error_message = str(e.detail)
#         return RedirectResponse(url=f"/form?error={error_message}", status_code=303)
#     return RedirectResponse(url="/", status_code=303)