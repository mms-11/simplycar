from sqlalchemy.orm import Session

from app.api.services._common import apply_partial_update, get_or_404
from app.models.stock_flow import StockFlow
from app.schemas.stock_flow import StockFlowCreate, StockFlowUpdate


def list_stock_flows(db: Session) -> list[StockFlow]:
    return db.query(StockFlow).all()


def create_stock_flow(db: Session, payload: StockFlowCreate) -> StockFlow:
    stock_flow = StockFlow(**payload.model_dump())
    db.add(stock_flow)
    db.commit()
    db.refresh(stock_flow)
    return stock_flow

def get_stock_flow(db: Session, stock_flow_id: int) -> StockFlow:
    return get_or_404(db, StockFlow, stock_flow_id, detail="Stock flow not found")

def update_stock_flow(db: Session, stock_flow_id: int, payload: StockFlowUpdate) -> StockFlow:
    stock_flow = get_or_404(db, StockFlow, stock_flow_id, detail="Stock flow not found")
    apply_partial_update(stock_flow, payload.model_dump(exclude_unset=True))
    db.add(stock_flow)
    db.commit()
    db.refresh(stock_flow)
    return stock_flow


def delete_stock_flow(db: Session, stock_flow_id: int) -> None:
    stock_flow = get_or_404(db, StockFlow, stock_flow_id, detail="Stock flow not found")
    db.delete(stock_flow)
    db.commit()