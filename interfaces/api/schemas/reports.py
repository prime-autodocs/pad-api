"""Schemas for reports"""
from typing import List, Optional
import datetime

from pydantic import BaseModel

from services.enums import CustomerTypeEnum, GenderEnum, CivilStatusEnum
from services.enums import CategoryEnum


class CustomerVehiclesReportItem(BaseModel):
    """Customer vehicles report item"""
    id: int
    name: str
    tax_id: str
    customer_type: CustomerTypeEnum
    total_vehicles: int

    class Config:
        """Configs"""
        from_attributes = True


class CustomerVehiclesReportResponse(BaseModel):
    """Customer vehicles report response"""
    items: List[CustomerVehiclesReportItem]
    total_clients: int

    class Config:
        """Configs"""
        from_attributes = True

class CustomerDetailsCustomer(BaseModel):
    """Customer details customer"""
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
    customer_image: Optional[str] = None

    class Config:
        """Configs"""
        from_attributes = True


class CustomerDetailsAddress(BaseModel):
    """Customer details address"""
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
        """Configs"""
        from_attributes = True


class CustomerDetailsDocuments(BaseModel):
    """Customer details documents"""
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
        """Configs"""
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

class VehicleDetail(BaseModel):
    """Detalhe de um veículo específico para relatórios."""
    id: int = None
    brand: str = None
    model: str = None
    number_plate: str = None
    chassis: str = None
    national_registry: str = None
    year_fabric: str = None
    year_model: str = None
    fuel: str = None
    color: str | None = None
    category: CategoryEnum = None
    certification_number: str | None = None
    crlv_image: str | None = None
    class Config:
        """Configs"""
        from_attributes = True
