from pathlib import Path
import pandas as pd


# -----------------------------
# 1. File paths
# -----------------------------
input_file = Path("data/processed/clean_sales_transactions.csv")
reports_folder = Path("reports")
report_file = reports_folder / "data_quality_report.txt"
customer_file = Path("data/processed/customer_transactions.csv")

reports_folder.mkdir(parents=True, exist_ok=True)


# -----------------------------
# 2. Load cleaned data
# -----------------------------
df = pd.read_csv(
    input_file,
    parse_dates=["InvoiceDate"]
)

print("=== CLEANED DATA LOADED ===")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")


# -----------------------------
# 3. Run data-quality checks
# -----------------------------
checks = {}

checks["duplicate_rows"] = int(df.duplicated().sum())
checks["missing_invoice_numbers"] = int(df["InvoiceNo"].isna().sum())
checks["missing_product_codes"] = int(df["StockCode"].isna().sum())
checks["missing_descriptions"] = int(df["Description"].isna().sum())
checks["missing_customer_ids"] = int(df["CustomerID"].isna().sum())
checks["missing_dates"] = int(df["InvoiceDate"].isna().sum())
checks["missing_revenue"] = int(df["Revenue"].isna().sum())

checks["negative_quantities"] = int((df["Quantity"] < 0).sum())
checks["zero_quantities"] = int((df["Quantity"] == 0).sum())
checks["negative_prices"] = int((df["UnitPrice"] < 0).sum())
checks["zero_prices"] = int((df["UnitPrice"] == 0).sum())
checks["negative_revenue"] = int((df["Revenue"] < 0).sum())

checks["invalid_revenue_calculations"] = int(
    (
        (df["Revenue"] - (df["Quantity"] * df["UnitPrice"]))
        .abs()
        > 0.001
    ).sum()
)

checks["duplicate_invoice_product_rows"] = int(
    df.duplicated(
        subset=["InvoiceNo", "StockCode", "InvoiceDate", "CustomerID"],
        keep=False
    ).sum()
)


# -----------------------------
# 4. Create customer-only data
# -----------------------------
customer_df = df[df["CustomerID"].notna()].copy()

customer_df.to_csv(customer_file, index=False)


# -----------------------------
# 5. Write a report
# -----------------------------
report_lines = []

report_lines.append("CUSTOMER REVENUE AND RETENTION ANALYTICS")
report_lines.append("DATA QUALITY REPORT")
report_lines.append("=" * 50)
report_lines.append("")
report_lines.append(f"Rows checked: {len(df):,}")
report_lines.append(f"Columns checked: {len(df.columns)}")
report_lines.append("")
report_lines.append("QUALITY CHECKS")
report_lines.append("-" * 50)

for check_name, result in checks.items():
    report_lines.append(f"{check_name}: {result:,}")

report_lines.append("")
report_lines.append("CUSTOMER ANALYSIS DATASET")
report_lines.append("-" * 50)
report_lines.append(f"Rows with CustomerID: {len(customer_df):,}")
report_lines.append(
    f"Unique customers: {customer_df['CustomerID'].nunique():,}"
)
report_lines.append(
    f"Unique invoices: {customer_df['InvoiceNo'].nunique():,}"
)
report_lines.append(
    f"Customer-attributed revenue: "
    f"{customer_df['Revenue'].sum():,.2f}"
)

report_lines.append("")
report_lines.append("DATE RANGE")
report_lines.append("-" * 50)
report_lines.append(f"Earliest date: {df['InvoiceDate'].min()}")
report_lines.append(f"Latest date: {df['InvoiceDate'].max()}")

report_lines.append("")
report_lines.append("INTERPRETATION")
report_lines.append("-" * 50)
report_lines.append(
    "Rows with missing CustomerID remain in the main sales dataset "
    "for overall revenue analysis."
)
report_lines.append(
    "Rows with missing CustomerID are excluded from customer retention "
    "analysis because they cannot be linked to a customer."
)
report_lines.append(
    "Large quantities are retained because they may represent legitimate "
    "wholesale transactions."
)

report_file.write_text("\n".join(report_lines), encoding="utf-8")


# -----------------------------
# 6. Print results
# -----------------------------
print("\n=== DATA QUALITY RESULTS ===")

for check_name, result in checks.items():
    print(f"{check_name}: {result:,}")

print("\n=== CUSTOMER DATASET ===")
print(f"Rows with CustomerID: {len(customer_df):,}")
print(f"Unique customers: {customer_df['CustomerID'].nunique():,}")
print(f"Unique invoices: {customer_df['InvoiceNo'].nunique():,}")
print(
    f"Customer-attributed revenue: "
    f"{customer_df['Revenue'].sum():,.2f}"
)

print("\n=== OUTPUT FILES ===")
print(f"Quality report: {report_file}")
print(f"Customer dataset: {customer_file}")
