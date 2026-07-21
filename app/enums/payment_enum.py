from enum import Enum

class PaymentMethod(str, Enum):
    cash = "cash"
    upi = "upi"
    credit_card = "credit_card"
    debit_card = "debit_card"

class PaymentStatus(str, Enum):
    pending = "pending"
    success = "success"
    failed = "failed"
    refunded = "refunded"