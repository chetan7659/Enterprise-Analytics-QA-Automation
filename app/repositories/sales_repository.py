from app.database import get_connection


def get_all_sales():
    connection = get_connection()

    cursor = connection.execute(
        """
        SELECT
            transaction_id,
            date,
            region,
            product,
            sales,
            cost,
            profit,
            quantity
        FROM sales
        """
    )

    rows = cursor.fetchall()
    connection.close()

    sales = []

    for row in rows:
        sales.append({
            "transaction_id": row[0],
            "date": row[1],
            "region": row[2],
            "product": row[3],
            "sales": row[4],
            "cost": row[5],
            "profit": row[6],
            "quantity": row[7]
        })

    return sales


def get_total_revenue(connection):
    cursor = connection.execute(
        """
        SELECT SUM(sales)
        FROM sales
        """
    )

    result = cursor.fetchone()

    return result[0]


def get_revenue_by_region(connection=None, region=None):
    should_close = connection is None
    if connection is None:
        connection = get_connection()

    if region is not None:
        cursor = connection.execute(
            """
            SELECT SUM(sales)
            FROM sales
            WHERE region = ?
            """,
            (region,)
        )
        row = cursor.fetchone()

        if should_close:
            connection.close()

        return row[0] if row and row[0] is not None else None

    cursor = connection.execute(
        """
        SELECT
            region,
            SUM(sales)
        FROM sales
        GROUP BY region
        ORDER BY region
        """
    )

    rows = cursor.fetchall()

    if should_close:
        connection.close()

    revenue_by_region = []

    for row in rows:
        revenue_by_region.append({
            "region": row[0],
            "revenue": row[1]
        })

    return revenue_by_region


def get_revenue_by_product(connection=None, product=None):
    should_close = connection is None
    if connection is None:
        connection = get_connection()

    if product is not None:
        cursor = connection.execute(
            """
            SELECT SUM(sales)
            FROM sales
            WHERE product = ?
            """,
            (product,)
        )
        row = cursor.fetchone()

        if should_close:
            connection.close()

        return row[0] if row and row[0] is not None else None

    cursor = connection.execute(
        """
        SELECT
            product,
            SUM(sales)
        FROM sales
        GROUP BY product
        ORDER BY product
        """
    )
    rows = cursor.fetchall()

    if should_close:
        connection.close()

    revenue_by_product = []

    for row in rows:
        revenue_by_product.append({
            "product": row[0],
            "revenue": row[1]
        })

    return revenue_by_product


def get_revenue_by_product_for_region(region):
    connection = get_connection()

    cursor = connection.execute(
        """
        SELECT
            product,
            SUM(sales)
        FROM sales
        WHERE region = ?
        GROUP BY product
        ORDER BY product
        """,
        (region,)
    )

    rows = cursor.fetchall()
    connection.close()

    revenue_by_product = []

    for row in rows:
        revenue_by_product.append({
            "product": row[0],
            "revenue": row[1]
        })

    return revenue_by_product


def get_revenue_by_product_and_region(connection=None, product=None, region=None):
    should_close = connection is None
    if connection is None:
        connection = get_connection()

    cursor = connection.execute(
        """
        SELECT SUM(sales)
        FROM sales
        WHERE product = ?
        AND region = ?
        """,
        (product, region)
    )

    row = cursor.fetchone()

    if should_close:
        connection.close()

    return row[0] if row and row[0] is not None else None


def get_revenue_by_product_for_region_and_product(region, product):
    connection = get_connection()

    cursor = connection.execute(
        """
        SELECT
            product,
            SUM(sales)
        FROM sales
        WHERE region = ?
        AND product = ?
        GROUP BY product
        ORDER BY product
        """,
        (region, product)
    )

    rows = cursor.fetchall()
    connection.close()

    revenue = []

    for row in rows:
        revenue.append({
            "product": row[0],
            "revenue": row[1]
        })

    return revenue


def get_revenue_by_date_range(connection, start_date, end_date):
    cursor = connection.execute(
        """
        SELECT
            SUM(sales)
        FROM sales
        WHERE sale_date >= ?
        AND sale_date <= ?
        """,
        (start_date, end_date)
    )

    row = cursor.fetchone()

    if row is None or row[0] is None:
        return None

    return row[0]


def get_revenue_with_filters(
    start_date=None,
    end_date=None,
    region=None,
    product=None
):
    connection = get_connection()

    query = """
        SELECT SUM(sales)
        FROM sales
        WHERE 1 = 1
    """

    parameters = []

    if start_date:
        query += " AND sale_date >= ?"
        parameters.append(start_date)

    if end_date:
        query += " AND sale_date <= ?"
        parameters.append(end_date)

    if region:
        query += " AND region = ?"
        parameters.append(region)

    if product:
        query += " AND product = ?"
        parameters.append(product)

    cursor = connection.execute(
        query,
        parameters
    )

    row = cursor.fetchone()

    connection.close()

    return row[0] or 0