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
   tax_type: TaxTypeEnum | None = None
   tax_id: str | None = None
   full_name: str | None = None
   gender: GenderEnum | None = None
   email: str | None = None
   birth_date: datetime.date | None = None
   customer_type: CustomerTypeEnum | None = None
   civil_status: CivilStatusEnum | None = None
   tel_number: str | None = None

   class Config:
      from_attributes = True


class AddressCreate(BaseModel):
   address: str | None = None
   number: str | None = None
   complement: str | None = None
   neighborhood: str | None = None
   city: str | None = None
   state: str | None = None
   zip_code: str | None = None

   class Config:
      from_attributes = True


class DocumentsCreate(BaseModel):
   identity_number: str | None = None
   identity_org: str | None = None
   identity_issued_at: datetime.date | None = None
   identity_local: str | None = None
   driver_license_number: str | None = None
   driver_license_expiration: datetime.date | None = None
   driver_license_image: str | None = None
   smtr_permission_number: str | None = None
   smtr_permission_image: str | None = None
   smtr_ratr_number: str | None = None

   class Config:
      from_attributes = True


class CustomerCreateWithDetails(CustomerCreate):
   address: AddressCreate | None = None
   documents: DocumentsCreate | None = None

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


class CustomerAvailable(BaseModel):
   id: int
   name: str
   tax_id: str
