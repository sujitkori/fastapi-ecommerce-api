from app.database import Base
from sqlalchemy import Column, VARCHAR, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime,timezone


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    products = relationship("Product", back_populates="category")

