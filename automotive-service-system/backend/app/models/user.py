from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database.connection import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    login = Column(String, index=True)
    password = Column(String, index=True)
    phone = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    type = Column(String, index=True)   

    