from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_database_session
from app.models.services import Service
from app.schemas.servico import Service as ServiceSchema
from app.schemas.servico import ServiceCreate, ServiceUpdate

router = APIRouter()


@router.get("", response_model=list[ServiceSchema])
def list_services(db: Session = Depends(get_database_session)):
    return db.query(Service).all()


@router.post("", response_model=ServiceSchema, status_code=201)
def create_service(payload: ServiceCreate, db: Session = Depends(get_database_session)):
    service = Service(**payload.model_dump())
    db.add(service)
    db.commit()
    db.refresh(service)
    return service


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

    db.add(service)
    db.commit()
    db.refresh(service)
    return service
