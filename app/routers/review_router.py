from fastapi import APIRouter, Depends
from app.database import get_db
from app.core.dependencies import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.schemas import ReviewRequest, ReviewResponse
from app.services.review_service import create_review_service, get_all_review_service, update_review_service

router = APIRouter(prefix="", tags=["Reviews"])

@router.post("/products/{product_id}/reviews", response_model=ReviewResponse)
async def create_review_router(product_id:int, review_request:ReviewRequest, db:AsyncSession=Depends(get_db), current_user:User=Depends(get_current_user)):
    return await create_review_service(product_id, review_request, db, current_user)

@router.get("/products/{product_id}/reviews", response_model=list[ReviewResponse])
async def get_all_reviews_router(product_id: int, db:AsyncSession=Depends(get_db)):
    return await get_all_review_service(product_id, db)

@router.put("/products/{product_id}/reviews",response_model=ReviewResponse)
async def update_review_router(product_id: int, review_request:ReviewRequest, db:AsyncSession=Depends(get_db), current_user:User=Depends(get_current_user)):
    return await update_review_service(product_id, review_request, db, current_user)