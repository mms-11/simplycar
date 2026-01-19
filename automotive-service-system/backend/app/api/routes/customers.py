from fastapi import APIRouter, HTTPException
from typing import List
from ..models.customer import Customer
from ..schemas.customer import CustomerCreate, CustomerUpdate

router = APIRouter()

@router.post("/", response_model=Customer)
async def create_customer(customer: CustomerCreate):
    new_customer = Customer(**customer.dict())
    await new_customer.save()
    return new_customer

@router.get("/", response_model=List[Customer])
async def get_customers():
    return await Customer.all()

@router.get("/{customer_id}", response_model=Customer)
async def get_customer(customer_id: int):
    customer = await Customer.get(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.put("/{customer_id}", response_model=Customer)
async def update_customer(customer_id: int, customer: CustomerUpdate):
    existing_customer = await Customer.get(customer_id)
    if not existing_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    for key, value in customer.dict(exclude_unset=True).items():
        setattr(existing_customer, key, value)
    await existing_customer.save()
    return existing_customer

@router.delete("/{customer_id}", response_model=dict)
async def delete_customer(customer_id: int):
    customer = await Customer.get(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    await customer.delete()
    return {"message": "Customer deleted successfully"}