from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.enums import OrderStatus
from .order_item_schema import OrderItemResponse
from .user_schema import UserProfileResponse

class AdminOrderResponse(BaseModel):
    id: int
    user: UserProfileResponse
    total_amount: float
    status: OrderStatus
    created_at: datetime | None
    updated_at: datetime | None
    order_items: list[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)