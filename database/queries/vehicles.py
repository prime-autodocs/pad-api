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