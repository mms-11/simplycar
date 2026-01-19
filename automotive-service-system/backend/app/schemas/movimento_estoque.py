from pydantic import BaseModel
from typing import Optional

class AppointmentBase(BaseModel):
    customer_id: int
    vehicle_id: int
    service_id: int
    status: str
    total_value: float

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(AppointmentBase):
    status: Optional[str] = None
    total_value: Optional[float] = None

class Appointment(AppointmentBase):
    id: int

    class Config:
        orm_mode = True