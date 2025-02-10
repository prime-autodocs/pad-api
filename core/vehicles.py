from typing import List
from database.database import db
from fastapi import HTTPException, status

from loguru import logger

from interfaces.api.schemas.vehicles import VehiclesByCustomer, VehicleDetail
from database.queries.vehicles import VehiclesQueries
from database.models.vehicles import Vehicles
from services.utils.vehicle_validation import vehicle_data_validation
from services.utils.vehicle_data_formatter import data_formatter


class Vehicle:
    
    @classmethod
    def get_vehicles_by_customer_id(cls, customer_id: int) -> List[VehiclesByCustomer]:
        """function to get all vehicle from a customer

        Args:
            customer_id (int): id from table customers

        Returns:
            List[VehiclesByCustomer]: a list of all vehicles from a customer
        """
        vehicle = VehiclesQueries.get_vehicles_by_customer_id(customer_id=customer_id)
        return vehicle
    
    @classmethod
    def get_vehicle_detail(cls, vehicle_id: int) -> VehicleDetail:
        """ function to get a vehicle detail
        
        Args:
            vehicle_id (int): id from table vehicles
            
        Returns:
            VehicleDetail: a vehicle detail
        """
        vehicle = VehiclesQueries.get_vehicle_detail(vehicle_id=vehicle_id)
        return vehicle

    @classmethod
    def create_vehicle(cls, data: Vehicles) -> None:
        """function to create a vehicle
        
        Args:
            data (VehicleCreate): a model with vehicle atributes
        
        Returns:
            Message of sucess
        """
        validation = vehicle_data_validation(payload=data)
        if not validation.get("is_valid"):
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=validation.get("errors"))
        data = data_formatter(payload=data)

        try:
            VehiclesQueries.create_vehicle(data=data)
            return HTTPException(status_code=status.HTTP_200_OK, detail=f"Veículo: {data.number_plate} - {data.brand} {data.model} criado com sucesso")

        except Exception as e:
            logger.error(f"Erro geral no cadastro do veiculo: {e}")
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro geral no cadastro do veiculo: {e}")