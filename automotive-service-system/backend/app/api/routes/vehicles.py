from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_database_session
from app.models.vehicles import Vehicle
from app.schemas.vehicule import Vehicle as VehicleSchema
from app.schemas.vehicule import VehicleCreate, VehicleUpdate

router = APIRouter()


@router.get("", response_model=list[VehicleSchema])
def list_vehicles(db: Session = Depends(get_database_session)):
	return db.query(Vehicle).all()


@router.post("", response_model=VehicleSchema, status_code=201)
def create_vehicle(payload: VehicleCreate, db: Session = Depends(get_database_session)):
	vehicle = Vehicle(**payload.model_dump())
	db.add(vehicle)
	db.commit()
	db.refresh(vehicle)
	return vehicle


@router.get("/{vehicle_id}", response_model=VehicleSchema)
def get_vehicle(vehicle_id: int, db: Session = Depends(get_database_session)):
	vehicle = db.get(Vehicle, vehicle_id)
	if not vehicle:
		raise HTTPException(status_code=404, detail="Vehicle not found")
	return vehicle


@router.patch("/{vehicle_id}", response_model=VehicleSchema)
def update_vehicle(vehicle_id: int, payload: VehicleUpdate, db: Session = Depends(get_database_session)):
	vehicle = db.get(Vehicle, vehicle_id)
	if not vehicle:
		raise HTTPException(status_code=404, detail="Vehicle not found")

	data = payload.model_dump(exclude_unset=True)
	for key, value in data.items():
		setattr(vehicle, key, value)

	db.add(vehicle)
	db.commit()
	db.refresh(vehicle)
	return vehicle
