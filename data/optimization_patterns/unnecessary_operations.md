# Unnecessary Operations Elimination

**Pattern ID**: `unnecessary_operations`
**Performance Impact**: 20-35% improvement
**Use Case**: Queries with unnecessary CAST, string operations

## Description
Remove unnecessary CAST operations, complex string manipulations, and other operations that prevent BigQuery from using optimized execution paths.

## When to Apply
- Queries with unnecessary CAST operations
- Complex string operations that can be simplified
- Functions that prevent index usage
- Redundant data type conversions

## Example
```sql
-- Before (INEFFICIENT - unnecessary operations)
SELECT *
FROM orders o
WHERE CAST(o.customer_id AS STRING) = CAST(c.customer_id AS STRING)
AND SUBSTR(CAST(o.order_date AS STRING), 1, 10) >= '2024-01-01'
AND LOWER(o.status) LIKE 'completed%';

-- After (OPTIMIZED - direct comparisons)
SELECT order_id, customer_id, order_date, total_amount, status
FROM orders o
WHERE o.customer_id = c.customer_id
AND o.order_date >= '2024-01-01'
AND o.status = 'completed';
```

## Expected Improvement
20-35% improvement by enabling BigQuery's optimized execution paths.

## Documentation Reference
https://cloud.google.com/bigquery/docs/best-practices-performance-compute