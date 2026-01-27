from sqlalchemy.orm import Session

from app.api.services._common import apply_partial_update, get_or_404
from app.models.services import Service
from app.schemas.service import ServiceCreate, ServiceUpdate


def list_services(db: Session) -> list[Service]:
    return db.query(Service).all()


def create_service(db: Session, payload: ServiceCreate) -> Service:
    service = Service(**payload.model_dump())
    db.add(service)
    db.commit()
    db.refresh(service)
    return service


def get_service(db: Session, service_id: int) -> Service:
    return get_or_404(db, Service, service_id, detail="Service not found")


def update_service(db: Session, service_id: int, payload: ServiceUpdate) -> Service:
    service = get_or_404(db, Service, service_id, detail="Service not found")
    apply_partial_update(service, payload.model_dump(exclude_unset=True))
    db.add(service)
    db.commit()
    db.refresh(service)
    return service


def delete_service(db: Session, service_id: int) -> None:
    service = get_or_404(db, Service, service_id, detail="Service not found")
    db.delete(service)
    db.commit()
