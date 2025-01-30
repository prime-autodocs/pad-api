import json
from fastapi import status, HTTPException
from typing import List

from loguru import logger

from database.database import db
from database.models.customers import Customers
from database.models.customers_history import CustomersHistory
from database.queries.customers import CustomersQueries
from interfaces.api.schemas.customers import CustomersBase
from services.utils.customer_validation import customer_data_validation
from services.utils.customer_data_formatter import data_formatter

class Customer:
    
    @classmethod
    def get_all_customers(cls) -> List[CustomersBase]:
        """ Get all customers 

        Returns:
            List[CustomersBase]: List of all customers in customer table
        """
        customers = CustomersQueries.get_all_customers()
        return customers

    @classmethod
    def get_customer_by_cpf_number(cls, cpf_number: str) -> CustomersBase:
        """ Get a single customer by its cpf number

        Args:
            cpf_number (str): 11 or 14 numbers for CPF or CNPJ

        Returns:
            CustomersBase: Object of a single customer with all atributes
        """
        customer = CustomersQueries.get_customer_by_cpf(cpf_number=cpf_number)
        return customer
    
    @classmethod
    def create_customer(cls, data: Customers) -> None:
        """ Create a single customer 

        Args:
            data (Customers): A model with customers atributes

        Returns:
            Message of sucess
            
        Exceptions:
            400: General create error
        """
        validation = customer_data_validation(payload=data)
        if not validation.get("is_valid"):
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=validation.get("errors"))
        data = data_formatter(payload=data)

        customer = Customers(
            customer_type=data.customer_type,
            cpf_number=data.cpf_number,
            full_name=data.full_name,
            gender=data.gender,
            email=data.email,
            birth_date=data.birth_date,
            civil_status=data.civil_status,
            tel_number=data.tel_number,
        )
        
        try:
            db.add(customer)
            db.commit()
            db.close()
            
            return HTTPException(status_code=status.HTTP_200_OK, detail=f"Cliente: {customer.cpf_number} - {customer.full_name} criado com sucesso")

        except Exception as e:
            db.rollback()
            db.close()

            logger.error(f"Erro geral no cadastro do cliente: {e}")
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro geral no cadastro do cliente: {e}")

    @classmethod    
    def update_customer(cls, cpf_number: str, new_data: Customers) -> None:
        """ Update a single customer

        Args:
            cpf_number (str): 11 or 14 numbers for CPF or CNPJ
            new_data (Customers): A model with customers atributes the will change

        Returns:
            Message of sucess
            
        Exceptions:
            400: General update error
        """
        validation = customer_data_validation(payload=new_data)
        if not validation.get("is_valid"):
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=validation.get("errors"))

        customer_row = CustomersQueries.get_customer_by_cpf(cpf_number=cpf_number)
        if not customer_row:
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente com CPF {cpf_number} não encontrado."
            )
        

        columns_changed = []

        for key, value in new_data:
            if hasattr(customer_row, key):
                current_value = getattr(customer_row, key)
                if current_value != value:
                    columns_changed.append(key)
                    setattr(customer_row, key, value)

        customer_row.updated_by = "Lucas"

        for column in columns_changed:
            history = CustomersHistory(
                customer_id=customer_row.id,
                updated_by=customer_row.updated_by,
                column_change=column
            )
            db.add(history)

        try:
            db.commit()
            db.refresh(customer_row)
            db.close()

            return HTTPException(status_code=status.HTTP_200_OK, detail=f"Cliente: {customer_row.cpf_number} - {customer_row.full_name} atualizado com sucesso")
        
        except Exception as e:
            db.rollback()
            db.close()

            logger.error(f"Erro geral na atualização do cliente: {e}")
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro geral na atualização do cliente: {e}")
            
        
    @classmethod    
    def delete_customer(cls, cpf_number: str) -> None:
        """ Delete a single customer

        Args:
            cpf_number (str): 11 or 14 numbers for CPF or CNPJ

        Returns:
            Message of sucess
            
        Exceptions:
            400: General delete error
        """
        customer = CustomersQueries.get_customer_by_cpf(cpf_number=cpf_number)
        if not customer:
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente com CPF {cpf_number} não encontrado."
            )
        
        customer.updated_by = "Lucas"
        history = CustomersHistory(
                customer_id=customer.id,
                updated_by=customer.updated_by,
                column_change=f"{customer.cpf_number} Deleted"
            )
        
        try:
            db.delete(customer)
            db.add(history)
            db.commit()
            db.close()

            return HTTPException(status_code=status.HTTP_200_OK, detail=f"Cliente: {customer.cpf_number} - {customer.full_name} deletado com sucesso")
        
        except Exception as e:
            db.rollback()
            db.close()
            logger.error(f"Erro geral na exclusão do cliente: {e}")
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro geral na exclusão do cliente: {e}")
