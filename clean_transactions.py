from pathlib import Path
import pandas as pd


# File locations
raw_file = Path("data/raw/Online Retail.xlsx")
output_folder = Path("data/processed")
output_file = output_folder / "clean_sales_transactions.csv"

# Create the output folder if it does not exist
output_folder.mkdir(parents=True, exist_ok=True)

# Load the raw dataset
df = pd.read_excel(raw_file)

# Keep the original invoice number and create a text version
# This allows us to identify invoices beginning with "C".
df["InvoiceNoText"] = df["InvoiceNo"].astype(str).str.strip()
df["is_cancelled"] = df["InvoiceNoText"].str.startswith("C")

# Count rows before cleaning
rows_before = len(df)

# Apply our business rules
clean_df = df[
    (~df["is_cancelled"])
    & (df["Quantity"] > 0)
    & (df["UnitPrice"] > 0)
].copy()

# Calculate revenue for each transaction line
clean_df["Revenue"] = clean_df["Quantity"] * clean_df["UnitPrice"]

# Remove helper columns that are no longer needed
clean_df = clean_df.drop(columns=["InvoiceNoText", "is_cancelled"])

# Save the cleaned transaction-level dataset
clean_df.to_csv(output_file, index=False)

# Print a cleaning summary
print("=== CLEANING COMPLETE ===")
print(f"Rows before cleaning: {rows_before:,}")
print(f"Rows after cleaning: {len(clean_df):,}")
print(f"Rows removed: {rows_before - len(clean_df):,}")
print(f"Output file: {output_file}")
print(f"Total revenue: {clean_df['Revenue'].sum():,.2f}")

print("\n=== CLEANED DATA PREVIEW ===")
print(clean_df.head().to_string(index=False))

print("\n=== REMAINING MISSING VALUES ===")
print(clean_df.isna().sum())
