from app.schemas import UserCreate, LoginRequest, RefreshTokenRequest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import User
from fastapi import HTTPException, status
from app.core.auth import hash_password, verify_password, create_access_token, create_refresh_token, verify_refresh_token

async def register_user_service(user:UserCreate, db:AsyncSession):
    stmt = select(User).where(User.email == user.email)
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exist")

    hashed_password = hash_password(user.password)
    user_data = user.model_dump()

    user_data["password"] = hashed_password

    new_user = User(**user_data)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user

async def login_service(user:LoginRequest, db:AsyncSession):
    stmt = select(User).where(User.email == user.email)
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()

    if not existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email or password")
    
    is_valid_password = verify_password(user.password, existing_user.password)

    if not is_valid_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    access_token = create_access_token(
        {
            "sub": existing_user.email
        }
    )

    refresh_token = create_refresh_token(
        {
            "sub": existing_user.email
        }
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

async def refresh_token_service(token_data:RefreshTokenRequest, db:AsyncSession):
    email = verify_refresh_token(token_data.refresh_token)

    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    access_token = create_access_token(
        data={"sub": user.email}
    )

    return {
        "access_token":access_token,
        "token_type":"bearer"
    }