import pytest
from playwright.sync_api import Page, expect

BASE_URL = "http://127.0.0.1:8000/dashboard/"

def test_dashboard_loads(page: Page):
    page.goto(BASE_URL)
    # The title of the HTML page
    expect(page).to_have_title("Enterprise Analytics QA Platform")

def test_revenue_chart_is_visible(page: Page):
    page.goto(BASE_URL)
    chart = page.locator("#revenue-chart")
    expect(chart).to_be_visible()

def test_region_filter_exists(page: Page):
    page.goto(BASE_URL)
    
    # Locate all options under the select dropdown
    options = page.locator("#region-filter option").all_text_contents()
    
    assert "India" in options
    assert "USA" in options
    assert "All Regions" in options

def test_chart_type_controls_visible(page: Page):
    page.goto(BASE_URL)
    
    # Assert each button is visible
    expect(page.locator("button.btn-tab[data-type='bar']")).to_be_visible()
    expect(page.locator("button.btn-tab[data-type='line']")).to_be_visible()
    expect(page.locator("button.btn-tab[data-type='pie']")).to_be_visible()
