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


# ============================================================================
# STEP 45: ECHARTS TOOLTIP, LEGEND & AXIS VALIDATION
# ============================================================================

def test_step45_simulate_tooltip_data_india(client):
    response = client.get("/analytics/revenue-by-region", params={"region": "India"})
    api_data = response.json()["data"]
    tooltip_data = [{"name": item["region"], "value": item["revenue"]} for item in api_data]
    assert len(tooltip_data) == 1
    assert tooltip_data[0]["name"] == "India"
    assert tooltip_data[0]["value"] > 0

def test_step45_simulate_tooltip_data_usa(client):
    response = client.get("/analytics/revenue-by-region", params={"region": "USA"})
    api_data = response.json()["data"]
    tooltip_data = [{"name": item["region"], "value": item["revenue"]} for item in api_data]
    assert len(tooltip_data) == 1
    assert tooltip_data[0]["name"] == "USA"
    assert tooltip_data[0]["value"] > 0

def test_step45_simulate_tooltip_after_filter(client):
    response = client.get("/analytics/revenue-by-region", params={"region": "India"})
    api_data = response.json()["data"]
    names_in_data = [item["region"] for item in api_data]
    assert "India" in names_in_data
    assert "USA" not in names_in_data

def test_step45_validate_legend_and_series_name(client):
    response = client.get("/analytics/revenue-by-region")
    data = response.json()
    assert data["metric"] == "revenue_by_region"
    for item in data["data"]:
        assert "revenue" in item