from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional


class WorkerBase(BaseModel):
	name: str
	phone: str
	email: EmailStr
	service_specialty: Optional[str] = None


class WorkerCreate(WorkerBase):
	pass


class WorkerUpdate(BaseModel):
	name: Optional[str] = None
	phone: Optional[str] = None
	email: Optional[EmailStr] = None
	service_specialty: Optional[str] = None


class Worker(WorkerBase):
	id: int

	model_config = ConfigDict(from_attributes=True)
