from fastapi import APIRouter, Depends
from app.models import User
from app.core.dependencies import get_current_user
from app.schemas import UserProfileResponse


router = APIRouter(prefix="/users", tags=["users"])

@router.get("/profile", response_model = UserProfileResponse)
async def get_profile(current_user:User = Depends(get_current_user)):
    return current_user