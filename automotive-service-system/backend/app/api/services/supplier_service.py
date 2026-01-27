from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_database_session
from app.models.suppliers import Supplier
from app.schemas.supplier import Supplier as SupplierSchema
from app.schemas.supplier import SupplierCreate, SupplierUpdate

router = APIRouter()


@router.get("", response_model=list[SupplierSchema])
def list_suppliers(db: Session = Depends(get_database_session)):
    return db.query(Supplier).all()


@router.post("", response_model=SupplierSchema, status_code=201)
def create_supplier(payload: SupplierCreate, db: Session = Depends(get_database_session)):
    supplier = Supplier(**payload.model_dump())
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier


@router.get("/{supplier_id}", response_model=SupplierSchema)
def get_supplier(supplier_id: int, db: Session = Depends(get_database_session)):
    supplier = db.get(Supplier, supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier


@router.patch("/{supplier_id}", response_model=SupplierSchema)
def update_supplier(
    supplier_id: int,
    payload: SupplierUpdate,
    db: Session = Depends(get_database_session),
):
    supplier = db.get(Supplier, supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")

    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(supplier, key, value)

    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier


@router.delete("/{supplier_id}", status_code=204)
def delete_supplier(supplier_id: int, db: Session = Depends(get_database_session)):
    supplier = db.get(Supplier, supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")

    db.delete(supplier)
    db.commit()
    return None