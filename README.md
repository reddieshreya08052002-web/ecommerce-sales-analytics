# E-Commerce Sales & Revenue Analytics

**Tools:** Python, SQLite, Pandas, Matplotlib, Seaborn
**Domain:** Retail / Business Intelligence

---

This project started with a question I kept seeing in retail analytics: which parts of the business are actually driving revenue, and which ones just look busy? To answer it properly I needed a database I could query freely, so I built a star-schema SQLite database from 500K+ synthetic e-commerce transactions and wrote 40+ SQL queries against it.

The queries range from straightforward aggregations (revenue by category, top products by SKU) to more layered analysis — discount sensitivity by segment, quarterly seasonality patterns, and region-level performance gaps that wouldn't show up in a flat export.

---

## What the data showed

- Electronics leads on total revenue but also carries the highest average discount rate, which compresses margins significantly — the category looks better on the top line than it is on the bottom
- The South region outperformed other regions consistently across all three years in the dataset, not just in total volume but in average order value
- Revenue peaks sharply in Q4 every year; the effect is strong enough that Q4 alone accounts for a disproportionate share of annual revenue, making it the obvious window for promotions and inventory planning
- The top 10 products by revenue make up around 18% of total sales — a fairly classic Pareto distribution that held up across categories

---

## Project structure

```
ecommerce-sales-analytics/
├── ecommerce_analytics.py     # SQL query pipeline + visualization
├── ecommerce_analytics.png    # multi-panel dashboard output
├── ecommerce_requirements.txt
└── README.md
```

---

## Running it

```bash
pip install -r ecommerce_requirements.txt
python ecommerce_analytics.py
```

Builds the SQLite database in memory, runs all queries, and saves the dashboard chart.

---

## Skills demonstrated

SQL (window functions, aggregations, joins) · Star schema design · Python + SQLite · EDA · Retail KPI analysis
