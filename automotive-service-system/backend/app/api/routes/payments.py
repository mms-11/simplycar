from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.payments import Payment
from app.schemas.payment import PaymentCreate, PaymentRead, PaymentUpdate
from app.api.dependencies import get_database_session

router = APIRouter()

@router.get("", response_model=list[PaymentRead])
def list_payments(db: Session = Depends(get_database_session)):
    return db.query(Payment).all()

@router.post("", response_model=PaymentRead, status_code=201)
def create_payment(payload: PaymentCreate, db: Session = Depends(get_database_session)):
    payment = Payment(**payload.dict())
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment

@router.get("/{payment_id}", response_model=PaymentRead)
def get_payment(payment_id: int, db: Session = Depends(get_database_session)):
    payment = db.query(Payment).get(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@router.patch("/{payment_id}", response_model=PaymentRead)
def update_payment(payment_id: int, payload: PaymentUpdate, db: Session = Depends(get_database_session)):
    payment = db.query(Payment).get(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(payment, key, value)
    db.commit()
    db.refresh(payment)
    return payment

@router.delete("/{payment_id}", status_code=204)
def delete_payment(payment_id: int, db: Session = Depends(get_database_session)):
    payment = db.query(Payment).get(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    db.delete(payment)
    db.commit()
    return None
