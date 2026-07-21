from app.database import Base
from sqlalchemy import (Integer, Column, VARCHAR, Boolean, ForeignKey, DateTime)
from sqlalchemy.orm import relationship
from datetime import datetime, timezone 

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(255), unique=True, nullable=False)
    description = Column(VARCHAR(255), nullable=False)
    price = Column(Integer, nullable=False)
    stock_quantity = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, nullable=False, default=False)
    image = Column(VARCHAR(255), nullable=True)
    created_at = Column(DateTime, default=lambda:datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda:datetime.now(timezone.utc), onupdate=lambda:datetime.now(timezone.utc))
    category = relationship("Category", back_populates="products")
    cart_items = relationship("CartItem", back_populates="product")
    order_items = relationship("OrderItems", back_populates="product")
    reviews = relationship("Review", back_populates="product", cascade="all, delete-orphan")

