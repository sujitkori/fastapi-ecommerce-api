from fastapi import APIRouter, Depends
from app.schemas import CategoryCreate, CategoryResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.category_service import create_categories_service, get_categories_service
from app.models import User
from app.core.dependencies import get_admin_user

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=CategoryResponse)
async def create_categories(category:CategoryCreate, db:AsyncSession=Depends(get_db), admin_user:User=Depends(get_admin_user)):
    return await create_categories_service(category, db, admin_user)

@router.get("/", response_model=list[CategoryResponse])
async def get_categories(db:AsyncSession=Depends(get_db)):
    return await get_categories_service(db)
    