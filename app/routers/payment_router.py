from fastapi import APIRouter, Depends
from app.schemas import CreatePayment, PaymentResponse, PaymentStatusUpdate
from app.database import get_db
from app.core.dependencies import get_current_user, get_admin_user
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.services.payment_service import create_payment_service, get_all_payment_service, get_all_admin_payment_service, get_single_payment_service, update_payment_status_service

router = APIRouter(prefix="/payment", tags=["Payment"])

@router.post("/{order_id}", response_model=PaymentResponse)
async def create_payment_router(order_id:int, payment: CreatePayment, db:AsyncSession=Depends(get_db), current_user:User=Depends(get_current_user)):
    return await create_payment_service(order_id, payment, db, current_user)

@router.get("/", response_model=list[PaymentResponse])
async def get_all_payment_router(db:AsyncSession=Depends(get_db), current_user:User=Depends(get_current_user)):
    return await get_all_payment_service(db, current_user)

@router.get("/admin/", response_model=list[PaymentResponse])
async def get_all_admin_payment_router(db:AsyncSession=Depends(get_db), admin_user:User=Depends(get_admin_user)):
    return await get_all_admin_payment_service(db)

@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_single_payment_router(payment_id: int, db:AsyncSession=Depends(get_db), current_user:User=Depends(get_current_user)):
    return await get_single_payment_service(payment_id, db, current_user)

@router.put("/{payment_id}/status", response_model=PaymentResponse)
async def update_payment_status_router(payment_id:int, payment_status_update:PaymentStatusUpdate, db:AsyncSession=Depends(get_db), admin_user:User=Depends(get_admin_user)):
    return await update_payment_status_service(payment_id, payment_status_update, db, admin_user)