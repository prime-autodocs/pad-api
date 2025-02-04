import json
from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from typing import List

from loguru import logger

from database.models.customers import Customers
from database.queries.customers import CustomersQueries
from database.queries.customers_history import CustomerHistoriesQueries
from interfaces.api.schemas.customers import CustomersBase, CustomerFinder
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
    def create_customer(cls, data: Customers) -> None:
        """ Create a single customer 

        Args:
            data (Customers): A model with customers atributes

        Returns:
            Message of success
            
        Exceptions:
            400: General create error
        """
        validation = customer_data_validation(payload=data)
        if not validation.get("is_valid"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=validation.get("errors"))
        data = data_formatter(payload=data)

        try:
            CustomersQueries.create_customer(data=data)
            return JSONResponse(status_code=status.HTTP_200_OK, content=f"Cliente: {data.tax_id} - {data.full_name} criado com sucesso")

        except Exception as e:
            logger.error(f"Erro geral no cadastro do cliente: {e}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro geral no cadastro do cliente: {e}")

    @classmethod    
    def update_customer(cls, customer_id: int, new_data: Customers) -> None:
        """ Update a single customer

        Args:
            tax_id (str): 11 or 14 numbers for CPF or CNPJ
            new_data (Customers): A model with customers atributes the will change

        Returns:
            Message of success
            
        Exceptions:
            400: General update error
        """
        validation = customer_data_validation(payload=new_data)
        if not validation.get("is_valid"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=validation.get("errors"))

        customer_row = CustomersQueries.get_customer_by_id(customer_id=customer_id)
        
        columns_changed = []
        for key, value in new_data:
            if hasattr(customer_row, key) and value is not None:
                current_value = getattr(customer_row, key)
                if current_value != value:
                    columns_changed.append(key)
                    setattr(customer_row, key, value)

        customer_row.updated_by = "Lucas"

        for column in columns_changed:
            CustomerHistoriesQueries.add_customer_history(data=customer_row, description=f"Column {column} changed")
            
        try:
            CustomersQueries.update_customer(new_data=customer_row)
            return JSONResponse(status_code=status.HTTP_200_OK, content=f"Cliente: {customer_row.tax_id} - {customer_row.full_name} atualizado com sucesso")
        
        except Exception as e:
            logger.error(f"Erro geral na atualização do cliente: {e}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro geral na atualização do cliente: {e}")
            
        
    @classmethod    
    def delete_customer(cls, customer_id: int) -> None:
        """ Delete a single customer

        Args:
            tax_id (str): 11 or 14 numbers for CPF or CNPJ

        Returns:
            Message of success
            
        Exceptions:
            400: General delete error
        """
        customer = CustomersQueries.get_customer_by_id(customer_id=customer_id)
        customer.updated_by = "Lucas"
        
        CustomerHistoriesQueries.add_customer_history(data=customer, description=f"customer {customer.tax_id} deleted")
       
        try:
            CustomersQueries.delete_customer(customer=customer)
            return JSONResponse(status_code=status.HTTP_200_OK, content=f"Cliente: {customer.tax_id} - {customer.full_name} deletado com sucesso")
        
        except Exception as e:
            logger.error(f"Erro geral na exclusão do cliente: {e}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro geral na exclusão do cliente: {e}")

    @classmethod
    def get_customer_by_tax_id(cls, tax_id: str) -> CustomerFinder:
        """ Get a single customer by Tax ID

        Args:
            customer_id (int): ID of customer

        Returns:
            CustomersBase: Object of a single customer with all atributes
        """
        customer = CustomersQueries.get_customer_by_tax_id(tax_id=tax_id)          
        return customer