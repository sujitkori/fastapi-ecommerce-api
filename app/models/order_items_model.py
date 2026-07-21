from app.database import Base
from sqlalchemy import (Integer, Column, VARCHAR, Boolean, ForeignKey, DateTime)
from sqlalchemy.orm import relationship
from datetime import datetime, timezone 

class OrderItems(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_at_purchase = Column(Integer, nullable=False)
    order = relationship("Orders", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")