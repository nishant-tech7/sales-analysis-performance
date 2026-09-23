from pathlib import Path
import sqlite3
import pandas as pd

# Project folder
project_dir = Path(r"D:\sales-analysis-performance").resolve()

# Files
database_file = project_dir / "retail_sales.db"
query_file = project_dir / "SQL" / "sql" / "analysis_queries.sql"

# Check files
print("Database:", database_file)
print("SQL file:", query_file)

# Read SQL queries
queries = query_file.read_text(encoding="utf-8").split(";")

# Run queries
with sqlite3.connect(database_file) as connection:
    for number, query in enumerate(queries, start=1):
        if query.strip():
            print(f"\n--- Query {number} ---")
            result = pd.read_sql_query(query, connection)
            print(result)