from __future__ import annotations

from sqlalchemy.orm import Session

from app.api.services._common import apply_partial_update, get_or_404
from app.models.appointments import Appointment
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate


def list_appointments(db: Session) -> list[Appointment]:
    return db.query(Appointment).all()


def create_appointment(db: Session, payload: AppointmentCreate) -> Appointment:
    appointment = Appointment(**payload.model_dump())
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


def get_appointment(db: Session, appointment_id: int) -> Appointment:
    return get_or_404(db, Appointment, appointment_id, detail="Appointment not found")


def update_appointment(db: Session, appointment_id: int, payload: AppointmentUpdate) -> Appointment:
    appointment = get_or_404(db, Appointment, appointment_id, detail="Appointment not found")
    apply_partial_update(appointment, payload.model_dump(exclude_unset=True))
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


def delete_appointment(db: Session, appointment_id: int) -> None:
    appointment = get_or_404(db, Appointment, appointment_id, detail="Appointment not found")
    db.delete(appointment)
    db.commit()
