from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SqlEnum
from sqlalchemy.orm import relationship
from app.core.database import Base

class UserType(str, Enum):
    BASIC = "basic"
    ADMIN = "admin"
    COMPANY = "company"
    WORKER = "worker"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    type = Column(SqlEnum(UserType), default=UserType.BASIC, nullable=False)
