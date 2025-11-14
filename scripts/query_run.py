"""
SQL query runner for the synthetic e-commerce SQLite database.

Use: `python query_run.py`

Expects that `ingest_sqlite.py` has been executed and produced `ecom.db`.
Runs three analytical queries and prints concise tables to stdout.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

DB_PATH = Path(__file__).resolve().parents[1] / "db" / "ecom.db"


def run_query(conn: sqlite3.Connection, sql: str, description: str) -> pd.DataFrame:
    """Execute a SQL query and return a DataFrame with a heading."""
    print(f"\n=== {description} ===")
    df = pd.read_sql_query(sql, conn)
    if df.empty:
        print("No rows returned.")
        return df

    # Show up to 10 rows for readability
    print(df.head(10).to_string(index=False))
    return df


def main() -> None:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"SQLite database not found at {DB_PATH}. Run ingest_sqlite.py first.")

    with sqlite3.connect(DB_PATH) as conn:
        run_query(
            conn,
            """
            SELECT
                c.customer_id,
                c.first_name || ' ' || c.last_name AS customer_name,
                c.loyalty_tier,
                SUM(o.order_total) AS total_revenue
            FROM customers c
            JOIN orders o ON o.customer_id = c.customer_id
            GROUP BY c.customer_id
            ORDER BY total_revenue DESC
            LIMIT 10;
            """,
            "Top 10 customers by revenue",
        )

        run_query(
            conn,
            """
            SELECT
                p.product_id,
                p.name,
                p.category,
                SUM(oi.quantity) AS units_sold,
                SUM(oi.line_total) AS revenue
            FROM products p
            JOIN order_items oi ON oi.product_id = p.product_id
            GROUP BY p.product_id
            ORDER BY units_sold DESC
            LIMIT 10;
            """,
            "Top 10 products by units sold",
        )

        run_query(
            conn,
            """
            SELECT
                o.order_id,
                o.order_date,
                c.first_name || ' ' || c.last_name AS customer_name,
                p.name AS product_name,
                oi.quantity,
                oi.line_total
            FROM orders o
            JOIN customers c ON c.customer_id = o.customer_id
            JOIN order_items oi ON oi.order_id = o.order_id
            JOIN products p ON p.product_id = oi.product_id
            ORDER BY o.order_date DESC
            LIMIT 10;
            """,
            "10 most recent order line items",
        )


if __name__ == "__main__":
    main()

