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
    def get_customer_by_cpf(cls, cpf_number: str):
        """Query for get a single client 

        Args:
            cpf_number (str): 11 or 14 numbers for CPF or CNPJ

        Returns:
            Model Object: Customer
        """
        return db.query(Customers).filter(Customers.cpf_number == cpf_number).first()