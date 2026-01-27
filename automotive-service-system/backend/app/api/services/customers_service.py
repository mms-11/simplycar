from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_database_session
from app.models.cliente import Customer
from app.schemas.cliente import Customer as CustomerSchema
from app.schemas.cliente import CustomerCreate, CustomerUpdate

router = APIRouter()


@router.get("", response_model=list[CustomerSchema])
def list_customers(db: Session = Depends(get_database_session)):
    return db.query(Customer).all()


@router.post("", response_model=CustomerSchema, status_code=201)
def create_customer(payload: CustomerCreate, db: Session = Depends(get_database_session)):
    customer = Customer(**payload.model_dump())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


@router.get("/{customer_id}", response_model=CustomerSchema)
def get_customer(customer_id: int, db: Session = Depends(get_database_session)):
    customer = db.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.patch("/{customer_id}", response_model=CustomerSchema)
def update_customer(
    customer_id: int,
    payload: CustomerUpdate,
    db: Session = Depends(get_database_session),
):
    customer = db.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(customer, key, value)

    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer
