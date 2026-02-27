from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_database_session
from app.api.services import vehicles_service
from app.schemas.vehicule import Vehicle as VehicleSchema
from app.schemas.vehicule import VehicleCreate, VehicleUpdate

router = APIRouter()


@router.get("", response_model=list[VehicleSchema])
def list_vehicles(db: Session = Depends(get_database_session)):
	return vehicles_service.list_vehicles(db)


@router.post("", response_model=VehicleSchema, status_code=201)
def create_vehicle(payload: VehicleCreate, db: Session = Depends(get_database_session)):
	return vehicles_service.create_vehicle(db, payload)


@router.get("/{vehicle_id}", response_model=VehicleSchema)
def get_vehicle(vehicle_id: int, db: Session = Depends(get_database_session)):
	return vehicles_service.get_vehicle(db, vehicle_id)


@router.patch("/{vehicle_id}", response_model=VehicleSchema)
def update_vehicle(vehicle_id: int, payload: VehicleUpdate, db: Session = Depends(get_database_session)):
	return vehicles_service.update_vehicle(db, vehicle_id, payload)


@router.delete("/{vehicle_id}", status_code=204)
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_database_session)):
	vehicles_service.delete_vehicle(db, vehicle_id)
	return None
