from pydantic import BaseModel, ConfigDict
from typing import Optional


class MaterialBase(BaseModel):
	internal_code: str
	name: str
	category: Optional[str] = None

	market_avg_price: Optional[float] = None
	margin_percent: Optional[float] = None
	sale_price: Optional[float] = None

	stock_current: int = 0
	stock_minimum: int = 0
	active: bool = True


class MaterialCreate(MaterialBase):
	pass


class MaterialUpdate(BaseModel):
	internal_code: Optional[str] = None
	name: Optional[str] = None
	category: Optional[str] = None
	market_avg_price: Optional[float] = None
	margin_percent: Optional[float] = None
	sale_price: Optional[float] = None
	stock_current: Optional[int] = None
	stock_minimum: Optional[int] = None
	active: Optional[bool] = None


class Material(MaterialBase):
	id: int

	model_config = ConfigDict(from_attributes=True)


class ServiceMaterialLink(BaseModel):
	material_id: int
	quantity: int = 1


class VehicleServiceLink(BaseModel):
	service_id: int


class VehicleMaterialLink(BaseModel):
	material_id: int
