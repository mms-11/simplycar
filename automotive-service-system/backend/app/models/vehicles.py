from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database.connection import Base
from .materials import vehicle_materials, vehicle_services

class Vehicle(Base):
    __tablename__ = 'vehicles'

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, index=True)
    model = Column(String, index=True)
    year = Column(Integer)
    engine = Column(String)

    appointments = relationship("Appointment", back_populates="vehicle")
    services = relationship("Service", secondary=vehicle_services, back_populates="vehicles")
    materials = relationship("Material", secondary=vehicle_materials, back_populates="vehicles")