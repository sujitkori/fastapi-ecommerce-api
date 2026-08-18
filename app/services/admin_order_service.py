from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Orders, OrderItems, Product
from sqlalchemy.orm import joinedload, selectinload

async def get_admin_orders_service(db:AsyncSession):
    stmt = (
        select(Orders).options(
            joinedload(Orders.user),
            selectinload(Orders.order_items)
            .joinedload(OrderItems.product)
            .joinedload(Product.category)
        )
        )
    
    result = await db.execute(stmt)
    data = result.scalars().all()
    
    return data