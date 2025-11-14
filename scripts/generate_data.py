"""
Synthetic e-commerce data generator.

This script produces five CSV files under the local `data/` directory:
 - products.csv
 - customers.csv
 - orders.csv
 - order_items.csv
 - reviews.csv

Use: `python generate_data.py`
"""

from __future__ import annotations

import random
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd

RANDOM_SEED = 42
NUM_PRODUCTS = 50
NUM_CUSTOMERS = 100
NUM_ORDERS = 500
MAX_ITEMS_PER_ORDER = 5
REVIEW_PROBABILITY = 0.6  # 60% of orders receive at least one review


def random_date(start: date, end: date) -> datetime:
    """Return a random datetime between start and end dates."""
    delta_days = (end - start).days
    random_days = random.randint(0, delta_days)
    # random hour/minute to vary within the day
    random_seconds = random.randint(0, 86399)
    return datetime.combine(start + timedelta(days=random_days), datetime.min.time()) + timedelta(
        seconds=random_seconds
    )


def create_products() -> pd.DataFrame:
    categories = [
        "Electronics",
        "Home",
        "Outdoors",
        "Sports",
        "Beauty",
        "Automotive",
        "Toys",
        "Fashion",
        "Books",
        "Grocery",
    ]
    adjectives = [
        "Premium",
        "Compact",
        "Eco",
        "Smart",
        "Classic",
        "Deluxe",
        "Lightweight",
        "Portable",
        "Advanced",
        "Essential",
    ]
    nouns = [
        "Speaker",
        "Backpack",
        "Bottle",
        "Lamp",
        "Watch",
        "Camera",
        "Shoes",
        "Notebook",
        "Headphones",
        "Mixer",
    ]

    rows = []
    for product_id in range(1, NUM_PRODUCTS + 1):
        category = random.choice(categories)
        name = f"{random.choice(adjectives)} {random.choice(nouns)}"
        cost = round(random.uniform(5, 80), 2)
        price = round(cost * random.uniform(1.2, 2.5), 2)
        rows.append(
            {
                "product_id": product_id,
                "name": name,
                "category": category,
                "price": price,
                "cost": cost,
                "active": random.choice([True, True, True, False]),  # mostly active
            }
        )
    return pd.DataFrame(rows)


def create_customers() -> pd.DataFrame:
    first_names = ["Alex", "Jordan", "Taylor", "Casey", "Morgan", "Riley", "Harper", "Dakota", "Emerson", "Hayden"]
    last_names = ["Smith", "Lee", "Garcia", "Patel", "Brown", "Chen", "Davis", "Martinez", "Lopez", "Wilson"]
    cities = ["New York", "San Francisco", "Chicago", "Austin", "Seattle", "Boston", "Atlanta", "Denver", "Miami", "Phoenix"]
    states = ["NY", "CA", "IL", "TX", "WA", "MA", "GA", "CO", "FL", "AZ"]
    base_date = date.today() - timedelta(days=365)

    rows = []
    for customer_id in range(1, NUM_CUSTOMERS + 1):
        first = random.choice(first_names)
        last = random.choice(last_names)
        signup = random_date(base_date, date.today())
        rows.append(
            {
                "customer_id": customer_id,
                "first_name": first,
                "last_name": last,
                "email": f"{first.lower()}.{last.lower()}{customer_id}@example.com",
                "city": random.choice(cities),
                "state": random.choice(states),
                "signup_date": signup.date().isoformat(),
                "loyalty_tier": random.choice(["Bronze", "Silver", "Gold", "Platinum"]),
            }
        )
    return pd.DataFrame(rows)


def create_orders(customers: pd.DataFrame) -> pd.DataFrame:
    statuses = ["pending", "processing", "completed", "shipped", "cancelled"]
    start_date = date.today() - timedelta(days=180)
    rows = []
    for order_id in range(1, NUM_ORDERS + 1):
        customer_id = int(customers.sample(1)["customer_id"].iloc[0])
        order_dt = random_date(start_date, date.today())
        status = random.choices(statuses, weights=[0.05, 0.2, 0.4, 0.3, 0.05])[0]
        rows.append(
            {
                "order_id": order_id,
                "customer_id": customer_id,
                "order_date": order_dt.isoformat(sep=" "),
                "order_status": status,
                "shipping_method": random.choice(["ground", "express", "pickup"]),
                "order_total": 0.0,  # placeholder, filled after items are generated
            }
        )
    return pd.DataFrame(rows)


def create_order_items(orders: pd.DataFrame, products: pd.DataFrame) -> pd.DataFrame:
    rows = []
    order_totals = {}
    item_id = 1

    for _, order in orders.iterrows():
        num_items = random.randint(1, MAX_ITEMS_PER_ORDER)
        product_choices = products.sample(num_items, replace=True)
        order_total = 0.0
        for _, product in product_choices.iterrows():
            quantity = random.randint(1, 4)
            unit_price = float(product["price"])
            line_total = round(unit_price * quantity, 2)
            rows.append(
                {
                    "order_item_id": item_id,
                    "order_id": int(order["order_id"]),
                    "product_id": int(product["product_id"]),
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "line_total": line_total,
                }
            )
            order_total += line_total
            item_id += 1
        order_totals[int(order["order_id"])] = round(order_total, 2)

    orders["order_total"] = orders["order_id"].map(order_totals).fillna(0.0)
    return pd.DataFrame(rows)


def create_reviews(orders: pd.DataFrame, order_items: pd.DataFrame) -> pd.DataFrame:
    review_rows = []
    review_id = 1
    start_date = date.today() - timedelta(days=180)
    for _, order in orders.iterrows():
        if random.random() > REVIEW_PROBABILITY:
            continue

        # Use the first product from the order for simplicity
        order_id = int(order["order_id"])
        items = order_items[order_items["order_id"] == order_id]
        if items.empty:
            continue
        product_id = int(items.sample(1)["product_id"].iloc[0])
        review_date = random_date(start_date, date.today()).isoformat(sep=" ")
        review_rows.append(
            {
                "review_id": review_id,
                "order_id": order_id,
                "product_id": product_id,
                "customer_id": int(order["customer_id"]),
                "rating": random.randint(1, 5),
                "review_date": review_date,
                "review_text": random.choice(
                    [
                        "Great quality and fast shipping.",
                        "Decent product for the price.",
                        "Exceeded expectations!",
                        "Not satisfied with the durability.",
                        "Would definitely recommend to friends.",
                    ]
                ),
            }
        )
        review_id += 1
    return pd.DataFrame(review_rows)


def main(output_dir: Path) -> None:
    random.seed(RANDOM_SEED)

    output_dir.mkdir(parents=True, exist_ok=True)
    products = create_products()
    customers = create_customers()
    orders = create_orders(customers)
    order_items = create_order_items(orders, products)
    reviews = create_reviews(orders, order_items)

    products.to_csv(output_dir / "products.csv", index=False)
    customers.to_csv(output_dir / "customers.csv", index=False)
    orders.to_csv(output_dir / "orders.csv", index=False)
    order_items.to_csv(output_dir / "order_items.csv", index=False)
    reviews.to_csv(output_dir / "reviews.csv", index=False)
    print(f"Generated data files in {output_dir}")


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[1]
    data_dir = project_root / "data"
    main(data_dir)

