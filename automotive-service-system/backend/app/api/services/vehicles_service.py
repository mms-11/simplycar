from sqlalchemy.orm import Session

from app.api.services._common import apply_partial_update, get_or_404
from app.models.vehicles import Vehicle
from app.schemas.vehicule import VehicleCreate, VehicleUpdate


def list_vehicles(db: Session) -> list[Vehicle]:
	return db.query(Vehicle).all()


def create_vehicle(db: Session, payload: VehicleCreate) -> Vehicle:
	vehicle = Vehicle(**payload.model_dump())
	db.add(vehicle)
	db.commit()
	db.refresh(vehicle)
	return vehicle


def get_vehicle(db: Session, vehicle_id: int) -> Vehicle:
	return get_or_404(db, Vehicle, vehicle_id, detail="Vehicle not found")


def update_vehicle(db: Session, vehicle_id: int, payload: VehicleUpdate) -> Vehicle:
	vehicle = get_or_404(db, Vehicle, vehicle_id, detail="Vehicle not found")
	apply_partial_update(vehicle, payload.model_dump(exclude_unset=True))
	db.add(vehicle)
	db.commit()
	db.refresh(vehicle)
	return vehicle


def delete_vehicle(db: Session, vehicle_id: int) -> None:
	vehicle = get_or_404(db, Vehicle, vehicle_id, detail="Vehicle not found")
	db.delete(vehicle)
	db.commit()
