from pydantic import BaseModel, EmailStr
from typing import Optional

class CompanyBase(BaseModel):
    name: str
    cnpj: str
    email: EmailStr
    type: Optional[str] = None
    user_id: Optional[int] = None

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    cnpj: Optional[str] = None
    email: Optional[EmailStr] = None
    type: Optional[str] = None
    user_id: Optional[int] = None

class CompanyRead(CompanyBase):
    id: int
    class Config:
        orm_mode = True
