from typing import List
from database.database import db
from fastapi import HTTPException, status

from loguru import logger

from interfaces.api.schemas.vehicles import VehiclesByCustomer
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
    def create_vehicle(cls, data: Vehicles) -> None:
        
        validation = vehicle_data_validation(payload=data)
        if not validation.get("is_valid"):
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=validation.get("errors"))
        data = data_formatter(payload=data)

        vehicle = Vehicles(
            customer_id=data.customer_id,
            brand=data.brand,
            model=data.model,
            number_plate=data.number_plate,
            chassis=data.chassis,
            national_registry=data.national_registry,
            fabric_year=data.fabric_year,
            model_year=data.model_year,
            fuel=data.fuel,
            color=data.color,
            category=data.category,
            certification_number=data.cerfification_number,
            crlv_image=data.crlv_image
        )
        
        try:
            db.add(vehicle)
            db.commit()
            db.close()
            
            return HTTPException(status_code=status.HTTP_200_OK, detail=f"Cliente: {vehicle.number_plate} - {vehicle.brand} {vehicle.model} criado com sucesso")
        except Exception as e:
            db.rollback()
            db.close()

            logger.error(f"Erro geral no cadastro do cliente: {e}")
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro geral no cadastro do cliente: {e}")