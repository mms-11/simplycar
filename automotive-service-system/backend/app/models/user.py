from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SqlEnum
from sqlalchemy.orm import relationship
from app.core.database import Base

class UserType(str, Enum):
    
    ADMIN = "admin"
    COMPANY = "company"
    WORKER = "worker"
    CUSTOMER = "customer"
    SUPLIER = "supplier"
    

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    type = Column(SqlEnum(UserType), nullable=False)

    worker = relationship("Worker", back_populates="user", uselist=False)
    customer = relationship("Customer", back_populates="user", uselist=False)
    supplier = relationship("Supplier", back_populates="user", uselist=False)
    company = relationship("Company", back_populates="user", uselist=False)
