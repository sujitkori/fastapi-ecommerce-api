from fastapi import APIRouter, Depends
from app.models import User
from app.core.dependencies import get_current_user


router = APIRouter(prefix="/users", tags=["users"])

@router.get("/profile")
async def get_profile(current_user:User = Depends(get_current_user)):
    return {
        "message":"Protected Route",
        "user": {
            "id": current_user.id,
            "name":current_user.name,
            "email":current_user.email
        }
    }