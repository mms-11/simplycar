from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database.connection import Base

class Company(Base):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    cnpj = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    type = Column(String, index=True)   

    