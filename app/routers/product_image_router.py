from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.product_image_service import upload_product_image_service, update_product_image_service
from app.schemas import ProductResponse

from app.database import get_db
from app.core.dependencies import get_admin_user
from app.models import User

router = APIRouter(prefix="", tags=["Product Images"])

@router.post("/products/{product_id}/image", response_model=ProductResponse)
async def upload_product_image_router(product_id: int, image: UploadFile = File(...), db:AsyncSession=Depends(get_db), admin_user:User=Depends(get_admin_user)):
    return await upload_product_image_service(product_id, image, db, admin_user)

@router.put("/products/{product_id}/image", response_model=ProductResponse)
async def update_product_image_router(product_id: int, image: UploadFile = File(...), db:AsyncSession=Depends(get_db), admin_user:User=Depends(get_admin_user)):
    return await update_product_image_service(product_id, image, db, admin_user)




# NOTE:
# image: UploadFile = File(...)
# the ... is Python's Ellipsis object. In FastAPI, when used inside File(...), it means:

# This file field is required.

# So,
# image: UploadFile = File(...)
# means:

# image is an uploaded file
# FastAPI should read it from a multipart/form-data request
# the file is required
# FastAPI uses ... as a conventional way to say "no default value; this must be provided."

# image: UploadFile = File(None) means
# Optional,The client can omit the image, and image can be None.

# File(...) = required uploaded file.
# File(None) = optional uploaded file.