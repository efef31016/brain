from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from app.routers.ChooseTopicRouter import debates_info

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/")
async def get_home(request: Request, topic_id: str = None):

    page_title = "歡迎來到辯論大會"
    welcome_message = "僅做為學術研究，請先不要起爭議..."
    
    if topic_id and topic_id in debates_info:
        page_title = debates_info[topic_id]
    elif topic_id:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "page_title": page_title,
        "welcome_message": welcome_message
    })