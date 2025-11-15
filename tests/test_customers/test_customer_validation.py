import datetime

from database.models.customers import Customers
from services.enums import CustomerTypeEnum, CivilStatusEnum, GenderEnum, TaxTypeEnum
from services.utils.customer_validation import customer_data_validation


def _make_customer(
    *,
    full_name: str = "Joao da Silva",
    tax_id: str = "12345678909",
) -> Customers:
    return Customers(
        tax_type=TaxTypeEnum.CPF,
        tax_id=tax_id,
        full_name=full_name,
        gender=GenderEnum.male,
        email="joao@example.com",
        birth_date=datetime.date(1990, 1, 1),
        customer_type=CustomerTypeEnum.DETRAN,
        civil_status=CivilStatusEnum.single,
        tel_number="21999999999",
    )


def test_customer_validation_ok() -> None:
    customer = _make_customer()

    result = customer_data_validation(payload=customer)

    assert result["is_valid"] is True
    assert result["errors"] == []


def test_customer_validation_rejects_invalid_email() -> None:
    customer = _make_customer()
    customer.email = "email-invalido"

    result = customer_data_validation(payload=customer)

    assert result["is_valid"] is False
    assert any("Email inválido" in e for e in result["errors"])


def test_customer_validation_requires_full_name_with_two_words() -> None:
    customer = _make_customer(full_name="Joao")

    result = customer_data_validation(payload=customer)

    assert result["is_valid"] is False
    assert any("Nome completo deve conter pelo menos duas palavras" in e for e in result["errors"])


