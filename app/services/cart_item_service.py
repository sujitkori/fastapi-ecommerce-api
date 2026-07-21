from sqlalchemy import select
from app.models import CartItem, User, Product
from app.schemas import CartItemCreate, CartItemUpdate
from sqlalchemy.ext.asyncio import  AsyncSession
from fastapi import HTTPException, status
from sqlalchemy.orm import joinedload, selectinload

async def create_cartItem_service(cartItem:CartItemCreate, db:AsyncSession, current_user:User):

    product_stmt = select(Product).where(
        Product.id == cartItem.product_id,
        Product.is_active == True,
        Product.is_deleted == False,
    )

    product_result = await db.execute(product_stmt)
    product_exist = product_result.scalar_one_or_none()

    if not product_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    if product_exist.stock_quantity < cartItem.quantity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough stock available")
    
    
    cartItem_stmt = select(CartItem).where(
        CartItem.user_id == current_user.id, 
        CartItem.product_id == cartItem.product_id
        )
    
    cartItem_result = await db.execute(cartItem_stmt)
    existing_cart_item = cartItem_result.scalar_one_or_none()

    if existing_cart_item:
        new_quantity = existing_cart_item.quantity + cartItem.quantity

        if new_quantity > product_exist.stock_quantity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Only {product_exist.stock_quantity} items available in stock")
        
        existing_cart_item.quantity = new_quantity

        await db.commit()
        await db.refresh(existing_cart_item)

        stmt = (
        select(CartItem).options(
            joinedload(CartItem.product).joinedload(Product.category)
        ).where(CartItem.id == existing_cart_item.id)
        )

        result = await db.execute(stmt)
        new_existing_cart_item = result.scalar_one()

        return new_existing_cart_item
    
    add_cart_item = cartItem.model_dump()
    add_cart_item["user_id"] = current_user.id

    new_add_cart_item = CartItem(**add_cart_item)


    db.add(new_add_cart_item)
    await db.commit()
    await db.refresh(new_add_cart_item)

    stmt = (
        select(CartItem).options(
            joinedload(CartItem.product).joinedload(Product.category)
        ).where(CartItem.id == new_add_cart_item.id)
        )
    
    result = await db.execute(stmt)
    data = result.scalar_one()

    return data

async def get_cartitem_service(db:AsyncSession, current_user:User):
    stmt = (
        select(CartItem)
        .options(
            joinedload(CartItem.product).joinedload(Product.category)
        )
        .where(CartItem.user_id == current_user.id)
    )


    result = await db.execute(stmt)
    cart_data = result.scalars().all()
    return cart_data

async def update_cart_item_service(cart_item_id:int, quantity:CartItemUpdate, db:AsyncSession, current_user:User):
    stmt = (
        select(CartItem).options(
            joinedload(CartItem.product).joinedload(Product.category)
        ).where(CartItem.id == cart_item_id, CartItem.user_id == current_user.id)
        )
    result = await db.execute(stmt)
    cart_item = result.scalar_one_or_none()

    if not cart_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="cart_item not found")
    
    product_stmt = select(Product).where(
        Product.id == cart_item.product_id, 
        Product.is_active == True, 
        Product.is_deleted == False
        )
    
    product_result = await db.execute(product_stmt)
    product_data = product_result.scalar_one_or_none()

    if not product_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        # new_quantity = cart_item.quantity + product_data.stock_quantity

    if quantity.quantity > product_data.stock_quantity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"only {product_data.stock_quantity} items available in stock")
    
    cart_item.quantity = quantity.quantity

    await db.commit()
    await db.refresh(cart_item)

    stmt = (
        select(CartItem)
        .options(joinedload(CartItem.product).joinedload(Product.category))
        .where(CartItem.id == cart_item.id)
        )   
    
    result = await db.execute(stmt)
    return result.scalar_one()


async def delete_cart_service(cart_item_id:int, db:AsyncSession, current_user:User):
    stmt = select(CartItem).where(CartItem.id == cart_item_id, CartItem.user_id == current_user.id)
    result = await db.execute(stmt)
    cart_item = result.scalar_one_or_none()

    if not cart_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CartItem not found")

    await db.delete(cart_item)
    await db.commit()

    return {
        "message":"CartItem deleted successfully"
    }
