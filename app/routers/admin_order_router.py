from fastapi import APIRouter, Depends
from app.schemas import AdminOrderResponse
from sqlalchemy.ext.asyncio import  AsyncSession
from app.database import get_db
from app.core.dependencies import get_admin_user
from app.models import User
from app.services.admin_order_service import get_admin_orders_service

router = APIRouter(prefix="/admin/orders", tags=["Admin Orders"])

@router.get("/", response_model=list[AdminOrderResponse])
async def get_admin_order_router(db:AsyncSession=Depends(get_db), admin_user:User=Depends(get_admin_user)):
    return await get_admin_orders_service(db)