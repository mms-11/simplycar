from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional

class UserType(str, Enum):
    ADMIN = "admin"
    COMPANY = "company"
    WORKER = "worker"
    CUSTOMER = "customer"
    SUPLIER = "supplier"

class UserBase(BaseModel):
    login: str
    email: EmailStr
    type: UserType

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    login: Optional[str] = None
    email: Optional[EmailStr] = None
    type: Optional[UserType] = None
    password: Optional[str] = None

class UserRead(UserBase):
    id: int
    class Config:
        orm_mode = True
