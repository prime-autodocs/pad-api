import datetime
from typing import Optional
from pydantic import BaseModel

class VehiclesByCustomer(BaseModel):
    brand: str = None
    model: str = None
    number_plate: str = None
    
    class Config:
      """Configs"""
      from_attributes = True
      
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