from fastapi import APIRouter
import time
from core.dashboards import Dashboard
from interfaces.api.schemas.dashboards import (
    DashboardSummary,
    DashboardPeriod,
    NewCustomersTimeSeries,
)


router = APIRouter()


@router.get("/cards-summary")
async def get_dashboard_summary() -> DashboardSummary:
    """
    Endpoint para retornar os números principais do dashboard:
    - total de clientes cadastrados
    - total de veículos cadastrados
    - novos clientes no mês corrente
    - serviços realizados no mês corrente
    """
    return Dashboard.get_summary()


@router.get("/new-customers")
async def get_new_customers_timeseries(
    period: DashboardPeriod,
) -> NewCustomersTimeSeries:
    """
    Endpoint para retornar a série temporal de novos clientes.

    Parâmetro:
    - period: 'monthly' | 'quarter' | 'annual'
    """
    return Dashboard.get_new_customers_timeseries(period=period)

