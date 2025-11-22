from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from decimal import Decimal

class PaymentCreate(BaseModel):
    booking_id: UUID
    amount: Decimal
    method: str
    payer_name: Optional[str] = None

class PaymentOut(BaseModel):
    id: UUID
    booking_id: UUID
    amount: Decimal
    method: str
    status: str

    class Config:
        orm_mode = True