from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_database_session
from app.api.services import supplier_service
from app.schemas.supplier import Supplier as SupplierSchema
from app.schemas.supplier import SupplierCreate, SupplierUpdate

router = APIRouter()


@router.get("", response_model=list[SupplierSchema])
def list_suppliers(db: Session = Depends(get_database_session)):
    return supplier_service.list_suppliers(db)


@router.post("", response_model=SupplierSchema, status_code=201)
def create_supplier(payload: SupplierCreate, db: Session = Depends(get_database_session)):
    return supplier_service.create_supplier(db, payload)


@router.get("/{supplier_id}", response_model=SupplierSchema)
def get_supplier(supplier_id: int, db: Session = Depends(get_database_session)):
    return supplier_service.get_supplier(db, supplier_id)


@router.patch("/{supplier_id}", response_model=SupplierSchema)
def update_supplier(
    supplier_id: int,
    payload: SupplierUpdate,
    db: Session = Depends(get_database_session),
):
    return supplier_service.update_supplier(db, supplier_id, payload)


@router.delete("/{supplier_id}", status_code=204)
def delete_supplier(supplier_id: int, db: Session = Depends(get_database_session)):
    supplier_service.delete_supplier(db, supplier_id)
    return None