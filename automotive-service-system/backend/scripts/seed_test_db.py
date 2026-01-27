"""Seed script for local/test database.

Usage (PowerShell):
  $env:DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/simplycar_teste"
    python ./scripts/seed_test_db.py
    python ./scripts/seed_test_db.py --reset

Notes:
- Uses the project's SQLAlchemy models.
- `--reset` drops and recreates all tables (DEV/TEST only).
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path


# Ensure `backend/` is on sys.path so `import app...` works.
BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


from sqlalchemy import select

from app.database.connection import Base, SessionLocal, engine, init_db
from app.models.appointments import Appointment, appointment_workers
from app.models.customers import Customer
from app.models.materials import Material, MaterialSupplier, ServiceMaterial
from app.models.services import Service
from app.models.stock_flow import StockFlow
from app.models.suppliers import Supplier
from app.models.vehicles import Vehicle
from app.models.workers import Worker


def get_or_create_supplier(session, *, name: str, phone: str | None, email: str | None) -> Supplier:
    supplier = session.scalar(select(Supplier).where(Supplier.name == name))
    if supplier:
        supplier.phone = phone
        supplier.email = email
        return supplier
    supplier = Supplier(name=name, phone=phone, email=email)
    session.add(supplier)
    return supplier


def get_or_create_customer(session, *, name: str, phone: str, email: str) -> Customer:
    customer = session.scalar(select(Customer).where(Customer.email == email))
    if customer:
        customer.name = name
        customer.phone = phone
        return customer
    customer = Customer(name=name, phone=phone, email=email)
    session.add(customer)
    return customer


def get_or_create_worker(session, *, name: str, phone: str, email: str, service_specialty: str | None) -> Worker:
    worker = session.scalar(select(Worker).where(Worker.email == email))
    if worker:
        worker.name = name
        worker.phone = phone
        worker.service_specialty = service_specialty
        return worker
    worker = Worker(name=name, phone=phone, email=email, service_specialty=service_specialty)
    session.add(worker)
    return worker


def get_or_create_vehicle(session, *, brand: str, model: str, year: int, engine_name: str) -> Vehicle:
    vehicle = session.scalar(
        select(Vehicle).where(
            Vehicle.brand == brand,
            Vehicle.model == model,
            Vehicle.year == year,
            Vehicle.engine == engine_name,
        )
    )
    if vehicle:
        return vehicle
    vehicle = Vehicle(brand=brand, model=model, year=year, engine=engine_name)
    session.add(vehicle)
    return vehicle


def get_or_create_material(
    session,
    *,
    internal_code: str,
    name: str,
    category: str | None,
    market_avg_price: float | None,
    margin_percent: float | None,
    stock_current: int,
    stock_minimum: int,
    active: bool = True,
) -> Material:
    material = session.scalar(select(Material).where(Material.internal_code == internal_code))
    sale_price: float | None = None
    if market_avg_price is not None and margin_percent is not None:
        sale_price = round(market_avg_price * (1.0 + margin_percent / 100.0), 2)

    if material:
        material.name = name
        material.category = category
        material.market_avg_price = market_avg_price
        material.margin_percent = margin_percent
        material.sale_price = sale_price
        material.stock_current = stock_current
        material.stock_minimum = stock_minimum
        material.active = active
        return material

    material = Material(
        internal_code=internal_code,
        name=name,
        category=category,
        market_avg_price=market_avg_price,
        margin_percent=margin_percent,
        sale_price=sale_price,
        stock_current=stock_current,
        stock_minimum=stock_minimum,
        active=active,
    )
    session.add(material)
    return material


def get_or_create_service(
    session,
    *,
    name: str,
    description: str | None,
    average_time: int,
    labor_cost: float,
) -> Service:
    # No unique constraint in DB; we treat `name` as natural key for seeding.
    service = session.scalar(select(Service).where(Service.name == name))
    if service:
        service.description = description
        service.average_time = average_time
        service.labor_cost = labor_cost
        return service
    service = Service(name=name, description=description, average_time=average_time, labor_cost=labor_cost)
    session.add(service)
    return service


def ensure_material_supplier(
    session,
    *,
    material: Material,
    supplier: Supplier,
    purchase_price: float,
    last_updated: datetime,
) -> None:
    assoc = session.get(MaterialSupplier, {"material_id": material.id, "supplier_id": supplier.id})
    if assoc:
        assoc.purchase_price = purchase_price
        assoc.last_updated = last_updated
        return
    session.add(
        MaterialSupplier(
            material_id=material.id,
            supplier_id=supplier.id,
            purchase_price=purchase_price,
            last_updated=last_updated,
        )
    )


def ensure_service_material(session, *, service: Service, material: Material, quantity: int) -> None:
    assoc = session.get(ServiceMaterial, {"service_id": service.id, "material_id": material.id})
    if assoc:
        assoc.quantity = quantity
        return
    session.add(ServiceMaterial(service_id=service.id, material_id=material.id, quantity=quantity))


def get_or_create_appointment(
    session,
    *,
    customer: Customer,
    vehicle: Vehicle,
    service: Service,
    status: str,
    total_value: float,
) -> Appointment:
    appointment = session.scalar(
        select(Appointment).where(
            Appointment.customer_id == customer.id,
            Appointment.vehicle_id == vehicle.id,
            Appointment.service_id == service.id,
            Appointment.status == status,
            Appointment.total_value == total_value,
        )
    )
    if appointment:
        return appointment
    appointment = Appointment(
        customer_id=customer.id,
        vehicle_id=vehicle.id,
        service_id=service.id,
        status=status,
        total_value=total_value,
    )
    session.add(appointment)
    return appointment


def ensure_appointment_worker(session, *, appointment: Appointment, worker: Worker) -> None:
    # Composite PK: (appointment_id, worker_id)
    exists = session.execute(
        select(appointment_workers.c.appointment_id).where(
            appointment_workers.c.appointment_id == appointment.id,
            appointment_workers.c.worker_id == worker.id,
        )
    ).first()
    if exists:
        return
    session.execute(
        appointment_workers.insert().values(appointment_id=appointment.id, worker_id=worker.id)
    )


def ensure_vehicle_service(vehicle: Vehicle, service: Service) -> None:
    if service not in vehicle.services:
        vehicle.services.append(service)


def ensure_vehicle_material(vehicle: Vehicle, material: Material) -> None:
    if material not in vehicle.materials:
        vehicle.materials.append(material)


def ensure_stock_flow(
    session,
    *,
    material: Material,
    appointment: Appointment | None,
    flow_type: str,
    quantity: int,
    origin: str,
    created_at: datetime,
) -> None:
    # Create with deterministic timestamp so we can keep it idempotent.
    appointment_id = appointment.id if appointment else None
    exists = session.scalar(
        select(StockFlow.id).where(
            StockFlow.material_id == material.id,
            StockFlow.appointment_id.is_(appointment_id) if appointment_id is None else StockFlow.appointment_id == appointment_id,
            StockFlow.flow_type == flow_type,
            StockFlow.quantity == quantity,
            StockFlow.origin == origin,
            StockFlow.created_at == created_at,
        )
    )
    if exists:
        return
    session.add(
        StockFlow(
            material_id=material.id,
            appointment_id=appointment_id,
            flow_type=flow_type,
            quantity=quantity,
            origin=origin,
            created_at=created_at,
        )
    )


def seed(*, reset: bool) -> None:
    if reset:
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
    else:
        init_db()

    now = datetime(2026, 1, 27, 12, 0, 0)

    session = SessionLocal()
    try:
        # Suppliers
        supplier_auto = get_or_create_supplier(
            session,
            name="AutoParts SA",
            phone="+55 11 4000-1000",
            email="contato@autoparts.example",
        )
        supplier_lub = get_or_create_supplier(
            session,
            name="MegaLub Distribuidora",
            phone="+55 11 4000-2000",
            email="vendas@megalub.example",
        )
        session.flush()

        # Materials
        oil = get_or_create_material(
            session,
            internal_code="OIL-5W30",
            name="Óleo 5W30 (1L)",
            category="Lubrificante",
            market_avg_price=35.0,
            margin_percent=40.0,
            stock_current=30,
            stock_minimum=5,
        )
        oil_filter = get_or_create_material(
            session,
            internal_code="FILTER-OIL",
            name="Filtro de Óleo",
            category="Filtro",
            market_avg_price=25.0,
            margin_percent=50.0,
            stock_current=20,
            stock_minimum=5,
        )
        brake_pad = get_or_create_material(
            session,
            internal_code="BRAKEPAD-FRONT",
            name="Pastilha de Freio Dianteira",
            category="Freio",
            market_avg_price=120.0,
            margin_percent=35.0,
            stock_current=10,
            stock_minimum=2,
        )
        session.flush()

        # Supplier prices
        ensure_material_supplier(session, material=oil, supplier=supplier_lub, purchase_price=22.0, last_updated=now)
        ensure_material_supplier(session, material=oil_filter, supplier=supplier_auto, purchase_price=15.0, last_updated=now)
        ensure_material_supplier(session, material=brake_pad, supplier=supplier_auto, purchase_price=75.0, last_updated=now)

        # Services
        oil_change = get_or_create_service(
            session,
            name="Troca de óleo",
            description="Troca de óleo e filtro",
            average_time=60,
            labor_cost=120.0,
        )
        brake_service = get_or_create_service(
            session,
            name="Troca de pastilhas de freio",
            description="Substituição de pastilhas dianteiras",
            average_time=90,
            labor_cost=180.0,
        )
        session.flush()

        # Service materials
        ensure_service_material(session, service=oil_change, material=oil, quantity=4)
        ensure_service_material(session, service=oil_change, material=oil_filter, quantity=1)
        ensure_service_material(session, service=brake_service, material=brake_pad, quantity=1)

        # Vehicles
        gol = get_or_create_vehicle(session, brand="Volkswagen", model="Gol", year=2015, engine_name="1.6")
        civic = get_or_create_vehicle(session, brand="Honda", model="Civic", year=2018, engine_name="2.0")
        session.flush()

        ensure_vehicle_service(gol, oil_change)
        ensure_vehicle_service(gol, brake_service)
        ensure_vehicle_service(civic, oil_change)

        ensure_vehicle_material(gol, oil)
        ensure_vehicle_material(gol, oil_filter)
        ensure_vehicle_material(gol, brake_pad)

        # Customers
        maria = get_or_create_customer(session, name="Maria Silva", phone="+55 11 99999-1111", email="maria@exemplo.com")
        joao = get_or_create_customer(session, name="João Souza", phone="+55 11 98888-2222", email="joao@exemplo.com")

        # Workers
        carlos = get_or_create_worker(
            session,
            name="Carlos Mecânico",
            phone="+55 11 97777-3333",
            email="carlos@oficina.com",
            service_specialty="Motor",
        )
        ana = get_or_create_worker(
            session,
            name="Ana Técnica",
            phone="+55 11 96666-4444",
            email="ana@oficina.com",
            service_specialty="Freios",
        )
        session.flush()

        # Appointments
        appt1 = get_or_create_appointment(
            session,
            customer=maria,
            vehicle=gol,
            service=oil_change,
            status="scheduled",
            total_value=260.0,
        )
        appt2 = get_or_create_appointment(
            session,
            customer=joao,
            vehicle=gol,
            service=brake_service,
            status="completed",
            total_value=340.0,
        )
        session.flush()

        ensure_appointment_worker(session, appointment=appt1, worker=carlos)
        ensure_appointment_worker(session, appointment=appt2, worker=ana)

        # Stock flows (entries and exits)
        ensure_stock_flow(session, material=oil, appointment=None, flow_type="entry", quantity=30, origin="purchase", created_at=now)
        ensure_stock_flow(session, material=oil_filter, appointment=None, flow_type="entry", quantity=20, origin="purchase", created_at=now)
        ensure_stock_flow(session, material=brake_pad, appointment=None, flow_type="entry", quantity=10, origin="purchase", created_at=now)

        # Consumption tied to appointment
        ensure_stock_flow(session, material=oil, appointment=appt1, flow_type="exit", quantity=4, origin="service_use", created_at=now)
        ensure_stock_flow(session, material=oil_filter, appointment=appt1, flow_type="exit", quantity=1, origin="service_use", created_at=now)
        ensure_stock_flow(session, material=brake_pad, appointment=appt2, flow_type="exit", quantity=1, origin="service_use", created_at=now)

        session.commit()
        print("Seed concluído com sucesso.")
    finally:
        session.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed test database")
    parser.add_argument("--reset", action="store_true", help="Drop and recreate all tables before seeding")
    args = parser.parse_args()

    seed(reset=args.reset)


if __name__ == "__main__":
    main()
