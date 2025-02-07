from fastapi import status, HTTPException

from database.models.customers import Customers
from database.models.customers_history import CustomersHistory
from database.database import db

class CustomerHistoriesQueries():
    
    table = CustomersHistory
    
    @classmethod
    def add_customer_history(cls, data: Customers, description: str):
        history = CustomersHistory(
            customer_id=data.id,
            updated_by=data.updated_by,
            description=description
        )
        db.add(history)