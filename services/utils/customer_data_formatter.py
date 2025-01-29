from database.models.customers import Customers

def data_formatter(payload: Customers) -> Customers: 

    if payload.full_name != payload.full_name.title():
        payload.full_name = payload.full_name.title()

    if payload.email != payload.email.lower():
        payload.email = payload.email.lower()



    return payload