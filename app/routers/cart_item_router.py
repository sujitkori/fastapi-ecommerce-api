from fastapi import APIRouter, Depends
from app.schemas import CartItemCreate, CartItemResponse, CartItemUpdate
from sqlalchemy.ext.asyncio import  AsyncSession
from app.database import get_db
from app.core.dependencies import get_current_user
from app.models import User
from app.services.cart_item_service import create_cartItem_service, get_cartitem_service, update_cart_item_service, delete_cart_service


router = APIRouter(prefix="/cart", tags=["Cart"])

@router.post("/", response_model=CartItemResponse)
async def create_cartItem_router(cartItem:CartItemCreate, db:AsyncSession=Depends(get_db), current_user:User=Depends(get_current_user)):
    return await create_cartItem_service(cartItem, db, current_user)

@router.get("/", response_model=list[CartItemResponse])
async def get_cartItem_router(db:AsyncSession=Depends(get_db), current_user:User=Depends(get_current_user)):
    return await get_cartitem_service(db, current_user)

@router.put("/{cart_item_id}", response_model=CartItemResponse)
async def update_cart_item_router(cart_item_id:int, quantity:CartItemUpdate, db:AsyncSession=Depends(get_db), current_user:User=Depends(get_current_user)):
    return await update_cart_item_service(cart_item_id, quantity, db, current_user)

@router.delete("/{cart_item_id}")
async def delete_cart_router(cart_item_id:int, db:AsyncSession=Depends(get_db), current_user:User=Depends(get_current_user)):
    return await delete_cart_service(cart_item_id, db, current_user)