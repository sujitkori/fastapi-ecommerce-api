from app.database import Base
from sqlalchemy import (Integer, Column, VARCHAR, Boolean, ForeignKey, DateTime, Enum)
from sqlalchemy.orm import relationship
from datetime import datetime, timezone 
from app.enums import OrderStatus

class Orders(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_amount = Column(Integer, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.pending, nullable=False)
    created_at = Column(DateTime, default=lambda:datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda:datetime.now(timezone.utc), onupdate=lambda:datetime.now(timezone.utc))
    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItems", back_populates="order")
    payment = relationship("Payment", back_populates="order", uselist=False)