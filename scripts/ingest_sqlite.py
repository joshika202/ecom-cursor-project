"""
SQLite ingestion script for the synthetic e-commerce dataset.

Assumes CSVs were generated with `generate_data.py` and placed under `data/`.
Creates an `ecom.db` SQLite database, defines tables, and bulk loads the CSVs
using pandas.

Use: `python ingest_sqlite.py`
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = PROJECT_ROOT / "db" / "ecom.db"


def load_csv(name: str) -> pd.DataFrame:
    path = DATA_DIR / f"{name}.csv"
    if not path.exists():
        raise FileNotFoundError(f"CSV not found: {path}. Run generate_data.py first.")
    return pd.read_csv(path)


def create_tables(conn: sqlite3.Connection) -> None:
    """Drop and recreate tables with explicit typing."""
    cursor = conn.cursor()

    cursor.executescript(
        """
        PRAGMA foreign_keys = ON;

        DROP TABLE IF EXISTS reviews;
        DROP TABLE IF EXISTS order_items;
        DROP TABLE IF EXISTS orders;
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS customers;

        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            cost REAL NOT NULL,
            active INTEGER NOT NULL
        );

        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            city TEXT NOT NULL,
            state TEXT NOT NULL,
            signup_date TEXT NOT NULL,
            loyalty_tier TEXT NOT NULL
        );

        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            order_status TEXT NOT NULL,
            shipping_method TEXT NOT NULL,
            order_total REAL NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        );

        CREATE TABLE order_items (
            order_item_id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            line_total REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        );

        CREATE TABLE reviews (
            review_id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            customer_id INTEGER NOT NULL,
            rating INTEGER NOT NULL,
            review_date TEXT NOT NULL,
            review_text TEXT NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id),
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        );
        """
    )
    conn.commit()


def bulk_insert(conn: sqlite3.Connection) -> None:
    """Load each CSV via pandas and insert into SQLite."""
    dataframes = {
        "products": load_csv("products"),
        "customers": load_csv("customers"),
        "orders": load_csv("orders"),
        "order_items": load_csv("order_items"),
        "reviews": load_csv("reviews"),
    }

    for table, df in dataframes.items():
        df.to_sql(table, conn, if_exists="append", index=False)
        print(f"Inserted {len(df)} rows into {table}")


def main() -> None:
    if not DATA_DIR.exists():
        raise FileNotFoundError(f"Data directory not found at {DATA_DIR}. Run generate_data.py first.")

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()
        print(f"Existing database removed: {DB_PATH}")

    with sqlite3.connect(DB_PATH) as conn:
        create_tables(conn)
        bulk_insert(conn)
        print(f"SQLite database created at {DB_PATH}")


if __name__ == "__main__":
    main()

