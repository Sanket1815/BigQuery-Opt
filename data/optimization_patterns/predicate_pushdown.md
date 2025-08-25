# Predicate Pushdown

**Pattern ID**: `predicate_pushdown`
**Performance Impact**: 25-45% improvement
**Use Case**: Filters applied after JOINs or in outer queries

## Description
Move WHERE conditions closer to data sources to filter data early and reduce processing.

## When to Apply
- Filters in outer queries
- WHERE conditions after JOINs
- Subqueries with filters

## Example
```sql
-- Before (Filter applied late)
SELECT * 
FROM (
    SELECT c.name, o.total, o.date
    FROM customers c 
    JOIN orders o ON c.customer_id = o.customer_id
) 
WHERE date >= '2024-01-01';

-- After (Filter applied early)
SELECT c.name, o.total, o.date
FROM customers c 
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.date >= '2024-01-01';
```

## Expected Improvement
25-45% improvement by reducing data processing.

## Documentation Reference
https://cloud.google.com/bigquery/docs/best-practices-performance-compute