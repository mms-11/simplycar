from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional


class SupplierBase(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None


class Supplier(SupplierBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
