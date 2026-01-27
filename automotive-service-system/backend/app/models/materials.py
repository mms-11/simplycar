from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Table, UniqueConstraint
from sqlalchemy.orm import relationship

from ..database.connection import Base


vehicle_services = Table(
	"vehicle_services",
	Base.metadata,
	Column("vehicle_id", ForeignKey("vehicles.id"), primary_key=True),
	Column("service_id", ForeignKey("services.id"), primary_key=True),
)


vehicle_materials = Table(
	"vehicle_materials",
	Base.metadata,
	Column("vehicle_id", ForeignKey("vehicles.id"), primary_key=True),
	Column("material_id", ForeignKey("materials.id"), primary_key=True),
)


class ServiceMaterial(Base):
	__tablename__ = "service_materials"

	service_id = Column(Integer, ForeignKey("services.id"), primary_key=True)
	material_id = Column(Integer, ForeignKey("materials.id"), primary_key=True)
	quantity = Column(Integer, nullable=False, default=1)

	service = relationship("Service", back_populates="service_materials")
	material = relationship("Material", back_populates="service_materials")


class MaterialSupplier(Base):
	__tablename__ = "material_suppliers"

	material_id = Column(Integer, ForeignKey("materials.id"), primary_key=True)
	supplier_id = Column(Integer, ForeignKey("suppliers.id"), primary_key=True)
	purchase_price = Column(Float, nullable=False)
	last_updated = Column(DateTime, nullable=False, default=datetime.utcnow)

	material = relationship("Material", back_populates="material_suppliers")
	supplier = relationship("Supplier", back_populates="material_suppliers")


class Material(Base):
	__tablename__ = "materials"
	__table_args__ = (UniqueConstraint("internal_code", name="uq_material_internal_code"),)

	id = Column(Integer, primary_key=True, index=True)
	internal_code = Column(String, nullable=False, index=True)
	name = Column(String, nullable=False, index=True)
	category = Column(String, nullable=True, index=True)

	market_avg_price = Column(Float, nullable=True)
	margin_percent = Column(Float, nullable=True)
	sale_price = Column(Float, nullable=True)

	stock_current = Column(Integer, nullable=False, default=0)
	stock_minimum = Column(Integer, nullable=False, default=0)
	active = Column(Boolean, nullable=False, default=True)

	service_materials = relationship("ServiceMaterial", back_populates="material", cascade="all, delete-orphan")
	stock_flows = relationship("StockFlow", back_populates="material", cascade="all, delete-orphan")
	vehicles = relationship("Vehicle", secondary=vehicle_materials, back_populates="materials")
	material_suppliers = relationship("MaterialSupplier", back_populates="material", cascade="all, delete-orphan")
