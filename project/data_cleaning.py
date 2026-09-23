from pathlib import Path
import pandas as pd

# Project folders
project_dir = Path("D:\sales-analysis-performance\data\raw\retail_sales.csv").resolve().parent.parent
raw_file = project_dir / "data" / "raw" / "retail_sales.csv"
cleaned_file = project_dir / "data" / "cleaned" / "cleaned_retail_sales.csv"

# Load raw data
df = pd.read_csv("../data/raw/retail_sales.csv")

# 1. Remove duplicate orders
df = df.drop_duplicates(subset="OrderID", keep="first")

# 2. Convert OrderDate to date format
df["OrderDate"] = pd.to_datetime(df["OrderDate"], errors="coerce")

# 3. Convert numeric columns to numeric data types
numeric_columns = ["Sales", "Profit", "Quantity", "Discount"]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# 4. Handle missing values
# Remove rows where key values are missing
df = df.dropna(subset=["OrderID", "OrderDate", "CustomerID", "Sales", "Profit"])

# Replace missing category/text values with "Unknown"
text_columns = [
    "CustomerName", "Segment", "Region", "State",
    "Category", "SubCategory", "Product",
    "PaymentMethod", "ShipMode"
]

for column in text_columns:
    df[column] = df[column].fillna("Unknown")

# Replace missing Quantity and Discount values
df["Quantity"] = df["Quantity"].fillna(0)
df["Discount"] = df["Discount"].fillna(0)

# 5. Create ProfitMargin column
df["ProfitMargin"] = 0.0
df.loc[df["Sales"] != 0, "ProfitMargin"] = (
    df.loc[df["Sales"] != 0, "Profit"]
    / df.loc[df["Sales"] != 0, "Sales"]
) * 100

df["ProfitMargin"] = df["ProfitMargin"].round(2)

# Save cleaned data
cleaned_file.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(cleaned_file, index=False)

print("Data cleaning completed.")
print("Cleaned rows:", len(df))
print("Saved file:", cleaned_file)
print("Data cleaning process finished successfully.")
print("Cleaned rows:", len(df))
print("Saved file:", cleaned_file)


