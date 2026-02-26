from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.services._common import apply_partial_update, get_or_404
from app.models.materials import Material
from app.schemas.material import MaterialCreate, MaterialUpdate


def list_materials(db: Session) -> list[Material]:
	return db.query(Material).all()


def create_material(db: Session, payload: MaterialCreate) -> Material:
	material = Material(**payload.model_dump())
	db.add(material)
	try:
		db.commit()
	except IntegrityError:
		db.rollback()
		raise HTTPException(status_code=409, detail="Material conflict (internal_code must be unique)")
	db.refresh(material)
	return material


def get_material(db: Session, material_id: int) -> Material:
	return get_or_404(db, Material, material_id, detail="Material not found")


def update_material(db: Session, material_id: int, payload: MaterialUpdate) -> Material:
	material = get_or_404(db, Material, material_id, detail="Material not found")
	apply_partial_update(material, payload.model_dump(exclude_unset=True))
	db.add(material)
	try:
		db.commit()
	except IntegrityError:
		db.rollback()
		raise HTTPException(status_code=409, detail="Material conflict (internal_code must be unique)")
	db.refresh(material)
	return material


def delete_material(db: Session, material_id: int) -> None:
	material = get_or_404(db, Material, material_id, detail="Material not found")
	db.delete(material)
	db.commit()