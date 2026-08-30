from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert data["application"] == "Enterprise Analytics QA Platform"


def test_get_sales():
    response = client.get("/sales")

    assert response.status_code == 200

    data = response.json()

    assert "count" in data
    assert "data" in data

    assert data["count"] == len(data["data"])


def test_total_revenue():
    response = client.get("/analytics/revenue")

    assert response.status_code == 200

    data = response.json()

    assert data["metric"] == "total_revenue"
    assert data["value"] == 210000


def test_revenue_by_region():
    response = client.get("/analytics/revenue-by-region")

    assert response.status_code == 200

    data = response.json()

    assert data["metric"] == "revenue_by_region"
    assert "data" in data


def test_revenue_by_product():
    response = client.get("/analytics/revenue-by-product")

    assert response.status_code == 200

    data = response.json()

    assert data["metric"] == "revenue_by_product"
    assert data["filters"]["region"] is None
    assert data["filters"]["product"] is None
    assert "data" in data


def test_revenue_by_product_for_region():
    response = client.get(
        "/analytics/revenue-by-product",
        params={
            "region": "India"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["metric"] == "revenue_by_product"
    assert data["filters"]["region"] == "India"
    assert data["filters"]["product"] is None
    assert "data" in data


def test_revenue_by_product_for_region_and_product():
    response = client.get(
        "/analytics/revenue-by-product",
        params={
            "region": "India",
            "product": "Laptop"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["metric"] == "revenue_by_product"
    assert data["filters"]["region"] == "India"
    assert data["filters"]["product"] == "Laptop"
    assert "data" in data