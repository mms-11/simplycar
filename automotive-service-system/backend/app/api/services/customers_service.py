from sqlalchemy.orm import Session

from app.api.services._common import apply_partial_update, get_or_404
from app.models.customers import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate


def list_customers(db: Session) -> list[Customer]:
    return db.query(Customer).all()


def create_customer(db: Session, payload: CustomerCreate) -> Customer:
    customer = Customer(**payload.model_dump())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def get_customer(db: Session, customer_id: int) -> Customer:
    return get_or_404(db, Customer, customer_id, detail="Customer not found")


def update_customer(db: Session, customer_id: int, payload: CustomerUpdate) -> Customer:
    customer = get_or_404(db, Customer, customer_id, detail="Customer not found")
    apply_partial_update(customer, payload.model_dump(exclude_unset=True))
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def delete_customer(db: Session, customer_id: int) -> None:
    customer = get_or_404(db, Customer, customer_id, detail="Customer not found")
    db.delete(customer)
    db.commit()
