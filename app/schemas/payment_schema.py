from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.enums import PaymentMethod, PaymentStatus

class CreatePayment(BaseModel):
    payment_method: PaymentMethod

class PaymentResponse(BaseModel):
    id:int
    order_id:int
    amount: int
    payment_method:PaymentMethod
    payment_status: PaymentStatus
    transaction_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PaymentStatusUpdate(BaseModel):
    payment_status_update: PaymentStatus