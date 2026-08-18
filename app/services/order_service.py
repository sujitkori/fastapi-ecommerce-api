from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from sqlalchemy import select
from app.models import CartItem, Orders, OrderItems, Product
from sqlalchemy.orm import joinedload, selectinload
from fastapi import HTTPException, status
from app.schemas import OrderStatusUpdate
from app.enums import OrderStatus, PaymentStatus

async def create_order_service(db:AsyncSession, current_user:User):
    stmt = select(CartItem).options(joinedload(CartItem.product)).where(CartItem.user_id == current_user.id)
    result = await db.execute(stmt)
    cart_item = result.scalars().all()

    if not cart_item:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="cart item not found")
    
    total_amount = 0

    for cart in cart_item:
        if cart.quantity > cart.product.stock_quantity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Not enough stock available")
        
        total_amount += cart.quantity*cart.product.price
    print(total_amount)

    new_order = Orders(user_id = current_user.id, total_amount=total_amount)
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)

    for cart in cart_item:
        order_item = OrderItems(
            order_id = new_order.id,
            product_id = cart.product_id,
            quantity = cart.quantity,
            price_at_purchase = cart.product.price
        )
        
        db.add(order_item)
        cart.product.stock_quantity -= cart.quantity
        await db.delete(cart)

    await db.commit()

    stmt = (
        select(Orders).options(
            selectinload(Orders.order_items)
            .joinedload(OrderItems.product)
            .joinedload(Product.category),
            joinedload(Orders.payment)
            )
            .where(Orders.id == new_order.id)
            )
    
    result = await db.execute(stmt)
    final_order = result.unique().scalar_one()

    return final_order


async def get_order_service(db:AsyncSession, current_user:User):
    stmt = (
        select(Orders)
        .options(
            selectinload(Orders.order_items)
            .joinedload(OrderItems.product)
            .joinedload(Product.category),
            joinedload(Orders.payment)
        ).where(Orders.user_id == current_user.id)
    )

    result = await db.execute(stmt)
    order_data = result.unique().scalars().all()

    if not order_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No orders found")

    return order_data

async def get_single_order_service(order_id:int, db:AsyncSession, current_user:User):
    stmt = (
        select(Orders).options(
            selectinload(Orders.order_items)
            .joinedload(OrderItems.product)
            .joinedload(Product.category),
            joinedload(Orders.payment)
            ).where(Orders.id == order_id, Orders.user_id == current_user.id)
        )
    
    result = await db.execute(stmt)
    single_order = result.unique().scalar_one_or_none()

    if not single_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    return single_order


async def update_order_status_service(order_id:int, order_status:OrderStatusUpdate, db:AsyncSession, admin_user):
    stmt = (
        select(Orders).options(
            selectinload(Orders.order_items)
            .joinedload(OrderItems.product)
            .joinedload(Product.category),
            joinedload(Orders.payment)
            ).where(Orders.id == order_id)
        )
    
    result = await db.execute(stmt)
    order_data = result.unique().scalar_one_or_none()

    if not order_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    current_status = order_data.status
    requested_status = order_status.status

    if current_status == OrderStatus.pending:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order must be paid before shipment can begin")

    elif current_status == OrderStatus.paid:
        if requested_status != OrderStatus.processing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A paid order can only move to processing")

    elif current_status == OrderStatus.processing:
        if requested_status != OrderStatus.shipped:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A processing order can only move to shipped")
    
    elif current_status == OrderStatus.shipped:
        if requested_status != OrderStatus.delivered:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A shipped order can only move to delivered")

    elif current_status == OrderStatus.delivered:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order has already been delivered")
    
    elif current_status == OrderStatus.cancelled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cancelled orders cannot be updated")
    
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid order status")

    
    order_data.status = requested_status

    await db.commit()
    await db.refresh(order_data)

    result = await db.execute(stmt)
    updated_order = result.unique().scalar_one()

    return updated_order

async def cancel_order_service(order_id: int, db:AsyncSession, current_user:User):
    order_stmt = (
        select(Orders).options(
            selectinload(Orders.order_items)
            .joinedload(OrderItems.product)
            .joinedload(Product.category),
            joinedload(Orders.payment)
            ).where(Orders.id == order_id, Orders.user_id == current_user.id)
        )
    
    order_result = await db.execute(order_stmt)
    order_exist = order_result.unique().scalar_one_or_none()

    if not order_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    
    if order_exist.status in (
        OrderStatus.pending,
        OrderStatus.paid
    ):
        for order_item in order_exist.order_items:
            order_item.product.stock_quantity += order_item.quantity

        order_exist.status = OrderStatus.cancelled

        if order_exist.payment and order_exist.payment.payment_status == PaymentStatus.success:
            order_exist.payment.payment_status = PaymentStatus.refunded

        await db.commit()
        await db.refresh(order_exist)

        order_result = await db.execute(order_stmt)
        updated_order = order_result.scalar_one()
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"This order cannot be cancelled because it's already {order_exist.status.value}")
    
    return updated_order
