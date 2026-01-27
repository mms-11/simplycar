from pydantic import BaseModel, ConfigDict, EmailStr
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

    model_config = ConfigDict(from_attributes=True)