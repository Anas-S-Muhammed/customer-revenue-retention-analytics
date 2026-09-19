from pathlib import Path
import pandas as pd


file_path = ("data/raw/Online Retail.xlsx")
df = pd.read_excel(file_path)

print("=== DATASET SIZE ===")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")

print("\n=== CANCELLATION INVOICES ===")
cancelled = df["InvoiceNo"].astype(str).str.startswith("C")
print(f"Cancelled rows: {cancelled.sum():,}")
print(f"Cancellation percentage: {cancelled.mean() * 100:.2f}%")

print("\n=== NEGATIVE VALUES ===")
print(f"Negative quantities: {(df['Quantity'] < 0).sum():,}")
print(f"Zero quantities: {(df['Quantity'] == 0).sum():,}")
print(f"Negative prices: {(df['UnitPrice'] < 0).sum():,}")
print(f"Zero prices: {(df['UnitPrice'] == 0).sum():,}")

print("\n=== MISSING CUSTOMER IDs ===")
missing_customer = df["CustomerID"].isna()
print(f"Missing CustomerID rows: {missing_customer.sum():,}")
print(f"Missing CustomerID percentage: {missing_customer.mean() * 100:.2f}%")

print("\n=== DATE RANGE ===")
print(f"First transaction: {df['InvoiceDate'].min()}")
print(f"Last transaction: {df['InvoiceDate'].max()}")

print("\n=== COUNTRIES ===")
print(df["Country"].value_counts().head(15))

print("\n=== TOP PRODUCTS BY ROW COUNT ===")
print(df["Description"].value_counts().head(10))

print("\n=== NUMERICAL SUMMARY ===")
print(df[["Quantity", "UnitPrice"]].describe())