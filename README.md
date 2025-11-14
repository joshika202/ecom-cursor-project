# E-commerce Synthetic Data Exercise(Cursor IDE – A-SDLC Assignment)

This project demonstrates an end-to-end data workflow implemented using **Cursor IDE, **Python**, and SQLite, Pandas,Matplotlib.
The assignment involved generating synthetic e-commerce data, ingesting it into a SQLite database, and writing SQL queries that join multiple tables to produce meaningful insights.

The entire solution follows a clean project structure, clear prompts, and reproducible code — designed exactly as required in the assignment instructions.



## Requirements

- Python 3.10+
- `pip install -r requirements.txt`

## Workflow

1. **Generate CSV data**

   ```bash
   python scripts/generate_data.py
   ```

   Writes `products`, `customers`, `orders`, `order_items`, and `reviews` CSVs into `data/`.

2. **Ingest into SQLite**

   ```bash
   python scripts/ingest_sqlite.py
   ```

   Creates `db/ecom.db`, defines all tables, and bulk loads the CSVs.

3. **Run example analytical queries**

   ```bash
   python scripts/query_run.py
   ```

   Prints:
   - Top 10 customers by revenue
   - Top 10 products by units sold
   - 10 most recent order line items

4. **Generate dashboards**

   ```bash
   python scripts/visualize_reports.py
   ```

   Produces `analysis/dashboards/charts.png` with product and category insights.

## Directory Layout

```
ecom-cursor-project/
├── analysis/
│   └── dashboards/
│       └── charts.png
├── data/
├── db/
│   └── ecom.db
├── requirements.txt
├── README.md
├── .gitignore
└── scripts/
    ├── generate_data.py
    ├── ingest_sqlite.py
    ├── query_run.py
    └── visualize_reports.py
```
##Prompts
Here is a **clean, ready-to-paste bullet list** for your README:

---

### **Project Requirements**

* Create a new project skeleton for an e-commerce synthetic data exercise.
* Add these runnable Python files: **generate_data.py**, **ingest_sqlite.py**, **query_run.py**, and **README.md**.
* **generate_data.py** must generate five CSV files with realistic synthetic data:

  * `products.csv`
  * `customers.csv`
  * `orders.csv`
  * `order_items.csv`
  * `reviews.csv`
* The dataset should contain: **50 products**, **100 customers**, **500 orders**, and reviews for some orders.
* **ingest_sqlite.py** should:

  * Create a SQLite database named **ecom.db**
  * Define appropriate tables and schema
  * Bulk-import all generated CSV files
* **query_run.py** should execute at least **three SQL queries** involving multiple table joins:

  * Top 10 customers by revenue
  * Top 10 products by units sold
  * Recent orders with customer and product details
* Only use: **Python standard libraries**, **pandas**, and **sqlite3**.
* All scripts must be **self-contained, modular, and well-commented**.




## Notes

- All scripts rely only on the Python standard library plus `pandas`, `sqlite3`, and `matplotlib`.
- Adjust dataset sizes via constants in `scripts/generate_data.py`.
- `analysis/advanced_queries.sql` contains more in-depth SQL examples for notebooks or BI tools.

##Pictuers

![generate_data output](pic/ScreenShot-1)

