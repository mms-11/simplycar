<<<<<<< HEAD
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_database_session
from app.models.servico import Service
from app.schemas.servico import Service as ServiceSchema
from app.schemas.servico import ServiceCreate, ServiceUpdate

router = APIRouter()


@router.get("", response_model=list[ServiceSchema])
def list_services(db: Session = Depends(get_database_session)):
    return db.query(Service).all()


@router.post("", response_model=ServiceSchema, status_code=201)
def create_service(payload: ServiceCreate, db: Session = Depends(get_database_session)):
=======
from sqlalchemy.orm import Session

from app.api.services._common import apply_partial_update, get_or_404
from app.models.services import Service
from app.schemas.service import ServiceCreate, ServiceUpdate


def list_services(db: Session) -> list[Service]:
    return db.query(Service).all()


def create_service(db: Session, payload: ServiceCreate) -> Service:
>>>>>>> 272819deb90de0cd01e7ca9e6a81a927ae3f1a33
    service = Service(**payload.model_dump())
    db.add(service)
    db.commit()
    db.refresh(service)
    return service


<<<<<<< HEAD
@router.get("/{service_id}", response_model=ServiceSchema)
def get_service(service_id: int, db: Session = Depends(get_database_session)):
    service = db.get(Service, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service


@router.patch("/{service_id}", response_model=ServiceSchema)
def update_service(service_id: int, payload: ServiceUpdate, db: Session = Depends(get_database_session)):
    service = db.get(Service, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(service, key, value)

=======
def get_service(db: Session, service_id: int) -> Service:
    return get_or_404(db, Service, service_id, detail="Service not found")


def update_service(db: Session, service_id: int, payload: ServiceUpdate) -> Service:
    service = get_or_404(db, Service, service_id, detail="Service not found")
    apply_partial_update(service, payload.model_dump(exclude_unset=True))
>>>>>>> 272819deb90de0cd01e7ca9e6a81a927ae3f1a33
    db.add(service)
    db.commit()
    db.refresh(service)
    return service
<<<<<<< HEAD
=======


def delete_service(db: Session, service_id: int) -> None:
    service = get_or_404(db, Service, service_id, detail="Service not found")
    db.delete(service)
    db.commit()
>>>>>>> 272819deb90de0cd01e7ca9e6a81a927ae3f1a33
