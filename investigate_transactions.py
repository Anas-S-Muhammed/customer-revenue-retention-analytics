from pathlib import Path
import pandas as pd

file_path = Path("data/raw/Online Retail.xlsx")
df = pd.read_excel(file_path)

df["InvoiceNoText"] = df["InvoiceNo"].astype(str)

print("=== CANCELLATION EXAMPLES ===")
cancelled = df[df["InvoiceNoText"].str.startswith("C")]
print(cancelled.head(10).to_string(index=False))

print("\n=== NEGATIVE QUANTITY EXAMPLES ===")
negative_quantity = df[df["Quantity"] < 0]
print(negative_quantity.head(10).to_string(index=False))

print("\n=== ZERO-PRICE EXAMPLES ===")
zero_price = df[df["UnitPrice"] == 0]
print(zero_price.head(10).to_string(index=False))

print("\n=== NEGATIVE-PRICE EXAMPLES ===")
negative_price = df[df["UnitPrice"] < 0]
print(negative_price.to_string(index=False))

print("\n=== LARGE QUANTITY EXAMPLES ===")
large_quantity = df[df["Quantity"] > 1000]
print(large_quantity.to_string(index=False))

print("\n=== LARGE PRICE EXAMPLES ===")
large_price = df[df["UnitPrice"] > 1000]
print(large_price.head(20).to_string(index=False))
