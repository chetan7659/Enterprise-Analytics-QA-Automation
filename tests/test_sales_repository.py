from app.repositories.sales_repository import (
    get_revenue_by_date_range,
    get_revenue_by_product,
    get_revenue_by_product_and_region,
    get_revenue_by_region,
    get_revenue_with_filters,
    get_total_revenue,
)

from tests.helpers.sql_validation import get_expected_revenue

import pytest


def test_india_laptop_revenue():
    actual = get_revenue_with_filters(
        region="India",
        product="Laptop"
    )

    expected = get_expected_revenue(
        region="India",
        product="Laptop"
    )

    assert actual == expected


def test_january_revenue():
    actual = get_revenue_with_filters(
        start_date="2026-01-01",
        end_date="2026-01-31"
    )

    expected = get_expected_revenue(
        start_date="2026-01-01",
        end_date="2026-01-31"
    )

    assert actual == expected


def test_january_india_laptop_revenue():
    actual = get_revenue_with_filters(
        start_date="2026-01-01",
        end_date="2026-01-31",
        region="India",
        product="Laptop"
    )

    expected = get_expected_revenue(
        start_date="2026-01-01",
        end_date="2026-01-31",
        region="India",
        product="Laptop"
    )

    assert actual == expected


def test_usa_phone_revenue_is_zero():
    result = get_revenue_with_filters(
        region="USA",
        product="Phone"
    )

    assert result == 0


def test_january_revenue():
    result = get_revenue_with_filters(
        start_date="2026-01-01",
        end_date="2026-01-31"
    )

    assert result == 80000


actual = get_revenue_with_filters(
    start_date="2026-02-01",
    end_date="2026-02-28"
)

expected = get_expected_revenue(
    start_date="2026-02-01",
    end_date="2026-02-28"
)

assert actual == expected


def test_january_laptop_revenue():
    result = get_revenue_with_filters(
        start_date="2026-01-01",
        end_date="2026-01-31",
        product="Laptop"
    )

    assert result == 50000


def test_january_india_laptop_revenue():
    result = get_revenue_with_filters(
        start_date="2026-01-01",
        end_date="2026-01-31",
        region="India",
        product="Laptop"
    )

    assert result == 50000


@pytest.mark.parametrize(
    "region, product",
    [
        ("India", "Laptop"),
        ("India", "Phone"),
        ("USA", "Laptop"),
    ]
)
def test_revenue_by_region_and_product(region, product):
    actual = get_revenue_with_filters(
        region=region,
        product=product
    )

    expected = get_expected_revenue(
        region=region,
        product=product
    )

    assert actual == expected


@pytest.mark.parametrize(
    "region, product, expected",
    [
        ("India", "Laptop", 50000),
        ("India", "Phone", 30000),
        ("USA", "Laptop", 70000),
        ("USA", "Phone", 0),
    ]
)
def test_revenue_by_region_and_product(
    region,
    product,
    expected
):
    actual = get_revenue_with_filters(
        region=region,
        product=product
    )

    assert actual == expected


@pytest.mark.parametrize(
    "region, product",
    [
        ("India", "Laptop"),
        ("India", "Phone"),
        ("USA", "Laptop"),
        ("USA", "Phone"),
    ]
)
def test_revenue_by_region_and_product(region, product):
    actual = get_revenue_with_filters(
        region=region,
        product=product
    )

    expected = get_expected_revenue(
        region=region,
        product=product
    )

    assert actual == expected


@pytest.mark.parametrize(
    "start_date, end_date",
    [
        ("2026-01-01", "2026-01-31"),
        ("2026-02-01", "2026-02-28"),
    ]
)
def test_revenue_by_date_range(start_date, end_date):
    actual = get_revenue_with_filters(
        start_date=start_date,
        end_date=end_date
    )

    expected = get_expected_revenue(
        start_date=start_date,
        end_date=end_date
    )

    assert actual == expected


@pytest.mark.parametrize(
    "start_date, end_date, region",
    [
        ("2026-01-01", "2026-01-31", "India"),
        ("2026-01-01", "2026-01-31", "USA"),
        ("2026-02-01", "2026-02-28", "India"),
        ("2026-02-01", "2026-02-28", "USA"),
    ]
)
def test_revenue_by_date_and_region(
    start_date,
    end_date,
    region
):
    actual = get_revenue_with_filters(
        start_date=start_date,
        end_date=end_date,
        region=region
    )

    expected = get_expected_revenue(
        start_date=start_date,
        end_date=end_date,
        region=region
    )

    assert actual == expected


