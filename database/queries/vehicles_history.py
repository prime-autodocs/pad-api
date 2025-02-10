from fastapi import status, HTTPException

from database.models.vehicles import Vehicles
from database.models.vehicle_history import VehiclesHistory
from database.database import db

class VehiclesHistoriesQueries():
    
    table = VehiclesHistory
    
    @classmethod
    def add_vehicle_history(cls, data: Vehicles, description: str):
        history = VehiclesHistory(
            vehicle_id=data.id,
            updated_by=data.updated_by,
            description=description
        )
        db.add(history)