# Approximate Aggregation

**Pattern ID**: `approximate_aggregation`
**Performance Impact**: 50-80% improvement
**Use Case**: COUNT DISTINCT operations on large datasets

## Description
Replace exact COUNT(DISTINCT) with APPROX_COUNT_DISTINCT() for massive performance gains on large datasets. This is one of the highest-impact optimizations available in BigQuery.

## When to Apply
- ANY `COUNT(DISTINCT column)` operation (always consider this optimization)
- Tables with thousands or millions of rows
- Analytics queries where 1-2% variance is acceptable
- Dashboard queries that need fast response times
- Reporting queries with large datasets

## Example
```sql
-- Before (EXTREMELY SLOW on large datasets - can take minutes)
SELECT 
    region,
    COUNT(DISTINCT customer_id) as unique_customers,
    COUNT(DISTINCT product_id) as unique_products
FROM large_orders 
GROUP BY region;

-- After (FAST - completes in seconds)
SELECT 
    region,
    APPROX_COUNT_DISTINCT(customer_id) as unique_customers,
    APPROX_COUNT_DISTINCT(product_id) as unique_products
FROM large_orders 
GROUP BY region;
```

## Expected Improvement
50-80% improvement on large datasets. Can reduce execution time from minutes to seconds.

## Documentation Reference
https://cloud.google.com/bigquery/docs/reference/standard-sql/approximate_aggregate_functions