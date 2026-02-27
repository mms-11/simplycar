from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PaymentBase(BaseModel):
    service_id: int
    value: float
    comission: Optional[float] = None
    paid_at: Optional[datetime] = None

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    value: Optional[float] = None
    comission: Optional[float] = None
    paid_at: Optional[datetime] = None

class PaymentRead(PaymentBase):
    id: int
    class Config:
        orm_mode = True
