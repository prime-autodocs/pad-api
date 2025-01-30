import datetime
from typing import Optional
from pydantic import BaseModel
from services.enums import GenderEnum, CivilStatusEnum, CustomerTypeEnum

class CustomersBase(BaseModel):
  id: int = None
  customer_type: CustomerTypeEnum
  cpf_number: str = None
  full_name: str = None
  gender: GenderEnum
  email: str = None
  birth_date: datetime.date = None
  civil_status: CivilStatusEnum
  tel_number: str = None
  created_at: datetime.datetime = None
  updated_at: datetime.datetime = None
  updated_by: Optional[str] = None

  class Config:
      """Configs"""
      from_attributes = True


class CustomerCreate(BaseModel):
  customer_type: CustomerTypeEnum
  cpf_number: str = None
  full_name: str = None
  gender: GenderEnum
  email: str = None
  birth_date: datetime.date = None
  civil_status: CivilStatusEnum
  tel_number: str = None

  class Config:
     from_attributes = True

class CustomerUpdate(CustomerCreate):
   
   updated_by: str = None
   
   class Config:
      from_attributes = True