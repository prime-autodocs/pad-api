from fastapi import APIRouter
from typing import List
from core.vehicles import Vehicle
from interfaces.api.schemas.vehicles import VehiclesByCustomer

router = APIRouter()

@router.get(
    "/"
)
async def get_vehicles_by_customer(customer_id: int) -> List[VehiclesByCustomer]:
    """Endpoint that return a list of all vehicles from a customer

    Args:
        customer_id (int): id from table customers

    Returns:
        List[VehiclesByCustomer]: return each vehicle from a customer
    """
    response = Vehicle.get_vehicles_by_customer(customer_id=customer_id)
    return response