@pytest.mark.parametrize(
    "start_date, end_date, region, product",
    [
        ("2026-01-01", "2026-01-31", "India", "Laptop"),
        ("2026-01-01", "2026-01-31", "India", "Phone"),
        ("2026-01-01", "2026-01-31", "USA", "Laptop"),
        ("2026-02-01", "2026-02-28", "India", "Monitor"),
    ]
)
def test_revenue_with_filters(
    start_date,
    end_date,
    region,
    product
):
    actual = get_revenue_with_filters(
        start_date=start_date,
        end_date=end_date,
        region=region,
        product=product
    )

    expected = get_expected_revenue(
        start_date=start_date,
        end_date=end_date,
        region=region,
        product=product
    )

    assert actual == expected


def test_database_connection(db_connection):
    row = db_connection.execute(
        "SELECT 1"
    ).fetchone()

    assert row[0] == 1


def test_repository_revenue_matches_sql(db_connection):
    sql_result = db_connection.execute(
        """
        SELECT SUM(sales)
        FROM sales
        """
    ).fetchone()

    expected_revenue = sql_result[0]

    actual_revenue = get_total_revenue(db_connection)

    assert actual_revenue == expected_revenue




def test_date_range_includes_start_date(populated_db):
    sql_result = populated_db.execute(
        """
        SELECT SUM(sales)
        FROM sales
        WHERE sale_date BETWEEN ? AND ?
        """,
        (
            "2026-01-01",
            "2026-01-01"
        )
    ).fetchone()

    expected_revenue = sql_result[0]

    actual_revenue = get_revenue_by_date_range(
        populated_db,
        "2026-01-01",
        "2026-01-01"
    )

    assert actual_revenue == expected_revenue



def test_date_range_includes_end_date(populated_db):
    sql_result = populated_db.execute(
        """
        SELECT SUM(sales)
        FROM sales
        WHERE sale_date BETWEEN ? AND ?
        """,
        (
            "2026-01-31",
            "2026-01-31"
        )
    ).fetchone()

    expected_revenue = sql_result[0]

    actual_revenue = get_revenue_by_date_range(
        populated_db,
        "2026-01-31",
        "2026-01-31"
    )

    assert actual_revenue == expected_revenue




def test_sql_returns_none_for_no_data_range(populated_db):
    result = populated_db.execute(
        """
        SELECT SUM(sales)
        FROM sales
        WHERE sale_date BETWEEN ? AND ?
        """,
        (
            "2026-03-01",
            "2026-03-31"
        )
    ).fetchone()

    assert result[0] is None    



def test_repository_returns_none_for_no_data_range(populated_db):
    actual_revenue = get_revenue_by_date_range(
        populated_db,
        "2026-03-01",
        "2026-03-31"
    )

    assert actual_revenue is None    




@pytest.mark.parametrize(
    "start_date, end_date",
    [
        ("2026-01-01", "2026-01-31"),
        ("2026-01-10", "2026-01-20"),
        ("2026-02-05", "2026-02-05"),
    ]
)
def test_date_range_matches_sql(
    populated_db,
    start_date,
    end_date
):
    sql_result = populated_db.execute(
        """
        SELECT SUM(sales)
        FROM sales
        WHERE sale_date BETWEEN ? AND ?
        """,
        (start_date, end_date)
    ).fetchone()

    expected_revenue = sql_result[0]

    actual_revenue = get_revenue_by_date_range(
        populated_db,
        start_date,
        end_date
    )

    assert actual_revenue == expected_revenue


def test_sql_region_revenue(populated_db):
    result = populated_db.execute(
        """
        SELECT SUM(sales)
        FROM sales
        WHERE region = ?
        """,
        ("India",)
    ).fetchone()

    assert result[0] == 145000


@pytest.mark.parametrize(
    "region",
    [
        "India",
        "USA",
    ]
)
def test_region_revenue_matches_sql(populated_db, region):
    sql_result = populated_db.execute(
        """
        SELECT SUM(sales)
        FROM sales
        WHERE region = ?
        """,
        (region,)
    ).fetchone()

    expected_revenue = sql_result[0]

    actual_revenue = get_revenue_by_region(
        populated_db,
        region
    )

    assert actual_revenue == expected_revenue



