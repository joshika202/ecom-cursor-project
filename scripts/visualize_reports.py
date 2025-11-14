"""
Visualization helper for the synthetic e-commerce dataset.

Generates bar charts for:
- Top 10 products by units sold
- Revenue per product category

Outputs a combined figure at `analysis/dashboards/charts.png`.

Use: `python visualize_reports.py`
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "db" / "ecom.db"
OUTPUT_PATH = PROJECT_ROOT / "analysis" / "dashboards" / "charts.png"


def fetch_dataframe(query: str) -> pd.DataFrame:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"SQLite database not found at {DB_PATH}. Run ingest_sqlite.py first.")
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(query, conn)


def ensure_output_dir() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)


def plot_top_products(ax: plt.Axes) -> None:
    df = fetch_dataframe(
        """
        SELECT
            p.name AS product_name,
            SUM(oi.quantity) AS units_sold
        FROM products p
        JOIN order_items oi ON oi.product_id = p.product_id
        GROUP BY p.product_id
        ORDER BY units_sold DESC
        LIMIT 10;
        """
    )
    if df.empty:
        ax.text(0.5, 0.5, "No data available", ha="center", va="center")
        ax.set_title("Top 10 Products by Units Sold")
        return

    ax.barh(df["product_name"], df["units_sold"], color="#4C72B0")
    ax.invert_yaxis()
    ax.set_xlabel("Units Sold")
    ax.set_title("Top 10 Products by Units Sold")


def plot_revenue_by_category(ax: plt.Axes) -> None:
    df = fetch_dataframe(
        """
        SELECT
            p.category,
            SUM(oi.line_total) AS revenue
        FROM products p
        JOIN order_items oi ON oi.product_id = p.product_id
        GROUP BY p.category
        ORDER BY revenue DESC;
        """
    )
    if df.empty:
        ax.text(0.5, 0.5, "No data available", ha="center", va="center")
        ax.set_title("Revenue by Category")
        return

    ax.bar(df["category"], df["revenue"], color="#55A868")
    ax.set_ylabel("Revenue ($)")
    ax.set_title("Revenue by Category")
    ax.tick_params(axis="x", labelrotation=45)
    for label in ax.get_xticklabels():
        label.set_horizontalalignment("right")


def main() -> None:
    ensure_output_dir()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    plot_top_products(ax1)
    plot_revenue_by_category(ax2)
    fig.tight_layout()
    fig.savefig(OUTPUT_PATH, dpi=150)
    plt.close(fig)
    print(f"Charts saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

