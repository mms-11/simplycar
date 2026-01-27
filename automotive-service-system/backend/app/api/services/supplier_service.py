from sqlalchemy.orm import Session

from app.api.services._common import apply_partial_update, get_or_404
from app.models.suppliers import Supplier
from app.schemas.supplier import SupplierCreate, SupplierUpdate


def list_suppliers(db: Session) -> list[Supplier]:
    return db.query(Supplier).all()


def create_supplier(db: Session, payload: SupplierCreate) -> Supplier:
    supplier = Supplier(**payload.model_dump())
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier


def get_supplier(db: Session, supplier_id: int) -> Supplier:
    return get_or_404(db, Supplier, supplier_id, detail="Supplier not found")


def update_supplier(db: Session, supplier_id: int, payload: SupplierUpdate) -> Supplier:
    supplier = get_or_404(db, Supplier, supplier_id, detail="Supplier not found")
    apply_partial_update(supplier, payload.model_dump(exclude_unset=True))
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier


def delete_supplier(db: Session, supplier_id: int) -> None:
    supplier = get_or_404(db, Supplier, supplier_id, detail="Supplier not found")
    db.delete(supplier)
    db.commit()