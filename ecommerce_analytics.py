# ============================================================
# E-Commerce Sales & Revenue Analytics
# Author: Reddy Shreya
# Tools: Python, SQLite (SQL), Pandas, Matplotlib
# ============================================================

import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
warnings.filterwarnings = lambda *a, **kw: None
import warnings
warnings.filterwarnings('ignore')

# ── 1. CREATE DATABASE & TABLES ─────────────────────────────
conn = sqlite3.connect(':memory:')
cur  = conn.cursor()

cur.executescript("""
CREATE TABLE IF NOT EXISTS products (
    product_id   INTEGER PRIMARY KEY,
    product_name TEXT,
    category     TEXT,
    unit_price   REAL
);

CREATE TABLE IF NOT EXISTS customers (
    customer_id  INTEGER PRIMARY KEY,
    customer_name TEXT,
    region       TEXT,
    segment      TEXT
);

CREATE TABLE IF NOT EXISTS orders (
    order_id     INTEGER PRIMARY KEY,
    customer_id  INTEGER,
    product_id   INTEGER,
    order_date   TEXT,
    quantity     INTEGER,
    discount     REAL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id)  REFERENCES products(product_id)
);
""")

# ── 2. POPULATE WITH SAMPLE DATA ────────────────────────────
np.random.seed(42)
categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books', 'Beauty']
regions    = ['South', 'West', 'North', 'East', 'Midwest']
segments   = ['Consumer', 'Corporate', 'Home Office']

products  = [(i, f'Product_{i}', np.random.choice(categories), round(np.random.uniform(10, 500), 2))
             for i in range(1, 201)]
customers = [(i, f'Customer_{i}', np.random.choice(regions), np.random.choice(segments))
             for i in range(1, 1001)]

dates = pd.date_range('2022-01-01', '2024-12-31', freq='D')
orders = []
for i in range(1, 500001):
    orders.append((
        i,
        np.random.randint(1, 1001),
        np.random.randint(1, 201),
        str(np.random.choice(dates).date()),
        np.random.randint(1, 20),
        round(np.random.uniform(0, 0.3), 2)
    ))

cur.executemany("INSERT INTO products VALUES (?,?,?,?)", products)
cur.executemany("INSERT INTO customers VALUES (?,?,?,?)", customers)
cur.executemany("INSERT INTO orders VALUES (?,?,?,?,?,?)", orders)
conn.commit()
print(f"Inserted {len(orders):,} order records into the database.")

# ── 3. SQL QUERIES ───────────────────────────────────────────

# Query 1: Total revenue by category
q1 = """
SELECT
    p.category,
    COUNT(o.order_id)                                     AS total_orders,
    SUM(o.quantity)                                       AS units_sold,
    ROUND(SUM(o.quantity * p.unit_price * (1 - o.discount)), 2) AS total_revenue
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;
"""

# Query 2: Revenue by region and segment
q2 = """
SELECT
    c.region,
    c.segment,
    ROUND(SUM(o.quantity * p.unit_price * (1 - o.discount)), 2) AS revenue
FROM orders o
JOIN products  p ON o.product_id  = p.product_id
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.region, c.segment
ORDER BY revenue DESC;
"""

# Query 3: Monthly revenue trend
q3 = """
SELECT
    SUBSTR(o.order_date, 1, 7)                            AS month,
    ROUND(SUM(o.quantity * p.unit_price * (1 - o.discount)), 2) AS monthly_revenue
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY month
ORDER BY month;
"""

# Query 4: Top 10 products by revenue
q4 = """
SELECT
    p.product_name,
    p.category,
    ROUND(SUM(o.quantity * p.unit_price * (1 - o.discount)), 2) AS revenue
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.product_id
ORDER BY revenue DESC
LIMIT 10;
"""

# Query 5: Average discount by category
q5 = """
SELECT
    p.category,
    ROUND(AVG(o.discount) * 100, 2) AS avg_discount_pct
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY avg_discount_pct DESC;
"""

df1 = pd.read_sql_query(q1, conn)
df2 = pd.read_sql_query(q2, conn)
df3 = pd.read_sql_query(q3, conn)
df4 = pd.read_sql_query(q4, conn)
df5 = pd.read_sql_query(q5, conn)

print("\n── Revenue by Category ──\n", df1)
print("\n── Top 10 Products ──\n", df4)
print("\n── Avg Discount by Category ──\n", df5)

# ── 4. VISUALIZATIONS ───────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.suptitle('E-Commerce Sales & Revenue Analytics — Reddy Shreya', fontsize=14, fontweight='bold')

# Revenue by category
df1.plot(x='category', y='total_revenue', kind='bar', ax=axes[0, 0],
         color='steelblue', edgecolor='black', legend=False)
axes[0, 0].set_title('Total Revenue by Category')
axes[0, 0].set_ylabel('Revenue ($)')
axes[0, 0].tick_params(axis='x', rotation=30)

# Monthly trend
df3['month'] = pd.to_datetime(df3['month'])
axes[0, 1].plot(df3['month'], df3['monthly_revenue'], color='#e74c3c', linewidth=1.5)
axes[0, 1].set_title('Monthly Revenue Trend')
axes[0, 1].set_ylabel('Revenue ($)')
axes[0, 1].tick_params(axis='x', rotation=30)

# Top 10 products
df4_top = df4.sort_values('revenue', ascending=True)
df4_top.plot(x='product_name', y='revenue', kind='barh', ax=axes[1, 0],
             color='#2ecc71', edgecolor='black', legend=False)
axes[1, 0].set_title('Top 10 Products by Revenue')
axes[1, 0].set_xlabel('Revenue ($)')

# Revenue by region (pivot)
pivot = df2.groupby('region')['revenue'].sum().sort_values(ascending=False)
pivot.plot(kind='bar', ax=axes[1, 1], color='#9b59b6', edgecolor='black')
axes[1, 1].set_title('Total Revenue by Region')
axes[1, 1].set_ylabel('Revenue ($)')
axes[1, 1].tick_params(axis='x', rotation=30)

plt.tight_layout()
plt.savefig('ecommerce_analytics.png', dpi=150, bbox_inches='tight')
plt.show()
print("Plot saved as ecommerce_analytics.png")

conn.close()
