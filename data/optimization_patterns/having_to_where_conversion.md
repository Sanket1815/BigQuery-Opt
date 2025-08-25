# HAVING to WHERE Conversion

**Pattern ID**: `having_to_where_conversion`
**Performance Impact**: 15-25% improvement
**Use Case**: HAVING clauses that can be WHERE clauses

## Description
Convert HAVING clauses on non-aggregate columns to WHERE clauses to filter before grouping.

## When to Apply
- `HAVING` clauses on non-aggregate columns
- Filters that can be applied before grouping

## Example
```sql
-- Before (HAVING on non-aggregate column)
SELECT customer_id, COUNT(*) as order_count
FROM orders 
GROUP BY customer_id
HAVING customer_id > 1000;

-- After (WHERE clause - filters before grouping)
SELECT customer_id, COUNT(*) as order_count
FROM orders 
WHERE customer_id > 1000
GROUP BY customer_id;
```

## Expected Improvement
15-25% improvement by filtering before aggregation.

## Documentation Reference
https://cloud.google.com/bigquery/docs/best-practices-performance-compute