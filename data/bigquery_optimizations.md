# BigQuery Query Optimization Documentation

## Column Pruning

**Pattern ID**: `column_pruning`
**Performance Impact**: 20-40% improvement
**Use Case**: Queries using SELECT *

### Description
Replace `SELECT *` with specific column names to reduce data transfer and improve performance.

### When to Apply
- Queries using `SELECT *`
- Wide tables with many columns
- Network transfer optimization needed

### Example
```sql
-- Before (Inefficient)
SELECT * FROM orders WHERE order_date >= '2024-01-01';

-- After (Optimized)
SELECT order_id, customer_id, order_date, total_amount 
FROM orders 
WHERE order_date >= '2024-01-01';
```

### Expected Improvement
20-40% reduction in data transfer and query execution time.

### Documentation Reference
https://cloud.google.com/bigquery/docs/best-practices-performance-input

---

## JOIN Reordering

**Pattern ID**: `join_reordering`
**Performance Impact**: 20-40% improvement
**Use Case**: Multi-table JOINs with different table sizes

### Description
Reorder JOINs to place smaller tables first and apply more selective filters early.

### When to Apply
- Multiple JOINs (3+ tables)
- Tables with significantly different sizes
- Complex JOIN conditions

### Example
```sql
-- Before (Large table first - inefficient)
SELECT c.name, o.total, p.name
FROM large_orders o
JOIN small_customers c ON o.customer_id = c.customer_id
JOIN tiny_products p ON o.product_id = p.product_id;

-- After (Small table first - efficient)
SELECT c.name, o.total, p.name
FROM tiny_products p
JOIN large_orders o ON p.product_id = o.product_id
JOIN small_customers c ON o.customer_id = c.customer_id;
```

### Expected Improvement
20-40% improvement by reducing intermediate result sizes.

### Documentation Reference
https://cloud.google.com/bigquery/docs/best-practices-performance-compute#optimize_your_join_patterns

---

## Subquery to JOIN Conversion

**Pattern ID**: `subquery_to_join`
**Performance Impact**: 30-60% improvement
**Use Case**: Correlated subqueries and EXISTS clauses

### Description
Convert EXISTS subqueries, IN subqueries, and correlated subqueries to JOINs for better performance.

### When to Apply
- `EXISTS` subqueries
- `IN (SELECT ...)` subqueries
- `NOT EXISTS` patterns
- Correlated subqueries in SELECT clause

### Example
```sql
-- Before (Correlated subquery - slow)
SELECT customer_name 
FROM customers c 
WHERE EXISTS (
    SELECT 1 FROM orders o 
    WHERE o.customer_id = c.customer_id 
    AND o.status = 'completed'
);

-- After (JOIN - much faster)
SELECT DISTINCT c.customer_name
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status = 'completed';
```

### Expected Improvement
30-60% improvement for complex filtering operations.

### Documentation Reference
https://cloud.google.com/bigquery/docs/best-practices-performance-compute

---

## Approximate Aggregation

**Pattern ID**: `approximate_aggregation`
**Performance Impact**: 40-70% improvement
**Use Case**: Large datasets where exact counts aren't critical

### Description
Replace exact aggregation functions with approximate versions for better performance on large datasets.

### When to Apply
- `COUNT(DISTINCT column)` on tables with millions of rows
- Approximate results are acceptable for analytics
- Performance is more important than exact precision

### Example
```sql
-- Before (Slow on large datasets)
SELECT COUNT(DISTINCT customer_id) FROM large_orders;

-- After (Much faster)
SELECT APPROX_COUNT_DISTINCT(customer_id) FROM large_orders;
```

### Expected Improvement
40-70% improvement on large datasets.

### Documentation Reference
https://cloud.google.com/bigquery/docs/reference/standard-sql/approximate_aggregate_functions

---

## Window Function Optimization

**Pattern ID**: `window_optimization`
**Performance Impact**: 15-30% improvement
**Use Case**: Window functions without proper partitioning

### Description
Optimize window function specifications by adding appropriate PARTITION BY clauses and improving ORDER BY specifications.

### When to Apply
- Window functions without `PARTITION BY`
- Inefficient `ORDER BY` in window functions
- Correlated subqueries that can become window functions

### Example
```sql
-- Before (No partitioning - processes all data)
SELECT 
    customer_id,
    order_date,
    ROW_NUMBER() OVER (ORDER BY order_date) as row_num
FROM orders;

-- After (Partitioned - processes data in chunks)
SELECT 
    customer_id,
    order_date,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) as row_num
FROM orders;
```

