from pydantic import BaseModel, Field
from typing import Optional

class VehicleBase(BaseModel):
    brand: str = Field(..., example="Toyota")
    model: str = Field(..., example="Camry")
    year: int = Field(..., ge=1886, le=2023, example=2020)  # Cars were invented in 1886
    engine: str = Field(..., example="2.5L I4")

class VehicleCreate(VehicleBase):
    pass

class VehicleUpdate(VehicleBase):
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    engine: Optional[str] = None

class VehicleInDB(VehicleBase):
    id: int

class Vehicle(VehicleInDB):
    pass