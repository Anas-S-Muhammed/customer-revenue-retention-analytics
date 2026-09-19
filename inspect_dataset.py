from pathlib import Path
import pandas as pd

file_path = Path("data/raw/Online Retail.xlsx")

if not file_path.exists():
    print(f"File not found: {file_path}")
    print("check the filename and folder location.")
    raise SystemExit

df = pd.read_excel(file_path)

print("Dataset loaded successfully.")
print(f"Rows: {df.shape[0]:,}")
print(f"Columns: {df.shape[1]}")

print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst five rows:")
print(df.head())

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isna().sum())

print("\nBasic statistics:")
print(df.describe(include="all").transpose())