from pydantic import BaseModel, ConfigDict
from app.schemas.product_schema import ProductResponse

class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price_at_purchase: int
    product:ProductResponse

    model_config = ConfigDict(from_attributes=True)