from pydantic import BaseModel, EmailStr
from enum import Enum

class UserType(str, Enum):
    BASIC = "basic"
    ADMIN = "admin"
    COMPANY = "company"

class UserBase(BaseModel):
    login: str
    email: EmailStr
    type: UserType

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True
