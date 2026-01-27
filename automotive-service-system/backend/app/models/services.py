from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from ..database.connection import Base
from .materials import ServiceMaterial, vehicle_services

class Service(Base):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    average_time = Column(Integer, nullable=False)  # in minutes
    labor_cost = Column(Float, nullable=False)  # in currency

    appointments = relationship("Appointment", back_populates="service")
    vehicles = relationship("Vehicle", secondary=vehicle_services, back_populates="services")
    service_materials = relationship("ServiceMaterial", back_populates="service", cascade="all, delete-orphan")