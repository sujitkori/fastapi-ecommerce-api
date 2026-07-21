from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User, Product
from fastapi import UploadFile, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.utils.image_utils import save_image, validate_image
from pathlib import Path

async def upload_product_image_service(product_id: int, image:UploadFile, db:AsyncSession, admin_user:User):
    stmt = select(Product).options(joinedload(Product.category)).where(Product.id == product_id)

    result = await db.execute(stmt)

    product_exist = result.scalar_one_or_none()

    if not product_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    validate_image(image)
    
    image_path = await save_image(image)

    product_exist.image = image_path 

    await db.commit()
    await db.refresh(product_exist)

    return product_exist


async def update_product_image_service(product_id: int, image:UploadFile, db:AsyncSession, admin_user:User):
    stmt = select(Product).options(joinedload(Product.category)).where(Product.id == product_id)

    result = await db.execute(stmt)

    product_exist = result.scalar_one_or_none()

    if not product_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    validate_image(image)
    
    old_image = product_exist.image

    image_path = await save_image(image)

    product_exist.image = image_path 

    await db.commit()
    await db.refresh(product_exist)

    if old_image:
        old_image_path = Path(old_image)

        if old_image_path.exists():
            old_image_path.unlink()

    return product_exist