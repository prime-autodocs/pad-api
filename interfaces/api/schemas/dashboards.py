from enum import Enum
from typing import List

from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_customers: int
    total_vehicles: int
    new_customers_current_month: int
    services_current_month: int


class DashboardPeriod(str, Enum):
    monthly = "monthly"
    quarter = "quarter"
    annual = "annual"


class NewCustomersPoint(BaseModel):
    label: str
    value: int


class NewCustomersTimeSeries(BaseModel):
    period: DashboardPeriod
    points: List[NewCustomersPoint]
