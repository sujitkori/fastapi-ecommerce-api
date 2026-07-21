from app.schemas import ProductCreate, ProductUpdate, ProductSortFields, SortOrder, ProductResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from sqlalchemy import select, func
from app.models import Product, Category, Review
from fastapi import HTTPException, status
from sqlalchemy.orm import joinedload

async def product_create_service(product:ProductCreate, db:AsyncSession):
    product_stmt = select(Product).where(Product.name == product.name)
    product_result = await db.execute(product_stmt)
    existing_product = product_result.scalar_one_or_none()

    if existing_product:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product already exists")

    category_stmt = select(Category).where(Category.id == product.category_id)
    category_result = await db.execute(category_stmt)
    exist_category = category_result.scalar_one_or_none()

    if not exist_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category doesn't exist")
    
    product_data = product.model_dump()
    new_product = Product(**product_data) 
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)

    stmt = (
        select(Product)
        .options(
            joinedload(Product.category)
        )
        .where(Product.id == new_product.id)
    )

    result = await db.execute(stmt)
    new_product_data = result.scalar_one()

    return new_product_data


async def product_fetch_service(skip:int, limit:int, category_id:int | None, min_price:int | None, max_price:int | None, search:str | None , sort_by:ProductSortFields | None, sort_order:SortOrder, db:AsyncSession):  
    stmt = (
        select(Product)
        .options(joinedload(Product.category))
        .where(Product.is_active == True, Product.is_deleted == False)
    )

    if category_id is not None:
        stmt = stmt.where(Product.category_id == category_id)
    
    if min_price is not None:
        stmt = stmt.where(Product.price >= min_price)

    if max_price is not None:
        stmt = stmt.where(Product.price <= max_price)

    if search:
        stmt = stmt.where(Product.name.ilike(f"%{search}%"))

    if sort_by:
        if hasattr(Product, sort_by.value):
            column = getattr(Product, sort_by.value)

            if sort_order == SortOrder.desc:
                stmt = stmt.order_by(column.desc())
            else:
                stmt = stmt.order_by(column.asc())

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total_result = await db.execute(count_stmt)
    total = total_result.scalar_one()

    stmt = stmt.offset(skip).limit(limit)

    
    result = await db.execute(stmt)
    product_data = result.scalars().all()

    products_response = []

    for product in product_data:
        rating_stmt = (
            select(
                func.avg(Review.rating),
                func.count(Review.id)
            )
            .where(Review.product_id == product.id)
        )
        
        rating_result = await db.execute(rating_stmt)
        average_rating, review_count = rating_result.one()

        product_response = ProductResponse.model_validate(product).model_copy(
            update={
                "average_rating": average_rating,
                "review_count": review_count,
            }
        )

        products_response.append(product_response)



    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": products_response
    }

async def get_single_product_service(product_id:int, db:AsyncSession):
    stmt = (
        select(Product)
        .options(joinedload(Product.category))
        .where(Product.id == product_id, Product.is_deleted == False)
    )
    result = await db.execute(stmt)
    single_product = result.scalar_one_or_none()

    if not single_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    return single_product

async def update_single_product_service(product_id:int, product:ProductUpdate, db:AsyncSession):
    stmt = (
        select(Product)
        .options(joinedload(Product.category))
        .where(Product.id == product_id, Product.is_deleted == False)
    )
    result = await db.execute(stmt)
    existing_product = result.scalar_one_or_none()

    if not existing_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    updated_product = product.model_dump(exclude_unset=True)

    if "category_id" in updated_product:
        category_stmt = select(Category).where(Category.id == updated_product["category_id"])
        category_result = await db.execute(category_stmt)
        exist_category = category_result.scalar_one_or_none()

        if not exist_category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category doesn't exist")
    
    
    for key, value in updated_product.items():
        setattr(existing_product, key, value)

    await db.commit()
    await db.refresh(existing_product)

    stmt = (
        select(Product)
        .options(joinedload(Product.category))
        .where(Product.id == product_id, Product.is_deleted == False)
    )
    result = await db.execute(stmt)
    final_data = result.scalar_one()

    return final_data

async def delete_product_service(product_id:int, db:AsyncSession):
    stmt = select(Product).where(Product.id == product_id, Product.is_deleted == False)
    result = await db.execute(stmt)
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")
    
    product.is_deleted = True

    await db.commit()

    return {
        "message": "Product deleted successfully"
    }