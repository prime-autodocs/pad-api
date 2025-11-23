"""Queries for vehicles"""
from database.session import db_session
from database.models.vehicles import Vehicles
from services.enums import CategoryEnum, FuelEnum


class VehiclesQueries:
    """Queries for vehicles"""

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

            return vehicle

    @classmethod
    def get_vehicle_by_id(cls, vehicle_id: int):
        """Query to get a vehicle by id

        Args:
            vehicle_id (int): id from table vehicles
        """
        with db_session() as db:
            vehicle = db.query(Vehicles).filter(Vehicles.id == vehicle_id).first()
            return vehicle if vehicle else None

    @classmethod
    def create_vehicle(cls, data: Vehicles):
        """Query to create a vehicle

        Args:
            data (Model): a model with vehicle atributes
        """
        with db_session() as db:
            # Normaliza categoria para o enum/campo correto
            category_value = data.category
            if isinstance(category_value, str):
                value_lower = category_value.lower()
                if value_lower == "particular":
                    category_value = CategoryEnum.particular
                elif value_lower == "rent":
                    category_value = CategoryEnum.rent
            if isinstance(category_value, CategoryEnum):
                category_value = category_value.value

            # Normaliza combustível para o enum/campo correto
            fuel_value = data.fuel
            if isinstance(fuel_value, str):
                v = fuel_value.lower()
                # "Álcool', 'Gás', 'Gasolina', 'Álcool/Gasolina', 'Gasolina/Gas' or 'Diesel'"
                if v in ("álcool", "gás", "gasolina", "álcool/gasolina", "gasolina/gas", "diesel"):
                    fuel_value = FuelEnum(v)
            if isinstance(fuel_value, FuelEnum):
                fuel_value = fuel_value.value

            vehicle = Vehicles(
                customer_id=data.customer_id,
                brand=data.brand,
                model=data.model,
                number_plate=data.number_plate,
                chassis=data.chassis,
                national_registry=data.national_registry,
                year_fabric=data.year_fabric,
                year_model=data.year_model,
                fuel=fuel_value,
                color=data.color,
                category=category_value,
                certification_number=data.certification_number,
                crlv_image=data.crlv_image,
            )

            db.add(vehicle)
            db.commit()

    @classmethod
    def update_vehicle(cls, new_data: Vehicles):
        """Query to update a vehicle

        Args:
            new_data (Model): a model with vehicle atributes
        """
        with db_session() as db:
            db.merge(new_data)
            db.commit()

    @classmethod
    def delete_vehicle(cls, vehicle: Vehicles):
        """Query to delete a vehicle

        Args:
            vehicle (Model): a model with vehicle atributes
        """
        with db_session() as db:
            db.delete(vehicle)
            db.commit()

