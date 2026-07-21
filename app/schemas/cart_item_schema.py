from pydantic import BaseModel, ConfigDict
from datetime import datetime
from .product_schema import ProductResponse

class CartItemCreate(BaseModel):
    product_id:int
    quantity:int

class CartItemResponse(BaseModel):
    id:int
    user_id:int
    product_id:int
    quantity:int
    product:ProductResponse | None
    created_at: datetime | None
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)

class CartItemUpdate(BaseModel):
    quantity: int