from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_database_session
from app.api.services import stock_flow_service
from app.schemas.stock_flow import StockFlow as StockFlowSchema
from app.schemas.stock_flow import StockFlowCreate, StockFlowUpdate

router = APIRouter()


@router.get("", response_model=list[StockFlowSchema])
def list_stock_flows(db: Session = Depends(get_database_session)):
    return stock_flow_service.list_stock_flows(db)


@router.post("", response_model=StockFlowSchema, status_code=201)
def create_stock_flow(payload: StockFlowCreate, db: Session = Depends(get_database_session)):
    return stock_flow_service.create_stock_flow(db, payload)


@router.get("/{stock_flow_id}", response_model=StockFlowSchema)
def get_stock_flow(stock_flow_id: int, db: Session = Depends(get_database_session)):
    return stock_flow_service.get_stock_flow(db, stock_flow_id)


@router.patch("/{stock_flow_id}", response_model=StockFlowSchema)
def update_stock_flow(
    stock_flow_id: int,
    payload: StockFlowUpdate,
    db: Session = Depends(get_database_session),
):
    return stock_flow_service.update_stock_flow(db, stock_flow_id, payload)

@router.delete("/{stock_flow_id}", status_code=204)
def delete_stock_flow(stock_flow_id: int, db: Session = Depends(get_database_session)):
    stock_flow_service.delete_stock_flow(db, stock_flow_id)
    return None