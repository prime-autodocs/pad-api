"""Queries para relatórios."""
from typing import List, Optional

from sqlalchemy import func, or_

from database.session import db_session
from database.models.customers import Customers
from database.models.vehicles import Vehicles
from database.models.address import Address
from database.models.documents import Documents
from interfaces.api.schemas.reports import (
    CustomerVehiclesReportItem,
    CustomerDetailsResponse,
    VehicleDetail,
)
from services.enums import CustomerTypeEnum, FuelEnum


class ReportsQueries:
    """Queries para relatórios."""
    @classmethod
    def get_customers_vehicles_report(
        cls,
        search: Optional[str] = None,
        filter_by: Optional[CustomerTypeEnum] = None,
    ) -> List[CustomerVehiclesReportItem]:
        """
        Retorna a lista de clientes com a quantidade de veículos cadastrados.

        - `search`: filtra por nome, CPF/CNPJ (tax_id) ou placa (number_plate)
        - `filter_by`: filtra pelo tipo de cliente (CustomerTypeEnum)
        - ordena alfabeticamente pelo nome do cliente
        """
        with db_session() as db:
            # base: LEFT OUTER JOIN para contar inclusive clientes sem veículos
            query = (
                db.query(
                    Customers.id.label("id"),
                    Customers.full_name.label("name"),
                    Customers.tax_id.label("tax_id"),
                    Customers.customer_type.label("customer_type"),
                    func.count(Vehicles.id).label("total_vehicles"),
                )
                .outerjoin(
                    Vehicles,
                    Vehicles.customer_id == Customers.id,
                )
            )

            if filter_by is not None:
                query = query.filter(Customers.customer_type == filter_by)

            if search:
                like_pattern = f"%{search}%"
                query = query.filter(
                    or_(
                        Customers.full_name.ilike(like_pattern),
                        Customers.tax_id.ilike(like_pattern),
                        Vehicles.number_plate.ilike(like_pattern),
                    )
                )

            query = (
                query.group_by(
                    Customers.id,
                    Customers.full_name,
                    Customers.tax_id,
                    Customers.customer_type,
                )
                .order_by(Customers.full_name.asc())
            )

            rows = query.all()

            items: List[CustomerVehiclesReportItem] = []
            for row in rows:
                items.append(
                    CustomerVehiclesReportItem(
                        id=row.id,
                        name=row.name,
                        tax_id=row.tax_id,
                        customer_type=row.customer_type,
                        total_vehicles=row.total_vehicles,
                    )
                )

            return items

    @classmethod
    def get_customer_details(cls, customer_id: int) -> Optional[CustomerDetailsResponse]:
        """
        Retorna os detalhes completos de um cliente (customers, address, documents).
        """
        with db_session() as db:
            customer = db.query(Customers).filter(Customers.id == customer_id).first()
            if not customer:
                return None

            address = (
                db.query(Address)
                .filter(Address.customer_id == customer_id)
                .order_by(Address.id.desc())
                .first()
            )

            documents = (
                db.query(Documents)
                .filter(Documents.customer_id == customer_id)
                .first()
            )

            # Monta o objeto de resposta com os dados do cliente na raiz
            # e as chaves aninhadas address/documents.
            response = CustomerDetailsResponse.model_validate(
                customer,
                from_attributes=True,
            )
            response.address = address
            response.documents = documents
            return response

    @classmethod
    def get_vehicle_detail(cls, vehicle_id: int) -> Optional[VehicleDetail]:
        """Retorna o detalhe de um veículo específico para relatórios."""
        with db_session() as db:
            vehicle = db.query(Vehicles).filter(Vehicles.id == vehicle_id).first()
            vehicle.fuel = vehicle.fuel.value
            
            return vehicle if vehicle else None
