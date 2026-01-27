from sqlalchemy import Column, Integer, ForeignKey, String, Float, Table
from sqlalchemy.orm import relationship
from ..database.connection import Base

appointment_workers = Table(
    "appointment_workers",
    Base.metadata,
    Column("appointment_id", ForeignKey("appointments.id"), primary_key=True),
    Column("worker_id", ForeignKey("workers.id"), primary_key=True),
)

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    service_id = Column(Integer, ForeignKey("services.id"))
    status = Column(String, index=True)
    total_value = Column(Float)

    customer = relationship("Customer", back_populates="appointments")
    workers = relationship("Worker", secondary=appointment_workers, back_populates="appointments")
    vehicle = relationship("Vehicle", back_populates="appointments")
    service = relationship("Service", back_populates="appointments")
    stock_flows = relationship("StockFlow", back_populates="appointment")