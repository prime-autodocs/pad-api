"""Core for vehicles"""
from typing import List

from fastapi.responses import JSONResponse
from fastapi import HTTPException, status
from loguru import logger

from interfaces.api.schemas.vehicles import VehiclesByCustomer
from database.queries.vehicles import VehiclesQueries
from database.models.vehicles import Vehicles
from services.utils.vehicle_validation import vehicle_data_validation
from services.utils.vehicle_data_formatter import data_formatter
from database.queries.vehicles_history import VehiclesHistoriesQueries
from database.queries.customers import CustomersQueries


class Vehicle:
    """Class for vehicles"""

    @classmethod
    def get_vehicle_by_id(cls, vehicle_id: int) -> VehiclesByCustomer:
        """function to get a vehicle by id

        Args:
            vehicle_id (int): id from table vehicles
        """
        vehicle = VehiclesQueries.get_vehicle_by_id(vehicle_id=vehicle_id)
        return vehicle

    @classmethod
    def get_vehicles_by_customer_id(cls, customer_id: int) -> List[VehiclesByCustomer]:
        """function to get all vehicle from a customer

        Args:
            customer_id (int): id from table customers

        Returns:
            List[VehiclesByCustomer]: a list of all vehicles from a customer
        """
        vehicles = VehiclesQueries.get_vehicles_by_customer_id(customer_id=customer_id)
        vehicle_customer = CustomersQueries.get_customer_by_id(customer_id=customer_id)
        if not vehicle_customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente não encontrado",
            )

        # Adiciona campo calculado (por enquanto hardcoded)
        for v in vehicles:
            v.customer_name = vehicle_customer.full_name
            v.tax_id = vehicle_customer.tax_id
            setattr(v, "last_legalization_year", 2025)

        return vehicles

    @classmethod
    def create_vehicle(cls, data: Vehicles) -> None:
        """function to create a vehicle
        
        Args:
            data (VehicleCreate): a model with vehicle atributes
        
        Returns:
            Message of success
        """
        validation = vehicle_data_validation(payload=data)
        if not validation.get("is_valid"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=validation.get("errors"),
            )

        data = data_formatter(payload=data)

        try:
            VehiclesQueries.create_vehicle(data=data)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=f"Veículo: {data.number_plate} - {data.brand} {data.model} criado com sucesso",
            )

        except Exception as e:
            logger.error(f"Erro geral no cadastro do veiculo: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro geral no cadastro do veiculo: {e}",
            ) from e

    @classmethod
    def update_vehicle(cls, vehicle_id: int, new_data: Vehicles) -> None:
        """ Update a single vehicle

        Args:
            vehicle_id (str): a ID (internal) of a vehicle from table Vehicle
            new_data (Vehicle): A model with vehicle atributes the will change

        Returns:
            Message of success
            
        Exceptions:
            400: General update error
        """
        validation = vehicle_data_validation(payload=new_data)
        if not validation.get("is_valid"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=validation.get("errors"),
            )

        vehicle_row = VehiclesQueries.get_vehicle_by_id(vehicle_id=vehicle_id)

        columns_changed = []
        for key, value in new_data:
            if hasattr(vehicle_row, key) and value is not None:
                current_value = getattr(vehicle_row, key)
                if current_value != value:
                    columns_changed.append(key)
                    setattr(vehicle_row, key, value)

        vehicle_row.updated_by = "Isaac"

        # for column in columns_changed:
        #     VehicleHistoriesQueries.add_vehicle_history(data=vehicle_row, description=f"Column {column} changed")

        try:
            VehiclesQueries.update_vehicle(new_data=vehicle_row)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=f"Cliente: {vehicle_row.brand} - {vehicle_row.model} atualizado com sucesso"
            )

        except Exception as e:
            logger.error(f"Erro geral na atualização do cliente: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro geral na atualização do cliente: {e}",
            ) from e

    @classmethod
    def delete_vehicle(cls, vehicle_id: int) -> None:
        """ function to delete a vehicle
        
        Args:
            vehicle_id (int): id from table vehicles
        
        Returns:
            Message of success
        """
        vehicle = VehiclesQueries.get_vehicle_by_id(vehicle_id=vehicle_id)
        try:
            VehiclesQueries.delete_vehicle(vehicle=vehicle)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=f"Veículo: {vehicle.brand} - {vehicle.model} deletado com sucesso",
            )
        except Exception as e:
            logger.error(f"Erro geral na exclusão do veículo: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro geral na exclusão do veículo: {e}",
            ) from e
