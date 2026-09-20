from pathlib import Path
import pandas as pd


# -----------------------------------
# 1. File paths
# -----------------------------------
input_file = Path("data/processed/clean_sales_transactions.csv")
output_folder = Path("reports")
analysis_file = Path("data/processed/analysis_transactions.csv")

output_folder.mkdir(parents=True, exist_ok=True)


# -----------------------------------
# 2. Load cleaned transactions
# -----------------------------------
df = pd.read_csv(
    input_file,
    parse_dates=["InvoiceDate"]
)

print("=== LOADED CLEAN TRANSACTIONS ===")
print(f"Rows before exact-duplicate removal: {len(df):,}")


# -----------------------------------
# 3. Remove exact duplicate records
# -----------------------------------
exact_duplicates = df.duplicated().sum()

df = df.drop_duplicates().copy()

print(f"Exact duplicate rows removed: {exact_duplicates:,}")
print(f"Rows used for analysis: {len(df):,}")


# Save the analysis-ready transaction file
df.to_csv(analysis_file, index=False)


# -----------------------------------
# 4. Create date fields
# -----------------------------------
df["Month"] = df["InvoiceDate"].dt.to_period("M").astype(str)
df["Year"] = df["InvoiceDate"].dt.year
df["MonthNumber"] = df["InvoiceDate"].dt.month


# -----------------------------------
# 5. Monthly sales analysis
# -----------------------------------
monthly_sales = (
    df.groupby("Month")
    .agg(
        revenue=("Revenue", "sum"),
        orders=("InvoiceNo", "nunique"),
        transaction_lines=("InvoiceNo", "size"),
        units_sold=("Quantity", "sum"),
        products_sold=("StockCode", "nunique"),
    )
    .reset_index()
)

monthly_sales["average_order_value"] = (
    monthly_sales["revenue"] / monthly_sales["orders"]
)

monthly_sales.to_csv(
    output_folder / "monthly_sales.csv",
    index=False
)


# -----------------------------------
# 6. Country sales analysis
# -----------------------------------
country_sales = (
    df.groupby("Country")
    .agg(
        revenue=("Revenue", "sum"),
        orders=("InvoiceNo", "nunique"),
        customers=("CustomerID", "nunique"),
        units_sold=("Quantity", "sum"),
    )
    .reset_index()
    .sort_values("revenue", ascending=False)
)

country_sales["revenue_share_percent"] = (
    country_sales["revenue"]
    / country_sales["revenue"].sum()
    * 100
)

country_sales.to_csv(
    output_folder / "country_sales.csv",
    index=False
)


# -----------------------------------
# 7. Product sales analysis
# -----------------------------------
product_sales = (
    df.groupby(["StockCode", "Description"], dropna=False)
    .agg(
        revenue=("Revenue", "sum"),
        units_sold=("Quantity", "sum"),
        orders=("InvoiceNo", "nunique"),
    )
    .reset_index()
    .sort_values("revenue", ascending=False)
)

product_sales.to_csv(
    output_folder / "product_sales.csv",
    index=False
)


# -----------------------------------
# 8. Customer summary
# -----------------------------------
customer_df = df[df["CustomerID"].notna()].copy()

customer_summary = (
    customer_df.groupby("CustomerID")
    .agg(
        revenue=("Revenue", "sum"),
        orders=("InvoiceNo", "nunique"),
        units_sold=("Quantity", "sum"),
        first_purchase=("InvoiceDate", "min"),
        last_purchase=("InvoiceDate", "max"),
        country=("Country", "first"),
    )
    .reset_index()
)

customer_summary["customer_type"] = customer_summary["orders"].apply(
    lambda number_of_orders:
    "Repeat customer"
    if number_of_orders > 1
    else "One-time customer"
)

customer_summary["days_between_first_and_last_purchase"] = (
    customer_summary["last_purchase"]
    - customer_summary["first_purchase"]
).dt.days

customer_summary = customer_summary.sort_values(
    "revenue",
    ascending=False
)

customer_summary.to_csv(
    output_folder / "customer_summary.csv",
    index=False
)


# -----------------------------------
# 9. One-time versus repeat customers
# -----------------------------------
customer_type_summary = (
    customer_summary.groupby("customer_type")
    .agg(
        customers=("CustomerID", "nunique"),
        revenue=("revenue", "sum"),
        average_revenue_per_customer=("revenue", "mean"),
        average_orders_per_customer=("orders", "mean"),
    )
    .reset_index()
)

customer_type_summary.to_csv(
    output_folder / "one_time_vs_repeat_customers.csv",
    index=False
)


# -----------------------------------
# 10. Print key results
# -----------------------------------
print("\n=== KEY SALES METRICS ===")
print(f"Total revenue: {df['Revenue'].sum():,.2f}")
print(f"Total orders: {df['InvoiceNo'].nunique():,}")
print(f"Total products: {df['StockCode'].nunique():,}")
print(f"Total countries: {df['Country'].nunique():,}")
print(f"Total units sold: {df['Quantity'].sum():,}")
print(
    f"Average order value: "
    f"{df.groupby('InvoiceNo')['Revenue'].sum().mean():,.2f}"
)

print("\n=== TOP 10 COUNTRIES BY REVENUE ===")
print(country_sales.head(10).to_string(index=False))

print("\n=== TOP 10 PRODUCTS BY REVENUE ===")
print(product_sales.head(10).to_string(index=False))

print("\n=== CUSTOMER TYPES ===")
print(customer_type_summary.to_string(index=False))

print("\n=== OUTPUT FILES CREATED ===")
print(f"- {analysis_file}")
print(f"- {output_folder / 'monthly_sales.csv'}")
print(f"- {output_folder / 'country_sales.csv'}")
print(f"- {output_folder / 'product_sales.csv'}")
print(f"- {output_folder / 'customer_summary.csv'}")
print(f"- {output_folder / 'one_time_vs_repeat_customers.csv'}")
