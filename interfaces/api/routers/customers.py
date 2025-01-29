from fastapi import APIRouter
from typing import List
from core.customers import Customer
from interfaces.api.schemas.customers import CustomersBase, CustomerCreate, CustomerUpdate, CustomerDelete

router = APIRouter()

@router.get(
    "/"
)
async def get_all_customers() -> List[CustomersBase]:
    response = Customer.get_all_customers()
    return response

@router.get(
    "/{cpf_number}"
)
async def get_customer_by_cpf(cpf_number: str) -> CustomersBase:
    response = Customer.get_customer_by_cpf_number(cpf_number=cpf_number)
    return response

@router.post(
    "/"
)
async def create_customer(
    data: CustomerCreate
) -> None:
    response = Customer.create_customer(data=data)
    return response

@router.patch(
    "/{cpf_number}"
)
async def update_customer(
    cpf_number: str,
    new_data: CustomerUpdate
) -> None:
    response = Customer.update_customer(cpf_number=cpf_number, new_data=new_data)
    return response

@router.delete(
    "/{cpf_number}"
)
async def delete_customer(
    cpf_number: str
) -> None:
    response = Customer.delete_customer(cpf_number=cpf_number)
    return response