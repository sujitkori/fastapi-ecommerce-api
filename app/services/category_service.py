from app.schemas import CategoryCreate, CategoryResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Category
from fastapi import HTTPException, status
from app.models import User

async def create_categories_service(category:CategoryCreate, db:AsyncSession, admin_user:User):
    stmt = select(Category).where(Category.name == category.name)
    result = await db.execute(stmt)
    existing_category = result.scalar_one_or_none()

    if existing_category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="category already exist")
    
    new_category = Category(name = category.name)
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)

    return new_category


async def get_categories_service(db:AsyncSession):
    stmt = select(Category)
    result = await db.execute(stmt)
    categories = result.scalars().all()
    return categories