from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.enums import OrderStatus
from .order_item_schema import OrderItemResponse

class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_amount: int
    status: OrderStatus
    created_at: datetime | None
    updated_at: datetime | None
    order_items: list[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)

class OrderStatusUpdate(BaseModel):
    status: OrderStatus
