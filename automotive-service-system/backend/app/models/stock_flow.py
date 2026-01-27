from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database.connection import Base


class StockFlow(Base):
	__tablename__ = "stock_flows"

	id = Column(Integer, primary_key=True, index=True)
	material_id = Column(Integer, ForeignKey("materials.id"), nullable=False, index=True)
	appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=True, index=True)

	flow_type = Column(String, nullable=False, index=True)  # 'entry' | 'exit'
	quantity = Column(Integer, nullable=False)
	origin = Column(String, nullable=False, index=True)  # 'purchase' | 'service_use' | 'adjustment'
	created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)

	material = relationship("Material", back_populates="stock_flows")
	appointment = relationship("Appointment", back_populates="stock_flows")

