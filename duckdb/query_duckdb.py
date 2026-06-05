show_tables = """
     SHOW TABLES
     """
bronze_sales =  "SELECT *     FROM bronze_sales  LIMIT 10"
bronze_customers=  "SELECT *     FROM bronze_customers LIMIT 10"
bronze_products =  "SELECT *     FROM bronze_products LIMIT 10"

import duckdb

conn = duckdb.connect("../duckdb/retail.duckdb")

df = conn.execute(
    
    show_tables
    
).fetchdf()

print(df)