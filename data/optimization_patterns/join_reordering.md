# JOIN Reordering

**Pattern ID**: `join_reordering`
**Performance Impact**: 25-50% improvement
**Use Case**: Multi-table JOINs with different table sizes

## Description
Reorder JOINs to place SMALLEST tables first to minimize intermediate result sizes. This is critical for BigQuery performance as it processes JOINs left-to-right and builds intermediate results.

## When to Apply
- ANY query with 2+ JOINs (always check for reordering opportunities)
- Tables with significantly different row counts
- Complex JOIN conditions that can benefit from early filtering
- Cross joins that should be explicit JOINs

## Example
```sql
-- Before (HIGHLY INEFFICIENT - starts with largest table)
FROM order_items oi  -- 100,000 rows (LARGEST)
JOIN orders o ON oi.order_id = o.order_id  -- 50,000 rows
JOIN customers c ON o.customer_id = c.customer_id  -- 1,000 rows
JOIN products p ON oi.product_id = p.product_id;  -- 50 rows (SMALLEST)

-- After (OPTIMIZED - starts with smallest table)
FROM products p  -- 50 rows (SMALLEST FIRST)
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o ON oi.order_id = o.order_id  
JOIN customers c ON o.customer_id = c.customer_id;  -- Build up gradually
```

## Expected Improvement
25-50% improvement by dramatically reducing intermediate result sizes and memory usage.

## Documentation Reference
https://cloud.google.com/bigquery/docs/best-practices-performance-compute#optimize_your_join_patterns