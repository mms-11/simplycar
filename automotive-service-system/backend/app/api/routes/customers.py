from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_database_session
from app.api.services import customers_service
from app.schemas.customer import Customer as CustomerSchema
from app.schemas.customer import CustomerCreate, CustomerUpdate

router = APIRouter()


@router.get("", response_model=list[CustomerSchema])
def list_customers(db: Session = Depends(get_database_session)):
    return customers_service.list_customers(db)


@router.post("", response_model=CustomerSchema, status_code=201)
def create_customer(payload: CustomerCreate, db: Session = Depends(get_database_session)):
    return customers_service.create_customer(db, payload)


@router.get("/{customer_id}", response_model=CustomerSchema)
def get_customer(customer_id: int, db: Session = Depends(get_database_session)):
    return customers_service.get_customer(db, customer_id)


@router.patch("/{customer_id}", response_model=CustomerSchema)
def update_customer(
    customer_id: int,
    payload: CustomerUpdate,
    db: Session = Depends(get_database_session),
):
    return customers_service.update_customer(db, customer_id, payload)


@router.delete("/{customer_id}", status_code=204)
def delete_customer(customer_id: int, db: Session = Depends(get_database_session)):
    customers_service.delete_customer(db, customer_id)
    return None
