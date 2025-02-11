from fastapi import APIRouter
from typing import List
from core.vehicles import Vehicle
from interfaces.api.schemas.vehicles import VehiclesByCustomer, VehicleCreate, VehicleDetail, VehicleUpdate

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

@router.get(
    "/{vehicle_id}"
)
async def get_vehicle_detail(vehicle_id: int) -> VehicleDetail:
    """ Endpoint that return a vehicle detail
    
    Args:
        vehicle_id (int): id from table vehicles
        
    Returns:
        VehicleDetail: return vehicle detail
    """
    response = Vehicle.get_vehicle_detail(vehicle_id=vehicle_id)
    return response

@router.post(
    "/"
)
async def create_vehicle(
    data: VehicleCreate
) -> None:
    """Endpoint to create a vehicle

    Args:
        data (VehicleCreate): Receive

    Returns:
        Message of sucess
        
    Exceptions:
        400: General create error
    """
    response = Vehicle.create_vehicle(data=data)
    return response

@router.patch(
    "/{customer_id}"
)
async def update_vehicle(
    vehicle_id: int,
    new_data: VehicleUpdate
) -> None:
    """Endpoint that update a vehicle in database

    Args:
        customer_id (int): ID of vehicle
        new_data (VehicleUpdate): Receive a model data of vehicle to update vehicle

    Returns:
        Message of success
        
    Exceptions:
        400: General create error
    """
    response = Vehicle.update_vehicle(customer_id=vehicle_id, new_data=new_data)
    return response
