from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_database_session
from app.models.workers import Worker
from app.schemas.workers import Workers as WorkerSchema
from app.schemas.workers import WorkerCreate, WorkerUpdate
from backend.app.schemas.vehicule import Vehicle, VehicleUpdate

router = APIRouter()


@router.get("", response_model=list[WorkerSchema])
def list_workers(db: Session = Depends(get_database_session)):
	return db.query(Worker ).all()


@router.post("", response_model=WorkerSchema, status_code=201)
def create_worker(payload: WorkerCreate, db: Session = Depends(get_database_session)):
	worker = Worker(**payload.model_dump())
	db.add(worker)
	db.commit()
	db.refresh(worker)
	return worker

@router.get("/{worker_id}", response_model=WorkerSchema)
def get_worker(worker_id: int, db: Session = Depends(get_database_session)):
	worker = db.get(Worker, worker_id)
	if not worker:
		raise HTTPException(status_code=404, detail="Worker not found")
	return worker


@router.patch("/{worker_id}", response_model=WorkerSchema)
def update_worker(worker_id: int, payload: WorkerUpdate, db: Session = Depends(get_database_session)):
	worker = db.get(Worker, worker_id)
	if not worker:
		raise HTTPException(status_code=404, detail="Worker not found")

	data = payload.model_dump(exclude_unset=True)
	for key, value in data.items():
		setattr(worker, key, value)
	db.add(worker)
	db.commit()
	db.refresh(worker)
	return worker

@router.delete("/{worker_id}", status_code=204)
def delete_worker(worker_id: int, db: Session = Depends(get_database_session)):
    worker = db.get(Worker, worker_id)
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    db.delete(worker)
    db.commit()
	
    return None 