def test_sql_product_revenue(populated_db):
    result = populated_db.execute(
        """
        SELECT SUM(sales)
        FROM sales
        WHERE product = ?
        """,
        ("Laptop",)
    ).fetchone()

    assert result[0] == 90000   



@pytest.mark.parametrize(
    "product",
    [
        "Laptop",
        "Phone",
        "Keyboard",
        "Mouse",
        "Monitor",
    ]
)
def test_product_revenue_matches_sql(
    populated_db,
    product
):
    sql_result = populated_db.execute(
        """
        SELECT SUM(sales)
        FROM sales
        WHERE product = ?
        """,
        (product,)
    ).fetchone()

    expected_revenue = sql_result[0]

    actual_revenue = get_revenue_by_product(
        populated_db,
        product
    )

    assert actual_revenue == expected_revenue    








def test_sql_product_revenue(populated_db):
    result = populated_db.execute(
        """
        SELECT SUM(sales)
        FROM sales
        WHERE product = ?
        """,
        ("Laptop",)
    ).fetchone()

    assert result[0] == 90000






@pytest.mark.parametrize(
    "product",
    [
        "Laptop",
        "Phone",
        "Keyboard",
        "Mouse",
        "Monitor",
    ]
)
def test_product_revenue_matches_sql(
    populated_db,
    product
):
    sql_result = populated_db.execute(
        """
        SELECT SUM(sales)
        FROM sales
        WHERE product = ?
        """,
        (product,)
    ).fetchone()

    expected_revenue = sql_result[0]

    actual_revenue = get_revenue_by_product(
        populated_db,
        product
    )

    assert actual_revenue == expected_revenue



def test_sql_product_and_region_revenue(populated_db):
    result = populated_db.execute(
        """
        SELECT SUM(sales)
        FROM sales
        WHERE product = ?
        AND region = ?
        """,
        ("Laptop", "India")
    ).fetchone()

    assert result[0] == 50000    


@pytest.mark.parametrize(
    "product, region",
    [
        ("Laptop", "India"),
        ("Laptop", "USA"),
        ("Phone", "India"),
        ("Phone", "USA"),
    ]
)
def test_product_region_revenue_matches_sql(
    populated_db,
    product,
    region
):
    sql_result = populated_db.execute(
        """
        SELECT SUM(sales)
        FROM sales
        WHERE product = ?
        AND region = ?
        """,
        (product, region)
    ).fetchone()

    expected_revenue = sql_result[0]

    actual_revenue = get_revenue_by_product_and_region(
        populated_db,
        product,
        region
    )

    assert actual_revenue == expected_revenue






def test_sql_product_region_date_revenue(populated_db):
    result = populated_db.execute(
        """
        SELECT SUM(sales)
        FROM sales
        WHERE product = ?
        AND region = ?
        AND sale_date BETWEEN ? AND ?
        """,
        (
            "Laptop",
            "India",
            "2026-01-01",
            "2026-01-31"
        )
    ).fetchone()

    assert result[0] == 50000



def test_sql_revenue_by_region(populated_db):
    result = populated_db.execute(
        """
        SELECT region, SUM(sales)
        FROM sales
        GROUP BY region
        ORDER BY region
        """
    ).fetchall()

    assert result == [
        ("India", 145000),
        ("USA", 60000),
    ]




def test_sql_revenue_by_product(populated_db):
    result = populated_db.execute(
        """
        SELECT product, SUM(sales)
        FROM sales
        GROUP BY product
        ORDER BY product
        """
    ).fetchall()

    assert result == [
        ("Keyboard", 10000),
        ("Laptop", 90000),
        ("Monitor", 40000),
        ("Mouse", 15000),
        ("Phone", 50000),
    ]


def test_sql_total_revenue(populated_db):
    result = populated_db.execute(
        """
        SELECT SUM(sales)
        FROM sales
        """
    ).fetchone()

    assert result[0] == 205000


def test_sql_sales_count(populated_db):
    result = populated_db.execute(
        """
        SELECT COUNT(*)
        FROM sales
        """
    ).fetchone()

    assert result[0] == 7


