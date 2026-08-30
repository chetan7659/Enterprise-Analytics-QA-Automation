import sqlite3

conn = sqlite3.connect('analytics.db')
print('USA-Laptop:', conn.execute("SELECT SUM(sales) FROM sales WHERE region='USA' AND product='Laptop'").fetchone())
print('USA-Phone:', conn.execute("SELECT SUM(sales) FROM sales WHERE region='USA' AND product='Phone'").fetchone())
print('\nAll USA by product:')
print(conn.execute("SELECT product, SUM(sales) FROM sales WHERE region='USA' GROUP BY product ORDER BY product").fetchall())
print('\nAll India by product:')
print(conn.execute("SELECT product, SUM(sales) FROM sales WHERE region='India' GROUP BY product ORDER BY product").fetchall())
conn.close()
