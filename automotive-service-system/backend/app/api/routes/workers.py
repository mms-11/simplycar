from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_database_session
from app.api.services import workers_service
from app.schemas.workers import Worker as WorkerSchema
from app.schemas.workers import WorkerCreate, WorkerUpdate

router = APIRouter()


@router.get("", response_model=list[WorkerSchema])
def list_workers(db: Session = Depends(get_database_session)):
	return workers_service.list_workers(db)


@router.post("", response_model=WorkerSchema, status_code=201)
def create_worker(payload: WorkerCreate, db: Session = Depends(get_database_session)):
	return workers_service.create_worker(db, payload)

@router.get("/{worker_id}", response_model=WorkerSchema)
def get_worker(worker_id: int, db: Session = Depends(get_database_session)):
	return workers_service.get_worker(db, worker_id)


@router.patch("/{worker_id}", response_model=WorkerSchema)
def update_worker(worker_id: int, payload: WorkerUpdate, db: Session = Depends(get_database_session)):
	return workers_service.update_worker(db, worker_id, payload)

@router.delete("/{worker_id}", status_code=204)
def delete_worker(worker_id: int, db: Session = Depends(get_database_session)):
	workers_service.delete_worker(db, worker_id)
	return None