from typing import Optional

from fastapi import HTTPException, status

from interfaces.api.schemas.reports import (
    CustomerVehiclesReportItem,
    CustomerVehiclesReportResponse,
    CustomerDetailsResponse,
    VehicleDetail,
)
from database.queries.reports import ReportsQueries
from services.enums import CustomerTypeEnum


class Reports:
    @classmethod
    def list_customers_vehicles(
        cls,
        search: Optional[str] = None,
        filter_by: Optional[CustomerTypeEnum] = None,
    ) -> CustomerVehiclesReportResponse:
        """
        Retorna o relatório de clientes com quantidade de veículos.
        """
        items = ReportsQueries.get_customers_vehicles_report(
            search=search,
            filter_by=filter_by,
        )
        return CustomerVehiclesReportResponse(
            items=items,
            total_clients=len(items),
        )

    @classmethod
    def get_customer_details(cls, customer_id: int) -> CustomerDetailsResponse:
        """
        Retorna os detalhes de um cliente específico.
        """
        details = ReportsQueries.get_customer_details(customer_id=customer_id)
        if details is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente não encontrado.",
            )
        return details

    @classmethod
    def get_vehicle_details(cls, vehicle_id: int) -> VehicleDetail:
        """
        Retorna o detalhe de um veículo específico para relatórios.
        """
        vehicle = ReportsQueries.get_vehicle_detail(vehicle_id=vehicle_id)
        if vehicle is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Veículo não encontrado.",
            )
            
        fuel_map = {
            'gas': "Gás",
            'alchool': "Álcool",
            'gasoline': "Gasolina",
            'alchool_gas': "Álcool/Gasolina",
            'gasoline_gas': "Gasolina/Gas",
            'diesel': "Diesel",
            'electric': "Elétrico",
        }
        vehicle.fuel = fuel_map.get(vehicle.fuel)
        return vehicle

