from fastapi import status, HTTPException

from database.models.vehicles import Vehicles
from database.models.vehicle_history import VehiclesHistory
from database.session import db_session


class VehiclesHistoriesQueries:

    table = VehiclesHistory

    @classmethod
    def add_vehicle_history(cls, data: Vehicles, description: str):
        history = VehiclesHistory(
            vehicle_id=data.id,
            updated_by=data.updated_by,
            description=description,
        )
        with db_session() as db:
            db.add(history)
            db.commit()