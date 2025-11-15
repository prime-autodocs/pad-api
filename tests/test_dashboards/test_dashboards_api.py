from fastapi.testclient import TestClient


def test_cards_summary_endpoint_ok(client: TestClient) -> None:
    resp = client.get("/dashboards/cards-summary")

    assert resp.status_code == 200
    body = resp.json()

    assert "total_customers" in body
    assert "total_vehicles" in body
    assert "new_customers_current_month" in body
    assert "services_current_month" in body


def test_new_customers_timeseries_monthly(client: TestClient) -> None:
    resp = client.get("/dashboards/new-customers", params={"period": "monthly"})

    assert resp.status_code == 200
    body = resp.json()

    assert body["period"] == "monthly"
    assert isinstance(body["points"], list)


