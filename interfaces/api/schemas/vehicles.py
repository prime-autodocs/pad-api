import datetime
from typing import Optional
from pydantic import BaseModel
from services.enums import FuelEnum, CategoryEnum

class VehiclesByCustomer(BaseModel):
  """Vehicles by customer"""
  id: int = None
  brand: str = None
  model: str = None
  number_plate: str = None
  customer_id: int = None
  customer_name: str = None
  tax_id: str = None
  last_legalization_year: int | None = None
  
  class Config:
    """Configs"""
    from_attributes = True

class VehicleCreate(BaseModel):
  """Create a vehicle"""
  customer_id: int = None
  brand: str = None
  model: str = None
  number_plate: str = None
  chassis: str = None
  national_registry: str = None
  year_fabric: str = None
  year_model: str = None
  fuel: FuelEnum = None
  color: str = None
  category: CategoryEnum = None
  certification_number: str = None
  crlv_image: str = None
  created_at: datetime.datetime = None
  updated_at: datetime.datetime = None
  updated_by: Optional[str] = None
  class Config:
    """Configs"""
    from_attributes = True
class VehicleUpdate(VehicleCreate):
  """Update a vehicle"""
  updated_by: str = None
  class Config:
    from_attributes = True