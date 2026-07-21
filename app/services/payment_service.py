from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from fastapi import HTTPException, status
from app.schemas import CreatePayment
from app.models import Orders, Payment
from app.enums import OrderStatus, PaymentStatus
import uuid
from app.schemas import PaymentStatusUpdate

async def create_payment_service(order_id:int, payment:CreatePayment, db:AsyncSession, current_user:User):
    stmt = select(Orders).where(Orders.id == order_id, Orders.user_id == current_user.id)
    result = await db.execute(stmt)
    order_exists = result.scalar_one_or_none()

    if not order_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    
    payment_stmt = select(Payment).where(Payment.order_id == order_exists.id)
    payment_result = await db.execute(payment_stmt)
    payment_exists = payment_result.scalar_one_or_none()

    if payment_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Payment already exists for this order")
    
    new_payment = Payment(
        order_id = order_exists.id,
        amount = order_exists.total_amount,
        payment_method = payment.payment_method,
        payment_status = PaymentStatus.pending,
        transaction_id = str(uuid.uuid4())
    )

    # order_exists.status = OrderStatus.paid

    db.add(new_payment)
    await db.commit()
    await db.refresh(new_payment)

    return new_payment

async def get_all_payment_service(db:AsyncSession, current_user:User):
    stmt = select(Payment).join(Payment.order).where(Orders.user_id == current_user.id)
    result = await db.execute(stmt)
    payment_data = result.scalars().all()

    if not payment_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No payments found")

    return payment_data
    

async def get_single_payment_service(payment_id: int, db:AsyncSession, current_user:User):
    stmt = select(Payment).join(Payment.order).where(Payment.id == payment_id, Orders.user_id == current_user.id)
    result = await db.execute(stmt)
    payment_single_data = result.scalar_one_or_none()

    if not payment_single_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No payment record found")

    return payment_single_data

async def update_payment_status_service(payment_id:int, payment_status_update:PaymentStatusUpdate, db:AsyncSession, admin_user:User):
    stmt = select(Payment).options(joinedload(Payment.order)).where(Payment.id == payment_id)
    result = await db.execute(stmt)
    payment_data = result.scalar_one_or_none()

    if not payment_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
    
    if payment_data.payment_status in (PaymentStatus.success, PaymentStatus.failed):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Payment has already been processed")
    

    if payment_status_update.payment_status_update == PaymentStatus.success:
        payment_data.payment_status = payment_status_update.payment_status_update
        payment_data.order.status = OrderStatus.paid

    elif payment_status_update.payment_status_update == PaymentStatus.failed:
        payment_data.payment_status = PaymentStatus.failed

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid payment status transition"
        )

    await db.commit()
    await db.refresh(payment_data)

    return payment_data
