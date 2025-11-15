from fastapi import status, HTTPException

from database.models.customers import Customers
from database.models.customers_history import CustomersHistory
from database.session import db_session


class CustomerHistoriesQueries:

    table = CustomersHistory

    @classmethod
    def add_customer_history(cls, data: Customers, description: str):
        history = CustomersHistory(
            customer_id=data.id,
            updated_by=data.updated_by,
            description=description,
        )
        with db_session() as db:
            db.add(history)
            db.commit()