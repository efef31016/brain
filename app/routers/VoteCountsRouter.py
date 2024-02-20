from fastapi import APIRouter
from dependencies import get_vote_counts_service

router = APIRouter()

@router.get("/api/whichCounts")
async def get_user_counts():
    return get_vote_counts_service.user_counts()