from pydantic import BaseModel
from datetime import datetime, date
from decimal import Decimal

class PaymentBase(BaseModel):
    amount: Decimal
    saving: Decimal
    housing: Decimal
    personal: Decimal
    concept: str
    payment_date: date

class PaymentCreate(PaymentBase):
    user_id: int

class PaymentEdit(PaymentBase):
    pass

class PaymentResponse(PaymentBase):
    payment_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True