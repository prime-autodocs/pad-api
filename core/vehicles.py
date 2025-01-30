from typing import List
from interfaces.api.schemas.vehicles import VehiclesByCustomer
from database.queries.vehicles import VehiclesQueries


class Vehicle:
    
    @classmethod
    def get_vehicles_by_customer(cls, customer_id: int) -> List[VehiclesByCustomer]:
        """function to get all vehicle from a customer

        Args:
            customer_id (int): id from table customers

        Returns:
            List[VehiclesByCustomer]: a list of all vehicles from a customer
        """
        vehicle = VehiclesQueries.get_vehicles_by_customer(customer_id=customer_id)
        return vehicle