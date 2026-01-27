from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_database_session
from app.models.appointments import Appointment
from app.schemas.ordem_servico import Appointment as AppointmentSchema
from app.schemas.ordem_servico import AppointmentCreate, AppointmentUpdate

router = APIRouter()


@router.get("", response_model=list[AppointmentSchema])
def list_appointments(db: Session = Depends(get_database_session)):
    return db.query(Appointment).all()


@router.post("", response_model=AppointmentSchema, status_code=201)
def create_appointment(payload: AppointmentCreate, db: Session = Depends(get_database_session)):
    appointment = Appointment(**payload.model_dump())
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


@router.get("/{appointment_id}", response_model=AppointmentSchema)
def get_appointment(appointment_id: int, db: Session = Depends(get_database_session)):
    appointment = db.get(Appointment, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment


@router.patch("/{appointment_id}", response_model=AppointmentSchema)
def update_appointment(
    appointment_id: int,
    payload: AppointmentUpdate,
    db: Session = Depends(get_database_session),
):
    appointment = db.get(Appointment, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(appointment, key, value)

    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment
