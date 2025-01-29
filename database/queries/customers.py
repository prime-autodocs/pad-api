from database.models.customers import Customers
from database.database import db

class CustomersQueries():
    
    table = Customers
    
    @classmethod
    def get_all_customers(cls):
        return db.query(Customers).all()
    
    @classmethod
    def get_customer_by_cpf(cls, cpf_number: str):
        return db.query(Customers).filter(Customers.cpf_number == cpf_number).first()