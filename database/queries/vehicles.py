from fastapi import status, HTTPException

from database.database import db
from database.models.vehicles import Vehicles

class VehiclesQueries():
    
    table = Vehicles
    
    @classmethod
    def get_vehicles_by_customer_id(cls, customer_id: int):
        """Query to get all vehicles from a customer

        Args:
            customer_id (int): id from table customers

        Returns:
            Model Object: return each vehicle from a customer
        """
        vehicle = db.query(Vehicles).filter(Vehicles.customer_id == customer_id).all()
        if not vehicle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente não encontrado."
            )
        return vehicle
    
    @classmethod
    def get_vehicle_detail(cls, vehicle_id: int):
        """ Query to get a vehicle detail
        
        Args:
            vehicle_id (int): id from table vehicles
        
        Returns:
            Model Object: return vehicle detail
        """
        vehicle = db.query(Vehicles).filter(Vehicles.id == vehicle_id).first()
        if not vehicle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Veículo não encontrado."
            )
        return vehicle
        
    @classmethod
    def create_vehicle(cls, data: Vehicles):
        """Query to create a vehicle

        Args:
            data (Model): a model with vehicle atributes
        """
        vehicle = Vehicles(
            customer_id=data.customer_id,
            brand=data.brand,
            model=data.model,
            number_plate=data.number_plate,
            chassis=data.chassis,
            national_registry=data.national_registry,
            year_fabric=data.year_fabric,
            year_model=data.year_model,
            fuel=data.fuel,
            color=data.color,
            category=data.category,
            certification_number=data.certification_number,
            crlv_image=data.crlv_image
        )
        
        db.add(vehicle)
        
    @classmethod
    def delete_vehicle(cls, vehicle: Vehicles):
        db.delete(vehicle)