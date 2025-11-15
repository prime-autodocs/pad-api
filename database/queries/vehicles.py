from fastapi import status, HTTPException

from database.session import db_session
from database.models.vehicles import Vehicles


class VehiclesQueries:

    table = Vehicles

    @classmethod
    def get_vehicles_by_customer_id(cls, customer_id: int):
        """Query to get all vehicles from a customer

        Args:
            customer_id (int): id from table customers

        Returns:
            Model Object: return each vehicle from a customer
        """
        with db_session() as db:
            vehicle = (
                db.query(Vehicles)
                .filter(Vehicles.customer_id == customer_id)
                .all()
            )
            if not vehicle:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Cliente não encontrado.",
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
        with db_session() as db:
            vehicle = db.query(Vehicles).filter(Vehicles.id == vehicle_id).first()
            if not vehicle:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Veículo não encontrado.",
                )
            return vehicle

    @classmethod
    def create_vehicle(cls, data: Vehicles):
        """Query to create a vehicle

        Args:
            data (Model): a model with vehicle atributes
        """
        with db_session() as db:
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
                crlv_image=data.crlv_image,
            )

            db.add(vehicle)
            db.commit()

    @classmethod
    def update_vehicle(cls, new_data: Vehicles):
        with db_session() as db:
            db.merge(new_data)
            db.commit()

    @classmethod
    def delete_vehicle(cls, vehicle: Vehicles):
        with db_session() as db:
            db.delete(vehicle)
            db.commit()


