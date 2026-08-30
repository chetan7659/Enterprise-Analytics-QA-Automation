import pytest


@pytest.fixture
def sample_sales():
    return [
        {
            "region": "India",
            "product": "Laptop",
            "sales": 50000
        },
        {
            "region": "India",
            "product": "Phone",
            "sales": 30000
        }
    ]


def test_sample_sales(sample_sales):
    assert len(sample_sales) == 2

    assert sample_sales[0]["region"] == "India"
    assert sample_sales[0]["product"] == "Laptop"
    assert sample_sales[0]["sales"] == 50000


def test_total_sales(sample_sales):
    total = sum(
        sale["sales"]
        for sale in sample_sales
    )

    assert total == 80000




def test_test_sales_data(test_sales_data):
    assert len(test_sales_data) == 7

    assert test_sales_data[0]["region"] == "India"
    assert test_sales_data[0]["product"] == "Keyboard"
    assert test_sales_data[0]["sales"] == 10000


def test_isolated_database(isolated_db):
    result = isolated_db.execute(
        "SELECT 1"
    ).fetchone()

    assert result[0] == 1    


def test_sales_table_exists(isolated_db):
    result = isolated_db.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name = 'sales'
        """
    ).fetchone()

    assert result is not None   



def test_populated_database(populated_db):
    result = populated_db.execute(
        "SELECT COUNT(*) FROM sales"
    ).fetchone()

    assert result[0] == 7


def test_populated_sales_values(populated_db):
    result = populated_db.execute(
        """
        SELECT sale_date, region, product, sales
        FROM sales
        ORDER BY id
        """
    ).fetchall()

    assert result[0] == (
        "2026-01-01",
        "India",
        "Keyboard",
        10000
    )

    assert result[1] == (
        "2026-01-10",
        "India",
        "Laptop",
        50000
    )

    assert result[2] == (
        "2026-01-20",
        "India",
        "Phone",
        30000
    )

    assert result[3] == (
        "2026-01-31",
        "India",
        "Mouse",
        15000
    )

    assert result[4] == (
        "2026-02-05",
        "India",
        "Monitor",
        40000
    )

    assert result[5] == (
        "2026-01-15",
        "USA",
        "Laptop",
        40000
    )

    assert result[6] == (
        "2026-02-10",
        "USA",
        "Phone",
        20000
    )


def test_sql_total_revenue(populated_db):
    result = populated_db.execute(
        """
        SELECT SUM(sales)
        FROM sales
        """
    ).fetchone()

    assert result[0] == 205000