### Expected Improvement
15-30% improvement for analytical queries.

### Documentation Reference
https://cloud.google.com/bigquery/docs/reference/standard-sql/analytic-functions

---

## Predicate Pushdown

**Pattern ID**: `predicate_pushdown`
**Performance Impact**: 25-45% improvement
**Use Case**: Filters applied after JOINs or in outer queries

### Description
Move WHERE conditions closer to data sources to filter data early and reduce processing.

### When to Apply
- Filters in outer queries
- WHERE conditions after JOINs
- Subqueries with filters

### Example
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

### Expected Improvement
25-45% improvement by reducing data processing.

### Documentation Reference
https://cloud.google.com/bigquery/docs/best-practices-performance-compute

---

## Clustering Optimization

**Pattern ID**: `clustering_optimization`
**Performance Impact**: 20-35% improvement
**Use Case**: Queries on clustered tables

### Description
Leverage clustering keys in WHERE clauses and optimize queries to use clustered table organization.

### When to Apply
- Tables with clustering keys
- Equality filters on clustered columns
- Range queries on clustered columns

### Example
```sql
-- Before (Not using clustering keys)
SELECT * FROM clustered_orders 
WHERE region = 'US-West' 
AND order_date >= '2024-01-01';

-- After (Using clustering keys first)
SELECT * FROM clustered_orders 
WHERE customer_id BETWEEN 1000 AND 2000  -- Clustering key
AND region = 'US-West' 
AND order_date >= '2024-01-01';
```

### Expected Improvement
20-35% improvement by leveraging physical data organization.

### Documentation Reference
https://cloud.google.com/bigquery/docs/clustered-tables

---

## Materialized View Suggestions

**Pattern ID**: `materialized_view_suggestion`
**Performance Impact**: 60-90% improvement
**Use Case**: Frequently accessed aggregations

### Description
Identify opportunities to create materialized views for frequently executed aggregation queries.

### When to Apply
- Queries with `GROUP BY` and aggregations
- Frequently executed reports
- Complex calculations repeated often

### Example
```sql
-- Frequently run query
SELECT 
    region,
    DATE(order_date) as order_day,
    COUNT(*) as daily_orders,
    SUM(total_amount) as daily_revenue
FROM orders 
WHERE order_date >= '2024-01-01'
GROUP BY region, DATE(order_date);

-- Suggestion: Create materialized view
CREATE MATERIALIZED VIEW daily_order_summary AS
SELECT 
    region,
    DATE(order_date) as order_day,
    COUNT(*) as daily_orders,
    SUM(total_amount) as daily_revenue
FROM orders 
GROUP BY region, DATE(order_date);
```

### Expected Improvement
60-90% improvement for frequently accessed aggregations.

### Documentation Reference
https://cloud.google.com/bigquery/docs/materialized-views-intro

---

## CASE WHEN Optimization

**Pattern ID**: `case_when_optimization`
**Performance Impact**: 15-25% improvement
**Use Case**: Complex conditional logic

### Description
Optimize CASE WHEN statements by reordering conditions and eliminating redundant checks.

### When to Apply
- Complex `CASE WHEN` statements
- Redundant condition checking
- Nested conditional logic

### Example
```sql
-- Before (Inefficient CASE structure)
SELECT 
    CASE 
        WHEN status = 'completed' AND total > 1000 THEN 'high_value'
        WHEN status = 'completed' AND total > 500 THEN 'medium_value'
        WHEN status = 'completed' THEN 'low_value'
        ELSE 'other'
    END as order_category
FROM orders;

-- After (Optimized CASE structure)
SELECT 
    CASE 
        WHEN status != 'completed' THEN 'other'
        WHEN total > 1000 THEN 'high_value'
        WHEN total > 500 THEN 'medium_value'
        ELSE 'low_value'
    END as order_category
FROM orders;
```

### Expected Improvement
15-25% improvement for queries with complex conditional logic.

### Documentation Reference
https://cloud.google.com/bigquery/docs/reference/standard-sql/conditional_expressions

---

## HAVING to WHERE Conversion

**Pattern ID**: `having_to_where_conversion`
**Performance Impact**: 15-25% improvement
**Use Case**: HAVING clauses that can be WHERE clauses

### Description
Convert HAVING clauses on non-aggregate columns to WHERE clauses to filter before grouping.

### When to Apply
- `HAVING` clauses on non-aggregate columns
- Filters that can be applied before grouping

### Example
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

### Expected Improvement
15-25% improvement by filtering before aggregation.

### Documentation Reference
https://cloud.google.com/bigquery/docs/best-practices-performance-compute