from fastapi.testclient import TestClient

from services.enums import CustomerTypeEnum, CivilStatusEnum, GenderEnum, TaxTypeEnum


def _make_customer_payload() -> dict:
    return {
        "tax_type": TaxTypeEnum.CPF.value,
        "tax_id": "12345678909",
        "full_name": "Joao da Silva",
        "gender": GenderEnum.male.value,
        "email": "joao@example.com",
        "birth_date": "1990-01-01",
        "customer_type": CustomerTypeEnum.DETRAN.value,
        "civil_status": CivilStatusEnum.single.value,
        "tel_number": "21999999999",
        "address": {
            "address": "Rua X",
            "number": "123",
            "neighborhood": "Centro",
            "city": "Rio de Janeiro",
            "state": "RJ",
            "zip_code": "20000-000",
        },
        "documents": {
            "identity_number": "1234567",
            "identity_org": "DETRAN",
        },
    }


def test_create_and_get_customer_flow(client: TestClient) -> None:
    # Cria o customer
    payload = _make_customer_payload()
    create_resp = client.post("/customers/", json=payload)

    assert create_resp.status_code == 200

    # Lista clientes e garante que o novo está presente
    list_resp = client.get("/customers/")
    assert list_resp.status_code == 200
    customers = list_resp.json()

    assert any(c["tax_id"] == payload["tax_id"] for c in customers)


