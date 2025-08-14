# Column Pruning

**Pattern ID**: `column_pruning`
**Performance Impact**: 30-50% improvement
**Use Case**: Queries using SELECT * on wide tables

## Description
Replace `SELECT *` with specific column names to dramatically reduce data transfer, improve query performance, and reduce costs. This is one of the most impactful optimizations for BigQuery.

## When to Apply
- ANY query using `SELECT *` (always apply this optimization)
- Wide tables with many columns (10+ columns)
- Queries where only specific columns are actually needed
- Network transfer optimization needed
- Cost reduction is important

## Example
```sql
-- Before (Highly Inefficient - scans all columns)
SELECT * FROM orders WHERE order_date >= '2024-01-01';

-- After (Optimized - scans only needed columns)
SELECT order_id, customer_id, order_date, total_amount 
FROM orders 
WHERE order_date >= '2024-01-01';
```

## Expected Improvement
30-50% reduction in data transfer and query execution time. Can reduce costs by 40-60% on wide tables.

## Documentation Reference
https://cloud.google.com/bigquery/docs/best-practices-performance-input