def test_sql_average_sales(populated_db):
    result = populated_db.execute(
        """
        SELECT AVG(sales)
        FROM sales
        """
    ).fetchone()

    expected = 205000 / 7

    assert result[0] == pytest.approx(expected)


def test_sql_min_sales(populated_db):
    result = populated_db.execute(
        """
        SELECT MIN(sales)
        FROM sales
        """
    ).fetchone()

    assert result[0] == 10000


def test_sql_max_sales(populated_db):
    result = populated_db.execute(
        """
        SELECT MAX(sales)
        FROM sales
        """
    ).fetchone()

    assert result[0] == 50000


def test_sql_sales_count_by_region(populated_db):
    result = populated_db.execute(
        """
        SELECT region, COUNT(*)
        FROM sales
        GROUP BY region
        ORDER BY region
        """
    ).fetchall()

    assert result == [
        ("India", 5),
        ("USA", 2),
    ]


def test_sql_average_sales_by_region(populated_db):
    result = populated_db.execute(
        """
        SELECT region, AVG(sales)
        FROM sales
        GROUP BY region
        ORDER BY region
        """
    ).fetchall()

    india_average = (10000 + 50000 + 30000 + 15000 + 40000) / 5
    usa_average = (40000 + 20000) / 2

    assert result[0][0] == "India"
    assert result[0][1] == pytest.approx(india_average)
    assert result[1][0] == "USA"
    assert result[1][1] == pytest.approx(usa_average)


def test_sql_region_aggregation_summary(populated_db):
    result = populated_db.execute(
        """
        SELECT
            region,
            COUNT(*),
            SUM(sales),
            AVG(sales),
            MIN(sales),
            MAX(sales)
        FROM sales
        GROUP BY region
        ORDER BY region
        """
    ).fetchall()

    assert result[0][0] == "India"
    assert result[0][1] == 5
    assert result[0][2] == 145000
    assert result[0][3] == pytest.approx(29000)
    assert result[0][4] == 10000
    assert result[0][5] == 50000

    assert result[1][0] == "USA"
    assert result[1][1] == 2
    assert result[1][2] == 60000
    assert result[1][3] == pytest.approx(30000)
    assert result[1][4] == 20000
    assert result[1][5] == 40000


def test_sql_revenue_by_region_and_product(populated_db):
    result = populated_db.execute(
        """
        SELECT region, product, SUM(sales)
        FROM sales
        GROUP BY region, product
        ORDER BY region, product
        """
    ).fetchall()

    assert result == [
        ("India", "Keyboard", 10000),
        ("India", "Laptop", 50000),
        ("India", "Monitor", 40000),
        ("India", "Mouse", 15000),
        ("India", "Phone", 30000),
        ("USA", "Laptop", 40000),
        ("USA", "Phone", 20000),
    ]


def test_sql_product_revenue_for_india(populated_db):
    result = populated_db.execute(
        """
        SELECT product, SUM(sales)
        FROM sales
        WHERE region = ?
        GROUP BY product
        ORDER BY product
        """,
        ("India",)
    ).fetchall()

    assert result == [
        ("Keyboard", 10000),
        ("Laptop", 50000),
        ("Monitor", 40000),
        ("Mouse", 15000),
        ("Phone", 30000),
    ]




def test_revenue_by_region_visualization_data(populated_db):
    rows = populated_db.execute(
        """
        SELECT region, SUM(sales)
        FROM sales
        GROUP BY region
        ORDER BY region
        """
    ).fetchall()

    result = {
        row[0]: row[1]
        for row in rows
    }

    assert result["India"] == 145000
    assert result["USA"] == 60000




def test_region_chart_data_contract(client):
    """Test that revenue by region returns proper contract for charting"""
    response = client.get("/analytics/revenue-by-region")

    assert response.status_code == 200

    data = response.json()

    # Verify structure
    assert "metric" in data
    assert "data" in data

    # Verify it's a list of regions
    assert isinstance(data["data"], list)

    # Check each region entry
    for item in data["data"]:
        assert "region" in item
        assert "revenue" in item
        assert isinstance(item["revenue"], (int, float))


def test_revenue_by_region_sql_expected(populated_db):
    result = populated_db.execute(
        """
        SELECT region, SUM(sales) AS revenue
        FROM sales
        GROUP BY region
        ORDER BY region
        """
    ).fetchall()

    expected = [
        ("India", 145000),
        ("USA", 60000),
    ]

    assert result == expected

