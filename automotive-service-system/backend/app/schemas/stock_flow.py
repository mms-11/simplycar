from datetime import datetime

from pydantic import BaseModel, ConfigDict
from typing import Literal, Optional


class StockFlowBase(BaseModel):
    material_id: int
    appointment_id: Optional[int] = None
    flow_type: Literal["entry", "exit"]
    quantity: int
    origin: Literal["purchase", "service_use", "adjustment"]


class StockFlowCreate(StockFlowBase):
    pass


class StockFlowUpdate(BaseModel):
    material_id: Optional[int] = None
    appointment_id: Optional[int] = None
    flow_type: Optional[Literal["entry", "exit"]] = None
    quantity: Optional[int] = None
    origin: Optional[Literal["purchase", "service_use", "adjustment"]] = None


class StockFlow(StockFlowBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)