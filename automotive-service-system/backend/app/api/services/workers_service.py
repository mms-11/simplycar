from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.services._common import apply_partial_update, get_or_404
from app.models.workers import Worker
from app.schemas.workers import WorkerCreate, WorkerUpdate


def list_workers(db: Session) -> list[Worker]:
	return db.query(Worker).all()


def create_worker(db: Session, payload: WorkerCreate) -> Worker:
	worker = Worker(**payload.model_dump())
	db.add(worker)
	try:
		db.commit()
	except IntegrityError:
		db.rollback()
		raise HTTPException(status_code=409, detail="Worker conflict (email must be unique)")
	db.refresh(worker)
	return worker


def get_worker(db: Session, worker_id: int) -> Worker:
	return get_or_404(db, Worker, worker_id, detail="Worker not found")


def update_worker(db: Session, worker_id: int, payload: WorkerUpdate) -> Worker:
	worker = get_or_404(db, Worker, worker_id, detail="Worker not found")
	apply_partial_update(worker, payload.model_dump(exclude_unset=True))
	db.add(worker)
	try:
		db.commit()
	except IntegrityError:
		db.rollback()
		raise HTTPException(status_code=409, detail="Worker conflict (email must be unique)")
	db.refresh(worker)
	return worker


def delete_worker(db: Session, worker_id: int) -> None:
	worker = get_or_404(db, Worker, worker_id, detail="Worker not found")
	db.delete(worker)
	db.commit()
