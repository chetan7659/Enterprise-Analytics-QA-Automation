from fastapi import FastAPI
from app.database import get_connection
from app.repositories.sales_repository import (
    get_all_sales,
    get_total_revenue,
    get_revenue_by_region as fetch_revenue_by_region,
    get_revenue_by_product as fetch_revenue_by_product,
    get_revenue_by_product_for_region,
    get_revenue_by_product_for_region_and_product,
)
app = FastAPI(title="Enterprise Analytics QA Platform")


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "application": "Enterprise Analytics QA Platform"
    }


@app.get("/sales")
def get_sales():
    sales = get_all_sales()

    return {
        "count": len(sales),
        "data": sales
    }

@app.get("/analytics/revenue")
def get_revenue():
    connection = get_connection()

    try:
        revenue = get_total_revenue(connection)

        return {
            "metric": "total_revenue",
            "value": revenue
        }

    finally:
        connection.close()

@app.get("/analytics/revenue-by-region")
def get_revenue_by_region():
    revenue_by_region = fetch_revenue_by_region()

    return {
        "metric": "revenue_by_region",
        "data": revenue_by_region
    }



@app.get("/analytics/revenue-by-product")
def get_revenue_by_product(
    region: str | None = None,
    product: str | None = None
):
    if region and product:
        data = get_revenue_by_product_for_region_and_product(
            region,
            product
        )
    elif region:
        data = get_revenue_by_product_for_region(region)
    else:
        data = fetch_revenue_by_product()

    return {
        "metric": "revenue_by_product",
        "filters": {
            "region": region,
            "product": product
        },
        "data": data
    }