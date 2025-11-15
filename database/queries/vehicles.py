from fastapi import status, HTTPException

from database.session import db_session
from database.models.vehicles import Vehicles
from services.enums import CategoryEnum, FuelEnum


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
            return vehicle

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
                v = fuel_value.lower().replace("ó", "o").replace("ô", "o").replace("ã", "a")

                if v in ("alcool", "alchool", "álcool"):
                    fuel_value = FuelEnum.alchool
                elif v in ("gasolina", "gasoline"):
                    fuel_value = FuelEnum.gasoline
                elif v in ("gas", "gnv"):
                    fuel_value = FuelEnum.gas
                elif v in ("gasolina/alcool", "alcool/gasolina", "gasolina/álcool", "álcool/gasolina"):
                    fuel_value = FuelEnum.alchool_gas
                elif v in ("gasolina/gas", "gas/gasolina"):
                    fuel_value = FuelEnum.gasoline_gas
                elif v == "diesel":
                    fuel_value = FuelEnum.diesel
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
        with db_session() as db:
            db.merge(new_data)
            db.commit()

    @classmethod
    def delete_vehicle(cls, vehicle: Vehicles):
        with db_session() as db:
            db.delete(vehicle)
            db.commit()


