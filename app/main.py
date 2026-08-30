from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database import get_connection
from app.repositories.sales_repository import (
    get_all_sales,
    get_total_revenue,
    get_revenue_by_region as fetch_revenue_by_region,
    get_revenue_by_product as fetch_revenue_by_product,
    get_revenue_by_product_for_region,
    get_revenue_by_product_for_region_and_product,
    get_revenue_with_filters,
)
app = FastAPI(title="Enterprise Analytics QA Platform")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
def get_revenue(region: str | None = None):
    revenue = get_revenue_with_filters(region=region)

    return {
        "metric": "total_revenue",
        "value": revenue
    }

@app.get("/analytics/revenue-by-region")
def get_revenue_by_region(region: str | None = None):
    if region:
        revenue = fetch_revenue_by_region(region=region)
        if revenue is None:
            data = []
        else:
            data = [{"region": region, "revenue": revenue}]
    else:
        data = fetch_revenue_by_region()

    return {
        "metric": "revenue_by_region",
        "data": data
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
    elif product:
        # Filter by product only
        all_products = fetch_revenue_by_product()
        data = [item for item in all_products if item["product"] == product]
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

app.mount("/dashboard", StaticFiles(directory="frontend", html=True), name="frontend")