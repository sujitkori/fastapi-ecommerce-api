from app.database import Base
from sqlalchemy import Column, Integer, ForeignKey, VARCHAR, DateTime, UniqueConstraint
from datetime import datetime, timezone
from sqlalchemy.orm import relationship

class Review(Base):
    __tablename__ = "reviews"

    __table_args__ = (
        UniqueConstraint(
            "user_id", 
            "product_id",
            name="uq_user_product_review",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"),nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(VARCHAR(1000), nullable=False)
    created_at = Column(DateTime, default=lambda:datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda:datetime.now(timezone.utc), onupdate=lambda:datetime.now(timezone.utc))
    user = relationship("User", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")