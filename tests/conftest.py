from typing import Any

import pytest
import sqlite3
from fastapi.testclient import TestClient
from app.database import get_connection
from app.main import app


@pytest.fixture
def client():
    """Fixture providing FastAPI test client for API testing"""
    return TestClient(app)


@pytest.fixture
def db_connection():
    # setup
    connection = get_connection()

    # give connection to test
    yield connection

    # cleanup
    connection.close()


@pytest.fixture
def test_sales_data():
    return [
        {
            "sale_date": "2026-01-01",
            "region": "India",
            "product": "Keyboard",
            "sales": 10000
        },
        {
            "sale_date": "2026-01-10",
            "region": "India",
            "product": "Laptop",
            "sales": 50000
        },
        {
            "sale_date": "2026-01-20",
            "region": "India",
            "product": "Phone",
            "sales": 30000
        },
        {
            "sale_date": "2026-01-31",
            "region": "India",
            "product": "Mouse",
            "sales": 15000
        },
        {
            "sale_date": "2026-02-05",
            "region": "India",
            "product": "Monitor",
            "sales": 40000
        },
        {
    "sale_date": "2026-01-15",
    "region": "USA",
    "product": "Laptop",
    "sales": 40000
        },
       {
    "sale_date": "2026-02-10",
    "region": "USA",
    "product": "Phone",
    "sales": 20000
       },
    ]

@pytest.fixture
def isolated_db():
    connection = sqlite3.connect(":memory:")

    connection.execute(
        """
        CREATE TABLE sales (
            id INTEGER PRIMARY KEY,
            sale_date TEXT NOT NULL,
            region TEXT NOT NULL,
            product TEXT NOT NULL,
            sales REAL NOT NULL
        )
        """
    )

    yield connection

    connection.close()


@pytest.fixture
def populated_db(isolated_db: sqlite3.Connection, test_sales_data: list[dict[str, Any]]):
    for sale in test_sales_data:
        isolated_db.execute(
            """
            INSERT INTO sales (
                sale_date,
                region,
                product,
                sales
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                sale["sale_date"],
                sale["region"],
                sale["product"],
                sale["sales"]
            )
        )

    isolated_db.commit()

    return isolated_db