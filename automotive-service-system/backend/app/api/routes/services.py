from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_database_session
from app.api.services import services_service
from app.schemas.service import Service as ServiceSchema
from app.schemas.service import ServiceCreate, ServiceUpdate

router = APIRouter()


@router.get("", response_model=list[ServiceSchema])
def list_services(db: Session = Depends(get_database_session)):
    return services_service.list_services(db)


@router.post("", response_model=ServiceSchema, status_code=201)
def create_service(payload: ServiceCreate, db: Session = Depends(get_database_session)):
    return services_service.create_service(db, payload)


@router.get("/{service_id}", response_model=ServiceSchema)
def get_service(service_id: int, db: Session = Depends(get_database_session)):
    return services_service.get_service(db, service_id)


@router.patch("/{service_id}", response_model=ServiceSchema)
def update_service(service_id: int, payload: ServiceUpdate, db: Session = Depends(get_database_session)):
    return services_service.update_service(db, service_id, payload)


@router.delete("/{service_id}", status_code=204)
def delete_service(service_id: int, db: Session = Depends(get_database_session)):
    services_service.delete_service(db, service_id)
    return None
