print("SCRIPT STARTED")

from pathlib import Path
import sqlite3
import pandas as pd

# Project directory
project_dir = Path(r"D:\sales-analysis-performance")

# File paths
csv_file = project_dir / "data" / "raw" / "retail_sales.csv"
sql_file = project_dir / "SQL" / "sql" / "create_tables.sql"
database_file = project_dir / "retail_sales.db"

# Check paths
print("CSV:", csv_file)
print("SQL:", sql_file)
print("CSV exists:", csv_file.exists())
print("SQL exists:", sql_file.exists())

# Read CSV
df = pd.read_csv(csv_file)

print("CSV loaded successfully!")
print("Rows:", len(df))

# Connect to SQLite
with sqlite3.connect(database_file) as connection:

    # Create table
    connection.executescript(
        sql_file.read_text(encoding="utf-8")
    )

    # Insert data
    df.to_sql(
        "retail_orders",
        connection,
        if_exists="append",
        index=False
    )

    # Check number of rows
    result = pd.read_sql_query(
        "SELECT COUNT(*) AS TotalRows FROM retail_orders",
        connection
    )

print("Database created:", database_file)
print(result)
print("SCRIPT FINISHED")