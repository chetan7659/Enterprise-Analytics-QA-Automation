import pytest
from fastapi.testclient import TestClient

from app.main import app

pytestmark = pytest.mark.api



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


# ============================================================================
# STEP 46: DASHBOARD INTEGRATION
# ============================================================================

def test_step46_kpi_syncs_with_filter(client):
    # Fetch KPI for India
    kpi_res = client.get("/analytics/revenue", params={"region": "India"})
    kpi_val = kpi_res.json()["value"]

    # Fetch Chart Data for India
    chart_res = client.get("/analytics/revenue-by-region", params={"region": "India"})
    chart_val = sum([item["revenue"] for item in chart_res.json()["data"]])

    assert kpi_val == chart_val

def test_step46_dashboard_state_consistency(client, db_connection):
    # SQL oracle for India
    cursor = db_connection.execute("SELECT SUM(sales) FROM sales WHERE region = 'India'")
    sql_val = cursor.fetchone()[0]

    # API KPI
    kpi_res = client.get("/analytics/revenue", params={"region": "India"})
    api_kpi_val = kpi_res.json()["value"]

    # API Chart
    chart_res = client.get("/analytics/revenue-by-region", params={"region": "India"})
    api_chart_val = sum([item["revenue"] for item in chart_res.json()["data"]])

    # Assert Dashboard Consistency
    assert sql_val == api_kpi_val == api_chart_val

def test_step46_kpi_reset(client):
    # KPI without filter (reset)
    kpi_res = client.get("/analytics/revenue")
    kpi_total = kpi_res.json()["value"]

    # KPI with filter
    kpi_india = client.get("/analytics/revenue", params={"region": "India"}).json()["value"]
    kpi_usa = client.get("/analytics/revenue", params={"region": "USA"}).json()["value"]

    assert kpi_total > kpi_india
    assert kpi_total > kpi_usa
    assert kpi_total >= (kpi_india + kpi_usa)
