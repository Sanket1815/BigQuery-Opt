# Subquery to JOIN Conversion

**Pattern ID**: `subquery_to_join`
**Performance Impact**: 40-70% improvement
**Use Case**: EXISTS, IN, and correlated subqueries

## Description
Convert inefficient subqueries (EXISTS, IN, correlated) to JOINs for dramatically better performance. Subqueries often cause BigQuery to scan data multiple times.

## When to Apply
- ANY `EXISTS` subquery (always convert to JOIN)
- ANY `IN (SELECT ...)` subquery (always convert to JOIN)
- `NOT EXISTS` patterns
- Correlated subqueries in SELECT clause
- Nested subqueries that can be flattened

## Example
```sql
-- Before (VERY INEFFICIENT - correlated subquery scans repeatedly)
SELECT customer_name 
FROM customers c 
WHERE EXISTS (
    SELECT 1 FROM orders o 
    WHERE o.customer_id = c.customer_id 
    AND o.status = 'completed'
);

-- After (MUCH FASTER - single scan with JOIN)
SELECT DISTINCT c.customer_name
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status = 'completed';
```

## Expected Improvement
40-70% improvement for complex filtering operations. Can reduce execution time from minutes to seconds.

## Documentation Reference
https://cloud.google.com/bigquery/docs/best-practices-performance-compute