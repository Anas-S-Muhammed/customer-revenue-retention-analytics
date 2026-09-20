# Business Findings

## Executive summary

The cleaned dataset contains 524,882 transaction lines, 19,962 orders, 3,922 products, and £10.64 million in revenue across 38 countries.

The United Kingdom dominates sales, generating approximately 84.6% of total revenue. Customer retention is commercially important: repeat customers generate substantially more revenue per customer than one-time customers.

## Key findings

### Revenue performance

- Total revenue: £10,642,119.63
- Total orders: 19,962
- Total units sold: 5,572,424
- Average order value: £533.12
- Countries represented: 38

### Customer behavior

The analysis identified 4,338 customers.

- One-time customers: 1,493
- Repeat customers: 2,845
- High-value repeat customers: 1,054
- Regular customers: 1,791

One-time customers generated approximately £613,989.56, while repeat customers generated approximately £8,273,228.16.

The average revenue per repeat customer was approximately £2,907.99, compared with £411.25 for a one-time customer.

### Customer retention

The December 2010 customer cohort had:

- 36.6% retention in month two
- 32.3% retention in month three

The January 2011 cohort had:

- 22.1% retention in month two
- 26.6% retention in month three

Retention varies across cohorts, so customer acquisition month should be considered when evaluating performance.

### Geographic performance

The United Kingdom generated approximately 84.6% of revenue.

The next largest markets by revenue were:

1. Netherlands
2. EIRE
3. Germany
4. France
5. Australia

This suggests that the business is highly dependent on the United Kingdom, while selected international markets may offer expansion opportunities.

### Product performance

The highest-revenue items include merchandise as well as postage and manual transaction records.

For future product decisions, postage, manual adjustments, and administrative items should be separated from normal merchandise.

## Recommendations

1. Target one-time customers with follow-up campaigns designed to encourage a second purchase.
2. Study the December 2010 cohort because it demonstrated stronger early retention than several later cohorts.
3. Investigate why retention varies between acquisition cohorts.
4. Protect the United Kingdom customer base while evaluating expansion in Germany, France, the Netherlands, and EIRE.
5. Separate merchandise revenue from postage and manual transaction records in future product dashboards.
6. Create a high-value customer segment for personalized offers and loyalty campaigns.

## Limitations

The dataset contains missing CustomerID values. Therefore, overall sales analysis uses more records than customer retention analysis.

The dataset covers a limited historical period from December 2010 to December 2011.

The analysis identifies patterns and associations. It does not prove that a marketing campaign or customer action caused a specific result.

Large quantities were retained because some may represent legitimate wholesale purchases. They should be investigated separately before operational decisions are made.

## Data-processing decisions

Cancelled invoices, negative quantities, zero quantities, zero prices, and negative prices were excluded from the cleaned sales dataset.

Exact duplicate rows were removed during analysis.

Rows with missing CustomerID were retained for overall sales analysis but excluded from customer-level retention analysis.
