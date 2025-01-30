from database.database import db
from database.models.vehicles import Vehicles

class VehiclesQueries():
    
    table = Vehicles
    
    @classmethod
    def get_vehicles_by_customer(cls, customer_id: int):
        """Query to get all vehicles from a customer

        Args:
            customer_id (int): id from table customers

        Returns:
            Model Object: return each vehicle from a customer
        """
        return db.query(Vehicles).filter(Vehicles.customer_id == customer_id).all()