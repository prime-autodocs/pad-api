import datetime
from typing import Optional
from pydantic import BaseModel
from services.enums import FuelEnum, CategoryEnum

class VehiclesByCustomer(BaseModel):
    id: int = None
    brand: str = None
    model: str = None
    number_plate: str = None
    
    class Config:
      """Configs"""
      from_attributes = True
      
class VehicleDetail(BaseModel):
    id: int = None
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
      
class VehicleCreate(BaseModel):
    customer_id: int = None
    brand: str = None
    model: str = None
    number_plate: str = None
    chassis: str = None
    national_registry: str = None
    year_fabric: str = None
    year_model: str = None
    fuel: str = None
    color: str = None
    category: str = None
    certification_number: str = None
    crlv_image: str = None
    created_at: datetime.datetime = None
    updated_at: datetime.datetime = None
    updated_by: Optional[str] = None
    
    class Config:
      """Configs"""
      from_attributes = True
  
class VehicleUpdate(VehicleCreate):
   
  updated_by: str = None
   
  class Config:
    from_attributes = True