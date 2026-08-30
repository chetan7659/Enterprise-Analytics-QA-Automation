from app.database import get_connection


def get_expected_revenue(
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