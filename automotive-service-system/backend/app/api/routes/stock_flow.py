from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_database_session
from app.models.stock_flow import Supplier

from app.schemas.stock_flow import StockFlow, stock_flow as StockFlowSchema
from app.schemas.stock_flow import StockFlowCreate, StockFlowUpdate
from backend.app.api.routes import supplier
from backend.app.schemas.supplier import SupplierUpdate

router = APIRouter()


@router.get("", response_model=list[StockFlowSchema])
def list_stock_flows(db: Session = Depends(get_database_session)):
    return db.query(StockFlow).all()


@router.post("", response_model=StockFlowSchema, status_code=201)
def create_stock_flow(payload: StockFlowCreate, db: Session = Depends(get_database_session)):
    stock_flow = StockFlow(**payload.model_dump())
    db.add(stock_flow)
    db.commit()
    db.refresh(stock_flow)
    return stock_flow


@router.get("/{stock_flow_id}", response_model=StockFlowSchema)
def get_stock_flow(stock_flow_id: int, db: Session = Depends(get_database_session)):
    stock_flow = db.get(StockFlow, stock_flow_id)
    if not stock_flow:
        raise HTTPException(status_code=404, detail="Stock flow not found")
    return stock_flow


@router.patch("/{stock_flow_id}", response_model=StockFlowSchema)
def update_stock_flow(
    stock_flow_id: int,
    payload: StockFlowUpdate,
    db: Session = Depends(get_database_session),
):
    stock_flow = db.get(StockFlow, stock_flow_id)
    if not stock_flow:
        raise HTTPException(status_code=404, detail="Stock flow not found")

    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(stock_flow, key, value)

    db.add(stock_flow)
    db.commit()
    db.refresh(stock_flow)
    return stock_flow
  #falta o delete

@router.delete("/{stock_flow_id}", status_code=204)
def delete_stock_flow(stock_flow_id: int, db: Session = Depends(get_database_session)):
    stock_flow = db.get(StockFlow, stock_flow_id)
    if not stock_flow:
        raise HTTPException(status_code=404, detail="Stock flow not found")

    db.delete(stock_flow)
    db.commit()
    return None