from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


# -----------------------------------
# 1. Paths
# -----------------------------------
reports_folder = Path("reports")
charts_folder = reports_folder / "charts"

charts_folder.mkdir(parents=True, exist_ok=True)


# -----------------------------------
# 2. Load analysis outputs
# -----------------------------------
monthly_sales = pd.read_csv(
    reports_folder / "monthly_sales.csv"
)

country_sales = pd.read_csv(
    reports_folder / "country_sales.csv"
)

product_sales = pd.read_csv(
    reports_folder / "product_sales.csv"
)

customer_types = pd.read_csv(
    reports_folder / "one_time_vs_repeat_customers.csv"
)

retention_matrix = pd.read_csv(
    reports_folder / "cohort_retention_matrix.csv",
    index_col=0
)


# -----------------------------------
# 3. Chart style
# -----------------------------------
plt.style.use("seaborn-v0_8-whitegrid")


# -----------------------------------
# 4. Monthly revenue
# -----------------------------------
plt.figure(figsize=(12, 6))

plt.plot(
    monthly_sales["Month"],
    monthly_sales["revenue"],
    marker="o",
    linewidth=2
)

plt.title("Monthly Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    charts_folder / "monthly_revenue.png",
    dpi=200
)

plt.close()


# -----------------------------------
# 5. Revenue by country
# -----------------------------------
top_countries = country_sales.head(10).sort_values("revenue")

plt.figure(figsize=(10, 6))

plt.barh(
    top_countries["Country"],
    top_countries["revenue"]
)

plt.title("Top 10 Countries by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Country")
plt.tight_layout()

plt.savefig(
    charts_folder / "revenue_by_country.png",
    dpi=200
)

plt.close()


# -----------------------------------
# 6. Top products
# -----------------------------------
top_products = product_sales.head(10).sort_values("revenue")

# Shorten long product names for readability
top_products["short_description"] = (
    top_products["Description"]
    .fillna("Unknown product")
    .astype(str)
    .str[:35]
)

plt.figure(figsize=(11, 7))

plt.barh(
    top_products["short_description"],
    top_products["revenue"]
)

plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Product")
plt.tight_layout()

plt.savefig(
    charts_folder / "top_products_by_revenue.png",
    dpi=200
)

plt.close()


# -----------------------------------
# 7. Customer segments
# -----------------------------------
plt.figure(figsize=(8, 6))

plt.bar(
    customer_types["customer_type"],
    customer_types["customers"]
)

plt.title("One-Time versus Repeat Customers")
plt.xlabel("Customer Type")
plt.ylabel("Number of Customers")
plt.xticks(rotation=20)
plt.tight_layout()

plt.savefig(
    charts_folder / "customer_segments.png",
    dpi=200
)

plt.close()


# -----------------------------------
# 8. Cohort retention heatmap
# -----------------------------------
plt.figure(figsize=(12, 7))

image = plt.imshow(
    retention_matrix,
    aspect="auto",
    cmap="Blues",
    vmin=0,
    vmax=100
)

plt.colorbar(image, label="Retention Rate (%)")

plt.title("Customer Cohort Retention")
plt.xlabel("Months Since First Purchase")
plt.ylabel("Cohort Month")

plt.xticks(
    range(len(retention_matrix.columns)),
    retention_matrix.columns
)

plt.yticks(
    range(len(retention_matrix.index)),
    retention_matrix.index
)

plt.tight_layout()

plt.savefig(
    charts_folder / "cohort_retention_heatmap.png",
    dpi=200
)

plt.close()


# -----------------------------------
# 9. Finish
# -----------------------------------
print("=== CHARTS CREATED ===")

for chart in sorted(charts_folder.glob("*.png")):
    print(chart)

