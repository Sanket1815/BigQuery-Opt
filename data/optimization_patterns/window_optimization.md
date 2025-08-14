# Window Function Optimization

**Pattern ID**: `window_optimization`
**Performance Impact**: 25-40% improvement
**Use Case**: Window functions without proper partitioning

## Description
Optimize window function specifications by adding appropriate PARTITION BY clauses. Window functions without partitioning process entire datasets unnecessarily.

## When to Apply
- ANY window function without `PARTITION BY` (always add partitioning)
- Inefficient `ORDER BY` in window functions
- Window functions that can be optimized with better partitioning
- ROW_NUMBER, RANK, DENSE_RANK without partitioning

## Example
```sql
-- Before (INEFFICIENT - processes entire dataset)
SELECT 
    customer_id,
    order_date,
    ROW_NUMBER() OVER (ORDER BY order_date) as row_num,
    RANK() OVER (ORDER BY total_amount DESC) as amount_rank
FROM orders;

-- After (OPTIMIZED - processes data in logical partitions)
SELECT 
    customer_id,
    order_date,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) as row_num,
    RANK() OVER (PARTITION BY customer_id ORDER BY total_amount DESC) as amount_rank
FROM orders;
```

## Expected Improvement
25-40% improvement for analytical queries by reducing data processing scope.

## Documentation Reference
https://cloud.google.com/bigquery/docs/reference/standard-sql/analytic-functions