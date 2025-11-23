"""Core for customers"""
from typing import List
from fastapi import status, HTTPException
from fastapi.responses import JSONResponse

from loguru import logger

from database.models.customers import Customers
from database.queries.customers import CustomersQueries
from database.queries.customers_history import CustomerHistoriesQueries
from interfaces.api.schemas.customers import (
    CustomersBase,
    CustomerFinder,
    CustomerCreateWithDetails,
    CustomerUpdate,
    CustomerAvailable,
)
from services.utils.customer_validation import customer_data_validation
from services.utils.customer_data_formatter import data_formatter
from services.utils.vercel_blob import VercelBlob


class Customer:
    """Class for customers"""
    @classmethod
    def get_all_customers(cls) -> List[CustomersBase]:
        """ Get all customers 

        Returns:
            List[CustomersBase]: List of all customers in customer table
        """
        customers = CustomersQueries.get_all_customers()
        return customers

    @classmethod
    def get_available_customers(
        cls,
        search: str | None = None,
        field_selected: str | None = None,
    ) -> List[CustomerAvailable]:
        """
        Retorna clientes disponíveis para seleção em cadastros de veículo,
        contendo apenas nome e CPF/CNPJ, ordenados alfabeticamente,
        com filtros por nome/CPF/CNPJ conforme parâmetros.
        """
        customers = CustomersQueries.get_available_customers(
            search=search,
            field_selected=field_selected,
        )
        return [
            CustomerAvailable(id=c.id, name=c.full_name, tax_id=c.tax_id)
            for c in customers
        ]

    @classmethod
    def get_customer_by_id(cls, customer_id: int) -> CustomersBase:
        """ Get a single customer by ID

        Args:
            customer_id (int): ID of customer

        Returns:
            CustomersBase: Object of a single customer with all atributes
        """
        customer = CustomersQueries.get_customer_by_id(customer_id=customer_id)
        return customer

    @classmethod
    def create_customer(cls, data: CustomerCreateWithDetails) -> None:
        """ Create a single customer 

        Args:
            data (Customers): A model with customers atributes

        Returns:
            Message of success
            
        Exceptions:
            400: General create error
        """
        customer = CustomersQueries.get_customer_by_tax_id(tax_id=data.tax_id)
        if customer is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cliente já cadastrado.",
            )

        if data.customer_image:
            customer_image_url = VercelBlob.upload_with_delete(
                image_base64=data.customer_image,
                image_name=f"customer_photo_{data.tax_id}.png",
            )
        else:
            customer_image_url = None

        # Mapeia os dados de entrada (Pydantic) para o model Customers
        customer_model = Customers(
            tax_type=data.tax_type,
            tax_id=data.tax_id,
            full_name=data.full_name,
            gender=data.gender,
            email=data.email,
            birth_date=data.birth_date,
            customer_type=data.customer_type,
            civil_status=data.civil_status,
            tel_number=data.tel_number,
            customer_image=customer_image_url,
        )

        validation = customer_data_validation(payload=customer_model)
        if not validation.get("is_valid"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=validation.get("errors"),
            )
        customer_model = data_formatter(payload=customer_model)

        try:
            CustomersQueries.create_customer(
                customer=customer_model,
                address=data.address,
                documents=data.documents,
            )
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=f"Cliente: {customer_model.tax_id} - {customer_model.full_name} criado com sucesso",
            )

        except Exception as e:
            logger.error(f"Erro geral no cadastro do cliente: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro geral no cadastro do cliente: {e}",
            ) from e
    @classmethod
    def update_customer(cls, customer_id: int, new_data: CustomerUpdate) -> None:
        """ Update a single customer

        Args:
            tax_id (str): 11 or 14 numbers for CPF or CNPJ
            new_data (Customers): A model with customers atributes the will change

        Returns:
            Message of success
            
        Exceptions:
            400: General update error
        """
        customer_row = CustomersQueries.get_customer_by_id(customer_id=customer_id)

        # Aplica apenas campos enviados no payload (exclude_unset=True)
        payload_dict = new_data.model_dump(exclude_unset=True)
        if new_data.customer_image:
            new_data.customer_image = VercelBlob.upload_with_delete(
                image_base64=new_data.customer_image, 
                image_name=f"customer_photo_{customer_row.tax_id}.png",
            )
            new_image = True
        else:
            new_data.customer_image = customer_row.customer_image
            new_image = False
        columns_changed = []
        for key, value in payload_dict.items():
            # Campos de address/documents são tratados separadamente
            if key in {"address", "documents", "updated_by"}:
                continue

            if hasattr(customer_row, key) and value is not None:
                current_value = getattr(customer_row, key)
                if current_value != value:
                    columns_changed.append(key)
                    setattr(customer_row, key, value)
                    
        if new_image:
            customer_row.customer_image = new_data.customer_image

        customer_row.updated_by = new_data.updated_by or "Lucas"

        # Validação após aplicação das mudanças
        validation = customer_data_validation(payload=customer_row)
        if not validation.get("is_valid"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=validation.get("errors"),
            )

        # TODO: reativar histórico de alterações se necessário
        # for column in columns_changed:
        #     CustomerHistoriesQueries.add_customer_history(
        #         data=customer_row, description=f"Column {column} changed"
        #     )

        try:
            CustomersQueries.update_customer(
                new_data=customer_row,
                address=new_data.address,
                documents=new_data.documents,
            )
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=f"Cliente: {customer_row.tax_id} - {customer_row.full_name} atualizado com sucesso",
            )

        except Exception as e:
            logger.error(f"Erro geral na atualização do cliente: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro geral na atualização do cliente: {e}",
            ) from e

    @classmethod
    def delete_customer(cls, customer_id: int) -> None:
        """ Delete a single customer

        Args:
            customer_id (int): ID of customer

        Returns:
            Message of success
            
        Exceptions:
            400: General delete error
        """
        customer = CustomersQueries.get_customer_by_id(customer_id=customer_id)
        try:
            CustomersQueries.delete_customer(customer=customer)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=f"Cliente: {customer.tax_id} - {customer.full_name} deletado com sucesso",
            )
        
        except Exception as e:
            logger.error(f"Erro geral na exclusão do cliente: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro geral na exclusão do cliente: {e}",
            ) from e

    @classmethod
    def get_customer_by_tax_id(cls, tax_id: str) -> CustomerFinder:
        """ Get a single customer by Tax ID

        Args:
            tax_id (str): 11 or 14 numbers for CPF or CNPJ

        Returns:
            CustomerFinder: Object of a single customer with full_name, tax_id and tel_number
        """
        customer = CustomersQueries.get_customer_by_tax_id(tax_id=tax_id)
        return CustomerFinder(
            full_name=customer.full_name,
            tax_id=customer.tax_id,
            tel_number=customer.tel_number,
        )