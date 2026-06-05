# Project 1 (Sales Data Medallion Architecture)
import duckdb

duckdb.connect("../duckdb/retail.duckdb")

print("Database created successfully")