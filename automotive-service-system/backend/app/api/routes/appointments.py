from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_database_session
from app.api.services import appointments_service
from app.schemas.appointment import Appointment as AppointmentSchema
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate

router = APIRouter()


@router.get("", response_model=list[AppointmentSchema])
def list_appointments(db: Session = Depends(get_database_session)):
    return appointments_service.list_appointments(db)


@router.post("", response_model=AppointmentSchema, status_code=201)
def create_appointment(payload: AppointmentCreate, db: Session = Depends(get_database_session)):
    return appointments_service.create_appointment(db, payload)


@router.get("/{appointment_id}", response_model=AppointmentSchema)
def get_appointment(appointment_id: int, db: Session = Depends(get_database_session)):
    return appointments_service.get_appointment(db, appointment_id)


@router.patch("/{appointment_id}", response_model=AppointmentSchema)
def update_appointment(
    appointment_id: int,
    payload: AppointmentUpdate,
    db: Session = Depends(get_database_session),
):
    return appointments_service.update_appointment(db, appointment_id, payload)


@router.delete("/{appointment_id}", status_code=204)
def delete_appointment(appointment_id: int, db: Session = Depends(get_database_session)):
    appointments_service.delete_appointment(db, appointment_id)
    return None
