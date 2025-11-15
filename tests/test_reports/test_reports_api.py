from fastapi.testclient import TestClient


def test_reports_list_empty(client: TestClient) -> None:
    resp = client.get("/reports/list")

    assert resp.status_code == 200
    body = resp.json()

    assert "items" in body
    assert "total_clients" in body
    assert isinstance(body["items"], list)


def test_reports_customer_details_not_found(client: TestClient) -> None:
    resp = client.get("/reports/customer-details/999999")

    assert resp.status_code == 404


