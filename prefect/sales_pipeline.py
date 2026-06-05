from prefect import flow, task
import pandas as pd
import duckdb
import subprocess
import logging
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DBT_DIR = PROJECT_ROOT / "retail_dbt"

print(DBT_DIR)


# ==========================================
# CONFIGURATION
# ==========================================

DB_PATH = "../duckdb/retail.duckdb"

logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ==========================================
# TASK 1 - LOAD BRONZE LAYER
# ==========================================

@task(
    name="Load Bronze Layer",
    retries=2,
    retry_delay_seconds=10
)
def load_bronze():

    logging.info("Loading CSV files into Bronze Layer")

    conn = duckdb.connect(DB_PATH)

    sales = pd.read_csv("../data/sales.csv")
    customers = pd.read_csv("../data/customers.csv")
    products = pd.read_csv("../data/products.csv")
    
    
    conn.execute("""
    CREATE OR REPLACE TABLE bronze_sales AS
    SELECT * FROM read_csv_auto('../data/sales.csv')
    """)

    conn.execute("""
    CREATE OR REPLACE TABLE bronze_customers AS
    SELECT * FROM read_csv_auto('../data/customers.csv')
    """)

    conn.execute("""
    CREATE OR REPLACE TABLE bronze_products AS
    SELECT * FROM read_csv_auto('../data/products.csv')
    """)
    conn.close()

    logging.info("Bronze Layer Loaded Successfully")

    print("Bronze Layer Loaded")


# ==========================================
# TASK 2 - RUN DBT MODELS
# ==========================================

@task(
    name="Run dbt Build"
)
def run_dbt():

    logging.info("Running dbt build")

    result = subprocess.run(
        ["dbt", "build"],
        cwd=str(DBT_DIR),
        capture_output=True,
        text=True
    )

    print(result.stdout)

    if result.returncode != 0:
        logging.error(result.stderr)
        raise Exception("dbt build failed")

    logging.info("dbt build completed")


# ==========================================
# TASK 3 - RUN DATA QUALITY TESTS
# ==========================================

@task(
    name="Run Data Quality Tests"
)
def run_tests():

    logging.info("Running dbt tests")

    result = subprocess.run(
        ["dbt", "test"],
        cwd=str(DBT_DIR),
        capture_output=True,
        text=True
    )

    print(result.stdout)

    if result.returncode != 0:
        logging.error(result.stderr)
        raise Exception("dbt tests failed")

    logging.info("All tests passed")


# ==========================================
# TASK 4 - GENERATE REPORT
# ==========================================

@task(
    name="Generate Summary Report"
)
def generate_report():

    conn = duckdb.connect(DB_PATH)

    report = conn.execute("""

        SELECT
            COUNT(*) AS total_orders,
            ROUND(SUM(sales_amount),2) AS total_revenue,
            ROUND(AVG(sales_amount),2) AS avg_order_value

        FROM fact_sales

    """).fetchdf()

    Path("reports").mkdir(exist_ok=True)

    report.to_csv(
        "reports/sales_summary.csv",
        index=False
    )

    print("\n========== SALES SUMMARY ==========")
    print(report)

    conn.close()

    logging.info("Report Generated")


# ==========================================
# TASK 5 - TOP PRODUCTS REPORT
# ==========================================

@task(
    name="Generate Top Products Report"
)
def top_products_report():

    conn = duckdb.connect(DB_PATH)

    report = conn.execute("""

        SELECT
            product_name,
            SUM(quantity) AS units_sold,
            ROUND(SUM(sales_amount),2) AS revenue

        FROM fact_sales

        GROUP BY product_name

        ORDER BY revenue DESC

        LIMIT 10

    """).fetchdf()

    report.to_csv(
        "reports/top_products.csv",
        index=False
    )

    print("\n========== TOP PRODUCTS ==========")
    print(report)

    conn.close()

    logging.info("Top Product Report Generated")


# ==========================================
# TASK 6 - PIPELINE AUDIT
# ==========================================

@task(
    name="Pipeline Audit"
)
def pipeline_audit():

    conn = duckdb.connect(DB_PATH)

    conn.execute("""

        CREATE TABLE IF NOT EXISTS pipeline_audit (

            run_timestamp TIMESTAMP,
            status VARCHAR

        )

    """)

    conn.execute("""

        INSERT INTO pipeline_audit
        VALUES (
            CURRENT_TIMESTAMP,
            'SUCCESS'
        )

    """)

    conn.close()

    logging.info("Audit Record Inserted")


# ==========================================
# MAIN FLOW
# ==========================================

@flow(
    name="sales-medallion-pipeline",
    log_prints=True
)
def sales_pipeline():

    load_bronze()

    run_dbt()

    run_tests()

    generate_report()

    top_products_report()

    pipeline_audit()

    print("\nPipeline Completed Successfully")


# ==========================================
# ENTRY POINT
# ==========================================

if __name__ == "__main__":

    sales_pipeline()
