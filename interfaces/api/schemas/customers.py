import datetime
from typing import Optional
from pydantic import BaseModel
from services.enums import GenderEnum, CivilStatusEnum, CustomerTypeEnum, TaxTypeEnum

class CustomersBase(BaseModel):
   id: int = None
   tax_type: TaxTypeEnum
   tax_id: str = None
   full_name: str = None
   gender: GenderEnum
   email: str = None
   birth_date: datetime.date = None
   customer_type: CustomerTypeEnum
   civil_status: CivilStatusEnum
   tel_number: str = None
   created_at: datetime.datetime = None
   updated_at: datetime.datetime = None
   updated_by: Optional[str] = None

   class Config:
      """Configs"""
      from_attributes = True


class CustomerCreate(BaseModel):
   tax_type: TaxTypeEnum = None
   tax_id: str = None
   full_name: str = None
   gender: GenderEnum = None
   email: str = None
   birth_date: datetime.date = None
   customer_type: CustomerTypeEnum = None
   civil_status: CivilStatusEnum = None
   tel_number: str = None

   class Config:
      from_attributes = True

class CustomerUpdate(CustomerCreate):
   
   updated_by: str = None
   
   class Config:
      from_attributes = True
      
class CustomerFinder(BaseModel):
   full_name: str = None
   tax_id: str = None
   tel_number: str = None
   
   class Config:
      from_attributes = True