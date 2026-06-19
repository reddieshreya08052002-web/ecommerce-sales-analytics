# 🛒 E-Commerce Sales & Revenue Analytics

**Author:** Reddy Shreya  
**Tools:** Python · SQLite (SQL) · Pandas · Matplotlib · Seaborn  
**Domain:** Retail / Business Intelligence

---

## 🎯 Project Overview

This project builds a **star-schema relational database** of 500,000+ e-commerce transactions and uses **40+ SQL queries** to extract KPIs including revenue by category, region, product, and time period.

---

## 📁 Project Structure

```
ecommerce-sales-analytics/
│
├── ecommerce_analytics.py   # SQL queries + visualization pipeline
├── ecommerce_analytics.png  # Multi-panel dashboard output
├── queries/
│   ├── revenue_by_category.sql
│   ├── monthly_trend.sql
│   ├── top_products.sql
│   ├── region_segment.sql
│   └── discount_analysis.sql
├── requirements.txt
└── README.md
```

---

## 🔍 SQL Queries Included

| Query | Description |
|-------|-------------|
| Revenue by Category | Total orders, units sold, and revenue per category |
| Monthly Revenue Trend | Revenue aggregated by month (2022–2024) |
| Top 10 Products | Highest revenue-generating SKUs |
| Region & Segment | Revenue breakdown by geography and customer type |
| Discount Analysis | Average discount percentage by category |

---

## 📈 Key Business Insights

- **Electronics** drives the highest revenue but carries the highest discount rate
- **South region** consistently outperforms other regions
- Revenue peaks in **Q4** every year — ideal for promotions
- Top 10 products contribute ~18% of total revenue (Pareto principle)

---

## 🚀 How to Run

```bash
pip install -r requirements.txt
python ecommerce_analytics.py
```

---

## 🛠️ Requirements

See `requirements.txt`
