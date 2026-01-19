from sqlalchemy import Column, Integer, ForeignKey, String, Float
from sqlalchemy.orm import relationship
from ..database.connection import Base

class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'))
    service_id = Column(Integer, ForeignKey('services.id'))
    status = Column(String, index=True)
    total_value = Column(Float)

    customer = relationship("Customer", back_populates="appointments")
    vehicle = relationship("Vehicle", back_populates="appointments")
    service = relationship("Service", back_populates="appointments")