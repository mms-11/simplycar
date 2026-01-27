from pydantic import BaseModel, ConfigDict
from typing import Optional

class ServiceBase(BaseModel):
    name: str
    description: Optional[str] = None
    average_time: int  # in minutes
    labor_cost: float

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    average_time: Optional[int] = None  # in minutes
    labor_cost: Optional[float] = None

class Service(ServiceBase):
    id: int

    model_config = ConfigDict(from_attributes=True)