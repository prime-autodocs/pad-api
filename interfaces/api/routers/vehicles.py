from fastapi import APIRouter
from typing import List
from core.vehicles import Vehicle
from interfaces.api.schemas.vehicles import VehiclesByCustomer, VehicleCreate

router = APIRouter()

@router.get(
    "/"
)
async def get_vehicles_by_customer_id(customer_id: int) -> List[VehiclesByCustomer]:
    """Endpoint that return a list of all vehicles from a customer

    Args:
        customer_id (int): id from table customers

    Returns:
        List[VehiclesByCustomer]: return each vehicle from a customer
    """
    response = Vehicle.get_vehicles_by_customer_id(customer_id=customer_id)
    return response

@router.post(
    "/"
)
async def create_vehicle(
    data: VehicleCreate
) -> None:
    """_summary_

    Args:
        data (VehicleCreate): Receive

    Returns:
        Message of sucess
        
    Exceptions:
        400: General create error
    """
    response = Vehicle.create_vehicle(data=data)
    return response

