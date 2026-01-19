from pydantic import BaseModel, EmailStr
from typing import Optional

class CustomerBase(BaseModel):
    name: str
    phone: str
    email: EmailStr

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None

class Customer(CustomerBase):
    id: int

    class Config:
        orm_mode = True