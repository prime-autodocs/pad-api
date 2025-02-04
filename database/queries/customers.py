from fastapi import status, HTTPException

from database.models.customers import Customers
from database.database import db

class CustomersQueries():
    
    table = Customers
    
    @classmethod
    def get_all_customers(cls):
        """Query for get all customers

        Returns:
            Model Object: List[Customers]
        """
        return db.query(Customers).all()
    
    @classmethod
    def get_customer_by_id(cls, customer_id: int):
        """Query for get a single client by customer_id

        Args:
            customer_id (int): ID of the customer in database

        Returns:
            Model Object: Customer
        """
        customer = db.query(Customers).filter(Customers.id == customer_id).first()
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente não encontrado."
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
        customer = db.query(Customers).filter(Customers.tax_id == tax_id).first()
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente não encontrado."
            )
        return customer
    
    @classmethod
    def create_customer(cls, data: Customers):
        """Query to create a customer in database

        Args:
            customer (Customers): A model object of customer
        """
        customer = Customers(
            tax_type=data.tax_type,
            tax_id=data.tax_id,
            full_name=data.full_name,
            gender=data.gender,
            email=data.email,
            birth_date=data.birth_date,
            customer_type=data.customer_type,
            civil_status=data.civil_status,
            tel_number=data.tel_number,
        )
        
        db.add(customer)
    
    @classmethod
    def update_customer(cls, new_data: Customers):
        db.commit()
        db.refresh(new_data)
        db.close()
        
    @classmethod
    def delete_customer(cls, customer: Customers):
        db.delete(customer)

            