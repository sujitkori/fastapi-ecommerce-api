from fastapi import APIRouter, Depends, Query
from app.schemas import ProductCreate, ProductResponse, ProductUpdate, ProductSortFields, SortOrder, ProductListResponse
from app.database import get_db
from app.core.dependencies import get_current_user, get_admin_user
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.services.product_service import product_create_service, product_fetch_service, get_single_product_service, update_single_product_service, delete_product_service

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductResponse)
async def product_create_router(product:ProductCreate, db:AsyncSession=Depends(get_db), admin_user:User=Depends(get_admin_user)):
    return await product_create_service(product, db)

@router.get("/", response_model=ProductListResponse)
async def product_fetch_router(skip:int = Query(default=0, ge=0), limit:int = Query(default=10, ge=0, le=100), category_id: int | None = None, min_price: int | None = None, max_price:int | None = None, search:str | None = None , sort_by:ProductSortFields | None = None, sort_order:SortOrder = SortOrder.asc , db:AsyncSession=Depends(get_db), _current_user:User=Depends(get_current_user)):
    return await product_fetch_service(skip, limit, category_id, min_price, max_price, search, sort_by, sort_order, db)

@router.get("/{product_id}", response_model=ProductResponse)
async def get_single_product_router(product_id:int, db:AsyncSession=Depends(get_db), _current_user:User=Depends(get_current_user)):
    return await get_single_product_service(product_id, db)

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product_router(product_id:int, product:ProductUpdate, db:AsyncSession=Depends(get_db), _admin_user:User=Depends(get_admin_user)):
    return await update_single_product_service(product_id, product, db)

@router.delete("/{product_id}")
async def delete_product_router(product_id:int, db:AsyncSession=Depends(get_db), _admin_user:User=Depends(get_admin_user)):
    return await delete_product_service(product_id, db)