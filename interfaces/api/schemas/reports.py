from typing import List, Optional
import datetime

from pydantic import BaseModel

from services.enums import CustomerTypeEnum, GenderEnum, CivilStatusEnum


class CustomerVehiclesReportItem(BaseModel):
    id: int
    name: str
    tax_id: str
    customer_type: CustomerTypeEnum
    total_vehicles: int

    class Config:
        from_attributes = True


class CustomerVehiclesReportResponse(BaseModel):
    items: List[CustomerVehiclesReportItem]
    total_clients: int


class CustomerDetailsCustomer(BaseModel):
    id: int
    tax_type: str
    tax_id: str
    full_name: str
    gender: GenderEnum
    email: Optional[str] = None
    birth_date: Optional[datetime.date] = None
    customer_type: CustomerTypeEnum
    civil_status: CivilStatusEnum
    tel_number: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    updated_by: Optional[str] = None

    class Config:
        from_attributes = True


class CustomerDetailsAddress(BaseModel):
    id: int
    customer_id: int
    address: Optional[str] = None
    number: Optional[str] = None
    complement: Optional[str] = None
    neighborhood: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    created_at: datetime.datetime
    updated_at: datetime.datetime
    updated_by: Optional[str] = None

    class Config:
        from_attributes = True


class CustomerDetailsDocuments(BaseModel):
    id: int
    customer_id: int
    identity_number: Optional[str] = None
    identity_org: Optional[str] = None
    identity_issued_at: Optional[datetime.date] = None
    identity_local: Optional[str] = None
    driver_license_number: Optional[str] = None
    driver_license_expiration: Optional[datetime.date] = None
    driver_license_image: Optional[str] = None
    smtr_permission_number: Optional[str] = None
    smtr_permission_image: Optional[str] = None
    smtr_ratr_number: Optional[str] = None
    created_at: datetime.datetime
    updated_at: datetime.datetime
    updated_by: Optional[str] = None

    class Config:
        from_attributes = True


class CustomerDetailsResponse(CustomerDetailsCustomer):
    """
    Detalhes completos de um cliente.

    A estrutura segue o payload de criação:
    - campos do cliente na raiz
    - chaves aninhadas `address` e `documents`.
    """

    address: Optional[CustomerDetailsAddress] = None
    documents: Optional[CustomerDetailsDocuments] = None
