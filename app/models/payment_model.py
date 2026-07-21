from app.database import Base
from sqlalchemy import (Integer, Column, VARCHAR, Enum, ForeignKey, DateTime)
from sqlalchemy.orm import relationship
from datetime import datetime, timezone 
from app.enums import PaymentMethod, PaymentStatus

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), unique=True, nullable=False)
    amount = Column(Integer, nullable=False)
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.pending, nullable=False)
    transaction_id = Column(VARCHAR(255), nullable=False, unique=True)
    created_at = Column(DateTime, default=lambda:datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda:datetime.now(timezone.utc), onupdate=lambda:datetime.now(timezone.utc))
    order = relationship("Orders", back_populates="payment")