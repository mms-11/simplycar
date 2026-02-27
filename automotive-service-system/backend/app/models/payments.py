from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database.connection import Base

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=False)
    value = Column(Float, nullable=False)
    comission = Column(Float, nullable=True)
    paid_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    service = relationship("Service", back_populates="payments")
