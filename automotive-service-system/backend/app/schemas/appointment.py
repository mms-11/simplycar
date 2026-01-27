from pydantic import BaseModel, ConfigDict
from typing import Optional


class AppointmentBase(BaseModel):
	customer_id: int
	vehicle_id: int
	service_id: int
	status: str
	total_value: float


class AppointmentCreate(AppointmentBase):
	pass


class AppointmentUpdate(BaseModel):
	customer_id: Optional[int] = None
	vehicle_id: Optional[int] = None
	service_id: Optional[int] = None
	status: Optional[str] = None
	total_value: Optional[float] = None


class Appointment(AppointmentBase):
	id: int

	model_config = ConfigDict(from_attributes=True)
