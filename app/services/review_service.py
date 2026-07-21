from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User, Review, Product, Orders, OrderItems
from app.schemas import ReviewRequest
from fastapi import HTTPException, status
from sqlalchemy import select
from app.enums import OrderStatus

async def create_review_service( product_id:int, review_request:ReviewRequest, db: AsyncSession, current_user:User):
    product_stmt = select(Product).where(Product.id == product_id)
    product_result = await db.execute(product_stmt)
    product_exist = product_result.scalar_one_or_none()

    if not product_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    

    review_stmt = select(Review).where(Review.product_id == product_id, Review.user_id == current_user.id)
    review_result = await db.execute(review_stmt)
    review_exist = review_result.scalar_one_or_none()

    if review_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You can only review a product once.")
    
    is_order_delivered_stmt = (
        select(OrderItems).join(OrderItems.order)
        .where(
            Orders.user_id == current_user.id, 
            Orders.status == OrderStatus.delivered,
            OrderItems.product_id == product_id
        )
    )
    is_order_delivered_result = await db.execute(is_order_delivered_stmt)
    is_order_delivered_data = is_order_delivered_result.scalar_one_or_none()

    if not is_order_delivered_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You can only review products you have purchased.")
    
    review_data = review_request.model_dump()

    review_data["user_id"] = current_user.id
    review_data["product_id"] = product_id

    new_review = Review(**review_data)

    db.add(new_review)
    await db.commit()
    await db.refresh(new_review)

    return new_review


async def get_all_review_service(product_id: int, db:AsyncSession):
    prdt_stmt = select(Product).where(Product.id == product_id)
    prdt_result = await db.execute(prdt_stmt)
    prdt_exist = prdt_result.scalar_one_or_none()

    if not prdt_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    stmt = select(Review).where(Review.product_id == product_id)
    result = await db.execute(stmt)
    review_data = result.scalars().all()

    return review_data

async def update_review_service(product_id: int, review_request:ReviewRequest, db:AsyncSession, current_user:User):
    stmt = select(Review).where(Review.product_id == product_id, Review.user_id == current_user.id)
    result = await db.execute(stmt)
    review_data = result.scalar_one_or_none()

    if not review_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No review found")

    updated_review = review_request.model_dump(exclude_unset=True)

    for key, value in updated_review.items():
        setattr(review_data, key, value)

    await db.commit()
    await db.refresh(review_data)

    return review_data

    
