from fastapi import APIRouter
from typing import List

from core.customers import Customer
from interfaces.api.schemas.customers import (
    CustomersBase,
    CustomerCreateWithDetails,
    CustomerUpdate,
    CustomerFinder,
)

router = APIRouter()

@router.get(
    "/"
)
async def get_all_customers() -> List[CustomersBase]:
    """Endpoint that bring a list of all Customers

    Returns:
        List[CustomersBase]: A list of customers objects with all atributes
    """
    response = Customer.get_all_customers()
    return response

@router.get(
    "/{customer_id}"
)
async def get_customer_by_id(customer_id: int) -> CustomersBase:
    """Endpoint that bring a single customer by ID

    Args:
        customer_id (int): ID of customer

    Returns:
        CustomersBase: Object of a single customer with all atributes
    """
    response = Customer.get_customer_by_id(customer_id=customer_id)
    return response

@router.post(
    "/"
)
async def create_customer(
    data: CustomerCreateWithDetails
) -> None:
    """Endpoint that create a customer in database

    Args:
        data (CustomerCreateWithDetails): Receive a model data of customer to create customer

    Returns:
        Message of success
        
    Exceptions:
        400: General create error
    """
    response = Customer.create_customer(data=data)
    return response

@router.patch(
    "/{customer_id}"
)
async def update_customer(
    customer_id: int,
    new_data: CustomerUpdate
) -> None:
    """Endpoint that update a customer in database

    Args:
        customer_id (int): ID of customer
        new_data (CustomerUpdate): Receive a model data of customer to update customer

    Returns:
        Message of success
        
    Exceptions:
        400: General create error
    """
    response = Customer.update_customer(customer_id=customer_id, new_data=new_data)
    return response

@router.delete(
    "/{customer_id}"
)
async def delete_customer(
    customer_id: int
) -> None:
    """Endpoint that delete a customer in database

    Args:
        customer_id (int): ID of customer

    Returns:
        _type_: _description_
    """
    response = Customer.delete_customer(customer_id=customer_id)
    return response

@router.get(
    "/tax_id/{tax_id}"
)
async def get_customer_by_tax_id(
    tax_id: str
) -> CustomerFinder:
    """Endpoint that bring a single customer by Tax ID

    Args:
        tax_id (str): 11 or 14 numbers for CPF or CNPJ

    Returns:
        CustomerFinder: Model with tax_id, full_name and tel_number
    """
    response = Customer.get_customer_by_tax_id(tax_id=tax_id)
    return response