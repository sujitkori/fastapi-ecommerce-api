from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import UserCreate, UserResponse, LoginRequest, TokenResponse, RefreshTokenRequest, AccessTokenResponse
from app.database import get_db
from app.services.auth_service import register_user_service, login_service, refresh_token_service

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse)
async def register_user(user:UserCreate, db:AsyncSession=Depends(get_db)):
    return await register_user_service(user, db)

@router.post("/login", response_model=TokenResponse)
async def login(user:LoginRequest, db:AsyncSession=Depends(get_db)):
    return await login_service(user, db)

@router.post("/refresh", response_model=AccessTokenResponse)
async def refresh_token_router(token_data:RefreshTokenRequest, db:AsyncSession=Depends(get_db)):
    return await refresh_token_service(token_data, db)