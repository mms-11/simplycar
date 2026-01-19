from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from ..database.connection import Base

class Service(Base):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    average_time = Column(Float, nullable=False)  # in hours
    labor_cost = Column(Float, nullable=False)  # in currency

    appointments = relationship("Appointment", back_populates="service")