import pytest
from playwright.sync_api import Page, expect

pytestmark = pytest.mark.e2e


BASE_URL = "http://127.0.0.1:8000/dashboard/"

def get_expected_revenue(db_connection, region=None):
    """Independent SQL Oracle to determine expected values."""
    cursor = db_connection.cursor()
    if region:
        cursor.execute("SELECT SUM(sales) FROM sales WHERE region = ?", (region,))
    else:
        cursor.execute("SELECT SUM(sales) FROM sales")
    result = cursor.fetchone()[0]
    return result if result is not None else 0

def test_india_filter_updates_dashboard(page: Page, db_connection):
    page.goto(BASE_URL)
    
    expected_revenue = get_expected_revenue(db_connection, "India")
    
    # Intercept the API request
    with page.expect_response("**/analytics/revenue-by-region?region=India") as response_info:
        page.locator("#region-filter").select_option("India")
        
    response = response_info.value
    assert response.ok
    
    # API Verification
    api_data = response.json()
    assert api_data["data"][0]["revenue"] == expected_revenue
    
    # ECharts State Verification
    page.wait_for_function(f"window.revenueChart && window.revenueChart.getOption().xAxis[0].data[0] === 'India'")
    chart_option = page.evaluate("() => window.revenueChart.getOption()")
    
    assert chart_option["xAxis"][0]["data"] == ["India"]
    assert chart_option["series"][0]["data"] == [expected_revenue]


def test_usa_filter_updates_dashboard(page: Page, db_connection):
    page.goto(BASE_URL)
    
    expected_revenue = get_expected_revenue(db_connection, "USA")
    
    # Intercept the API request
    with page.expect_response("**/analytics/revenue-by-region?region=USA") as response_info:
        page.locator("#region-filter").select_option("USA")
        
    response = response_info.value
    assert response.ok
    
    # API Verification
    api_data = response.json()
    assert api_data["data"][0]["revenue"] == expected_revenue
    
    # ECharts State Verification
    page.wait_for_function(f"window.revenueChart && window.revenueChart.getOption().xAxis[0].data[0] === 'USA'")
    chart_option = page.evaluate("() => window.revenueChart.getOption()")
    
    assert chart_option["xAxis"][0]["data"] == ["USA"]
    assert chart_option["series"][0]["data"] == [expected_revenue]


def test_reset_filter_restores_data(page: Page, db_connection):
    page.goto(BASE_URL)
    
    # 1. Select India
    with page.expect_response("**/analytics/revenue-by-region?region=India"):
        page.locator("#region-filter").select_option("India")
        
    page.wait_for_function(f"window.revenueChart && window.revenueChart.getOption().xAxis[0].data.length === 1")
    
    # 2. Reset to All Regions (value="")
    with page.expect_response("**/analytics/revenue-by-region"):
        page.locator("#region-filter").select_option("")
        
    page.wait_for_function(f"window.revenueChart && window.revenueChart.getOption().xAxis[0].data.length > 1")
    
    chart_option = page.evaluate("() => window.revenueChart.getOption()")
    regions = chart_option["xAxis"][0]["data"]
    
    assert "India" in regions
    assert "USA" in regions


def test_filter_and_chart_type_switch_preserves_data(page: Page, db_connection):
    page.goto(BASE_URL)
    
    expected_revenue = get_expected_revenue(db_connection, "India")
    
    # Select India
    with page.expect_response("**/analytics/revenue-by-region?region=India"):
        page.locator("#region-filter").select_option("India")
        
    page.wait_for_function(f"window.revenueChart && window.revenueChart.getOption().xAxis[0].data[0] === 'India'")
    
    # Switch to Line
    page.locator("button[data-type='line']").click()
    page.wait_for_function("window.revenueChart.getOption().series[0].type === 'line'")
    
    chart_option = page.evaluate("() => window.revenueChart.getOption()")
    assert chart_option["xAxis"][0]["data"] == ["India"]
    assert chart_option["series"][0]["data"] == [expected_revenue]
    
    # Switch to Pie
    page.locator("button[data-type='pie']").click()
    page.wait_for_function("window.revenueChart.getOption().series[0].type === 'pie'")
    
    chart_option = page.evaluate("() => window.revenueChart.getOption()")
    pie_data = chart_option["series"][0]["data"]
    
    assert len(pie_data) == 1
    assert pie_data[0]["name"] == "India"
    assert pie_data[0]["value"] == expected_revenue
