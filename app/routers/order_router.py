from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import  AsyncSession
from app.database import get_db
from app.core.dependencies import get_current_user, get_admin_user
from app.models import User
from app.schemas import OrderResponse, OrderStatusUpdate
from app.services.order_service import create_order_service, get_order_service, get_single_order_service, update_order_status_service, cancel_order_service

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderResponse)
async def create_order_router(db:AsyncSession=Depends(get_db), current_user:User=Depends(get_current_user)):
    return await create_order_service(db, current_user)

@router.get("/", response_model=list[OrderResponse])
async def get_order_router(db:AsyncSession=Depends(get_db), current_user:User=Depends(get_current_user)):
    return await get_order_service(db, current_user)

@router.get("/{order_id}", response_model=OrderResponse)
async def get_single_order_router(order_id:int, db:AsyncSession=Depends(get_db), current_user:User=Depends(get_current_user)):
    return await get_single_order_service(order_id, db, current_user)

@router.put("/{order_id}/status", response_model=OrderResponse)
async def update_order_status_router(order_id:int, order_status:OrderStatusUpdate, db:AsyncSession=Depends(get_db), admin_user:User=Depends(get_admin_user)):
    return await update_order_status_service(order_id, order_status, db, admin_user)

@router.put("/{order_id}/cancel")
async def cancel_order_router(order_id:int, db:AsyncSession=Depends(get_db), current_user:User=Depends(get_current_user)):
    return await cancel_order_service(order_id, db, current_user)