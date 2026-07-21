from app.database import Base
from sqlalchemy import (Integer, Column, VARCHAR, Boolean, ForeignKey, DateTime)
from sqlalchemy.orm import relationship
from datetime import datetime, timezone 

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=lambda:datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda:datetime.now(timezone.utc), onupdate=lambda:datetime.now(timezone.utc))
    user = relationship("User", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")

