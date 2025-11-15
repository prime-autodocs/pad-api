from typing import Optional

from fastapi import APIRouter, Query
import time
from core.reports import Reports
from interfaces.api.schemas.reports import (
    CustomerVehiclesReportResponse,
    CustomerDetailsResponse,
)
from services.enums import CustomerTypeEnum


router = APIRouter()


@router.get("/list", response_model=CustomerVehiclesReportResponse)
async def list_customers_vehicles(
    search: Optional[str] = Query(
        default=None,
        description="Texto para busca por nome, CPF/CNPJ ou placa",
    ),
    filter_by: Optional[CustomerTypeEnum] = Query(
        default=None,
        description="Filtra por tipo de cliente: DETRAN, SMTR ou both",
    ),
) -> CustomerVehiclesReportResponse:
    """
    Relatório de clientes com quantidade de veículos.

    - `search`: busca por partes do nome, CPF/CNPJ (tax_id) ou placa (number_plate)
    - `filter_by`: filtra pelo tipo de cliente (CustomerTypeEnum)
    - ordenado alfabeticamente pelo nome do cliente
    """
    time.sleep(5)
    return Reports.list_customers_vehicles(search=search, filter_by=filter_by)


@router.get("/customer-details/{customer_id}", response_model=CustomerDetailsResponse)
async def get_customer_details(customer_id: int) -> CustomerDetailsResponse:
    """
    Retorna todos os dados do cliente (customers, address, documents)
    para o `customer_id` informado.
    """
    return Reports.get_customer_details(customer_id=customer_id)

