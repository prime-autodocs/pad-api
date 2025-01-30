from pydantic import BaseModel

class VehiclesByCustomer(BaseModel):
    brand: str = None
    model: str = None
    number_plate: str = None
    
    class Config:
      """Configs"""
      from_attributes = True