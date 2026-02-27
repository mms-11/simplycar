from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional

class CustomerBase(BaseModel):
    name: str
    phone: str
    email: EmailStr
    user_id: Optional[int] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    user_id: Optional[int] = None

class CustomerRead(CustomerBase):
    id: int
    class Config:
        orm_mode = True