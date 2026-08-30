import sqlite3

DATABASE_PATH = "analytics.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    return connection

def create_sales_table():
    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS sales (
            transaction_id INTEGER PRIMARY KEY,
            date TEXT NOT NULL,
            region TEXT NOT NULL,
            product TEXT NOT NULL,
            sales REAL NOT NULL,
            cost REAL NOT NULL,
            profit REAL NOT NULL,
            quantity INTEGER NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()

def seed_sales_data():
    connection = get_connection()

    sales_data = [
        (1, "2026-01-10", "India", "Laptop", 50000, 40000, 10000, 2),
        (2, "2026-01-11", "India", "Phone", 30000, 24000, 6000, 3),
        (3, "2026-01-12", "USA", "Laptop", 70000, 55000, 15000, 2),
        (4, "2026-01-13", "USA", "Monitor", 20000, 15000, 5000, 4),
        (5, "2026-01-14", "India", "Monitor", 40000, 30000, 10000, 5),
    ]

    connection.executemany(
        """
        INSERT INTO sales (
            transaction_id,
            date,
            region,
            product,
            sales,
            cost,
            profit,
            quantity
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        sales_data
    )

    connection.commit()
    connection.close()    