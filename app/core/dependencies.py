from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from app.database import get_db
from app.core.auth import verify_access_token
from app.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token:str=Depends(oauth2_scheme), db:AsyncSession = Depends(get_db)):
    email = verify_access_token(token)
    print(email)

    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    print(user)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    return user

async def get_admin_user(current_user:User=Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    
    return current_user
