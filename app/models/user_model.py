from sqlalchemy import Column, VARCHAR, Integer, DateTime
from datetime import datetime,timezone
from app.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index = True)
    name = Column(VARCHAR(255), nullable = False)
    email = Column(VARCHAR(255), unique=True, nullable = False)
    password = Column(VARCHAR(255), nullable=False)
    role = Column(VARCHAR(50), nullable=False, default="user")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    cart_items = relationship("CartItem", back_populates="user")
    orders = relationship("Orders", back_populates="user")
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")