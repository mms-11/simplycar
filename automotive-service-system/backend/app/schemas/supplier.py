from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional


class SupplierBase(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    user_id: Optional[int] = None

class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    user_id: Optional[int] = None

class SupplierRead(SupplierBase):
    id: int
    class Config:
        orm_mode = True
