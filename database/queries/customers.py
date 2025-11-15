from typing import Optional

from fastapi import status, HTTPException

from database.models.customers import Customers
from database.models.address import Address
from database.models.documents import Documents
from database.session import db_session
from interfaces.api.schemas.customers import AddressCreate, DocumentsCreate


class CustomersQueries:

    table = Customers

    @classmethod
    def get_all_customers(cls):
        """Query for get all customers

        Returns:
            Model Object: List[Customers]
        """
        with db_session() as db:
            return db.query(Customers).all()

    @classmethod
    def get_customer_by_id(cls, customer_id: int):
        """Query for get a single client by customer_id

        Args:
            customer_id (int): ID of the customer in database

        Returns:
            Model Object: Customer
        """
        with db_session() as db:
            customer = db.query(Customers).filter(Customers.id == customer_id).first()
            if not customer:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Cliente não encontrado.",
                )
            return customer

    @classmethod
    def get_customer_by_tax_id(cls, tax_id: str):
        """Query for get a single client by tax_id

        Args:
            tax_id (str): 11 or 14 numbers for CPF or CNPJ

        Returns:
            Model Object: Customer
        """
        with db_session() as db:
            customer = db.query(Customers).filter(Customers.tax_id == tax_id).first()
            return customer if customer else None

    @classmethod
    def create_customer(
        cls,
        customer: Customers,
        address: Optional[AddressCreate],
        documents: Optional[DocumentsCreate],
    ):
        """Query to create a customer (and related data) in database."""
        with db_session() as db:
            # Salva o cliente
            db.add(customer)
            db.flush()  # garante que customer.id foi gerado

            # Endereço (opcional)
            if address is not None:
                address_row = Address(
                    customer_id=customer.id,
                    address=address.address,
                    number=address.number,
                    complement=address.complement,
                    neighborhood=address.neighborhood,
                    city=address.city,
                    state=address.state,
                    zip_code=address.zip_code,
                )
                db.add(address_row)

            # Documentos (opcional)
            if documents is not None:
                documents_row = Documents(
                    customer_id=customer.id,
                    identity_number=documents.identity_number,
                    identity_org=documents.identity_org,
                    identity_issued_at=documents.identity_issued_at,
                    identity_local=documents.identity_local,
                    driver_license_number=documents.driver_license_number,
                    driver_license_expiration=documents.driver_license_expiration,
                    driver_license_image=documents.driver_license_image,
                    smtr_permission_number=documents.smtr_permission_number,
                    smtr_permission_image=documents.smtr_permission_image,
                    smtr_ratr_number=documents.smtr_ratr_number,
                )
                db.add(documents_row)

            db.commit()

    @classmethod
    def update_customer(cls, new_data: Customers):
        with db_session() as db:
            db.merge(new_data)
            db.commit()

    @classmethod
    def delete_customer(cls, customer: Customers):
        with db_session() as db:
            db.delete(customer)
            db.commit()

