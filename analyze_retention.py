from pathlib import Path
import pandas as pd


# -----------------------------------
# 1. File paths
# -----------------------------------
input_file = Path("data/processed/analysis_transactions.csv")
output_folder = Path("reports")

output_folder.mkdir(parents=True, exist_ok=True)


# -----------------------------------
# 2. Load analysis-ready data
# -----------------------------------
df = pd.read_csv(
    input_file,
    dtype={
        "InvoiceNo": "string",
        "StockCode": "string",
        "CustomerID": "Int64",
    },
    parse_dates=["InvoiceDate"],
)

# Keep only transactions linked to a customer
customer_df = df[df["CustomerID"].notna()].copy()

# Convert the customer ID to integer-like text for cleaner output
customer_df["CustomerID"] = customer_df["CustomerID"].astype("Int64")


# -----------------------------------
# 3. Create monthly order fields
# -----------------------------------
customer_df["OrderMonth"] = (
    customer_df["InvoiceDate"]
    .dt.to_period("M")
)

first_purchase_month = (
    customer_df.groupby("CustomerID")["OrderMonth"]
    .min()
    .rename("CohortMonth")
)

customer_df = customer_df.merge(
    first_purchase_month,
    on="CustomerID",
    how="left",
)


# -----------------------------------
# 4. Calculate cohort month number
# -----------------------------------
customer_df["CohortIndex"] = (
    (customer_df["OrderMonth"].dt.year
     - customer_df["CohortMonth"].dt.year) * 12
    + (customer_df["OrderMonth"].dt.month
       - customer_df["CohortMonth"].dt.month)
    + 1
)


# -----------------------------------
# 5. Count active customers by cohort
# -----------------------------------
cohort_counts = (
    customer_df.groupby(
        ["CohortMonth", "CohortIndex"]
    )["CustomerID"]
    .nunique()
    .reset_index(name="active_customers")
)


# Size of each original cohort
cohort_sizes = (
    cohort_counts[
        cohort_counts["CohortIndex"] == 1
    ][["CohortMonth", "active_customers"]]
    .rename(columns={"active_customers": "cohort_size"})
)


cohort_counts = cohort_counts.merge(
    cohort_sizes,
    on="CohortMonth",
    how="left",
)

cohort_counts["retention_rate_percent"] = (
    cohort_counts["active_customers"]
    / cohort_counts["cohort_size"]
    * 100
)

cohort_counts["CohortMonth"] = (
    cohort_counts["CohortMonth"]
    .astype(str)
)

cohort_counts.to_csv(
    output_folder / "cohort_retention_long.csv",
    index=False,
)


# -----------------------------------
# 6. Create retention matrix
# -----------------------------------
retention_matrix = cohort_counts.pivot(
    index="CohortMonth",
    columns="CohortIndex",
    values="retention_rate_percent",
)

retention_matrix.to_csv(
    output_folder / "cohort_retention_matrix.csv"
)


# -----------------------------------
# 7. Monthly customer activity
# -----------------------------------
monthly_customer_activity = (
    customer_df.groupby("OrderMonth")
    .agg(
        active_customers=("CustomerID", "nunique"),
        orders=("InvoiceNo", "nunique"),
        revenue=("Revenue", "sum"),
    )
    .reset_index()
)

monthly_customer_activity["OrderMonth"] = (
    monthly_customer_activity["OrderMonth"]
    .astype(str)
)

monthly_customer_activity.to_csv(
    output_folder / "monthly_customer_activity.csv",
    index=False,
)


# -----------------------------------
# 8. Customer-level retention summary
# -----------------------------------
customer_summary = (
    customer_df.groupby("CustomerID")
    .agg(
        revenue=("Revenue", "sum"),
        orders=("InvoiceNo", "nunique"),
        first_purchase=("InvoiceDate", "min"),
        last_purchase=("InvoiceDate", "max"),
        country=("Country", "first"),
    )
    .reset_index()
)

customer_summary["customer_type"] = (
    customer_summary["orders"]
    .apply(
        lambda orders:
        "Repeat customer"
        if orders > 1
        else "One-time customer"
    )
)


# -----------------------------------
# 9. Create simple business segments
# -----------------------------------
revenue_75th_percentile = (
    customer_summary["revenue"].quantile(0.75)
)

customer_summary["customer_segment"] = "Regular customer"

customer_summary.loc[
    customer_summary["orders"] == 1,
    "customer_segment"
] = "One-time customer"

customer_summary.loc[
    (customer_summary["orders"] > 1)
    & (customer_summary["revenue"] >= revenue_75th_percentile),
    "customer_segment"
] = "High-value repeat customer"


customer_summary.to_csv(
    output_folder / "customer_retention_summary.csv",
    index=False,
)


# -----------------------------------
# 10. Print key findings
# -----------------------------------
print("=== RETENTION ANALYSIS COMPLETE ===")
print(
    f"Customers analyzed: "
    f"{customer_df['CustomerID'].nunique():,}"
)

print(
    f"Cohort months: "
    f"{customer_df['CohortMonth'].nunique():,}"
)

print("\n=== FIRST COHORT RETENTION CHECK ===")
print(
    cohort_counts[
        cohort_counts["CohortIndex"] <= 3
    ]
    .head(20)
    .to_string(index=False)
)

print("\n=== CUSTOMER SEGMENTS ===")
print(
    customer_summary["customer_segment"]
    .value_counts()
    .to_string()
)

print("\n=== OUTPUT FILES ===")
print("- reports/cohort_retention_long.csv")
print("- reports/cohort_retention_matrix.csv")
print("- reports/monthly_customer_activity.csv")
print("- reports/customer_retention_summary.csv")
