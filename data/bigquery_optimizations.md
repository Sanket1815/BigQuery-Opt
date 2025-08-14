## Column Pruning

**Pattern ID**: `column_pruning`
**Performance Impact**: 30-50% improvement
**Use Case**: Queries using SELECT * on wide tables

### Description
Replace `SELECT *` with specific column names to dramatically reduce data transfer, improve query performance, and reduce costs. This is one of the most impactful optimizations for BigQuery.

### When to Apply
- ANY query using `SELECT *` (always apply this optimization)
- Wide tables with many columns (10+ columns)
- Queries where only specific columns are actually needed
- Network transfer optimization needed
- Cost reduction is important

### Example
```sql
-- Before (Highly Inefficient - scans all columns)
SELECT * FROM orders WHERE order_date >= '2024-01-01';

-- After (Optimized - scans only needed columns)
SELECT order_id, customer_id, order_date, total_amount 
FROM orders 
WHERE order_date >= '2024-01-01';
```

### Expected Improvement
30-50% reduction in data transfer and query execution time. Can reduce costs by 40-60% on wide tables.

### Documentation Reference
https://cloud.google.com/bigquery/docs/best-practices-performance-input

---

## JOIN Reordering

**Pattern ID**: `join_reordering`
**Performance Impact**: 25-50% improvement
**Use Case**: Multi-table JOINs with different table sizes

### Description
Reorder JOINs to place SMALLEST tables first to minimize intermediate result sizes. This is critical for BigQuery performance as it processes JOINs left-to-right and builds intermediate results.

### When to Apply
- ANY query with 2+ JOINs (always check for reordering opportunities)
- Tables with significantly different row counts
- Complex JOIN conditions that can benefit from early filtering
- Cross joins that should be explicit JOINs

### Example
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

### Expected Improvement
25-50% improvement by dramatically reducing intermediate result sizes and memory usage.

### Documentation Reference
https://cloud.google.com/bigquery/docs/best-practices-performance-compute#optimize_your_join_patterns

---

## Subquery to JOIN Conversion

**Pattern ID**: `subquery_to_join`
**Performance Impact**: 40-70% improvement
**Use Case**: EXISTS, IN, and correlated subqueries

### Description
Convert inefficient subqueries (EXISTS, IN, correlated) to JOINs for dramatically better performance. Subqueries often cause BigQuery to scan data multiple times.

### When to Apply
- ANY `EXISTS` subquery (always convert to JOIN)
- ANY `IN (SELECT ...)` subquery (always convert to JOIN)
- `NOT EXISTS` patterns
- Correlated subqueries in SELECT clause
- Nested subqueries that can be flattened

### Example
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

### Expected Improvement
40-70% improvement for complex filtering operations. Can reduce execution time from minutes to seconds.

### Documentation Reference
https://cloud.google.com/bigquery/docs/best-practices-performance-compute

---

## Approximate Aggregation

**Pattern ID**: `approximate_aggregation`
**Performance Impact**: 50-80% improvement
**Use Case**: COUNT DISTINCT operations on large datasets

### Description
Replace exact COUNT(DISTINCT) with APPROX_COUNT_DISTINCT() for massive performance gains on large datasets. This is one of the highest-impact optimizations available in BigQuery.

### When to Apply
- ANY `COUNT(DISTINCT column)` operation (always consider this optimization)
- Tables with thousands or millions of rows
- Analytics queries where 1-2% variance is acceptable
- Dashboard queries that need fast response times
- Reporting queries with large datasets

### Example
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

### Expected Improvement
50-80% improvement on large datasets. Can reduce execution time from minutes to seconds.

### Documentation Reference
https://cloud.google.com/bigquery/docs/reference/standard-sql/approximate_aggregate_functions

---

## Window Function Optimization

**Pattern ID**: `window_optimization`
**Performance Impact**: 25-40% improvement
**Use Case**: Window functions without proper partitioning

### Description
Optimize window function specifications by adding appropriate PARTITION BY clauses. Window functions without partitioning process entire datasets unnecessarily.

### When to Apply
- ANY window function without `PARTITION BY` (always add partitioning)
- Inefficient `ORDER BY` in window functions
- Window functions that can be optimized with better partitioning
- ROW_NUMBER, RANK, DENSE_RANK without partitioning

### Example
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

### Expected Improvement
25-40% improvement for analytical queries by reducing data processing scope.

### Documentation Reference
https://cloud.google.com/bigquery/docs/reference/standard-sql/analytic-functions

---

## Cross JOIN Elimination

**Pattern ID**: `cross_join_elimination`
**Performance Impact**: 60-90% improvement
**Use Case**: Accidental cross joins using comma syntax

### Description
Convert accidental cross joins (comma syntax) to explicit INNER JOINs with proper conditions. Cross joins create cartesian products which are extremely inefficient.

### When to Apply
- ANY query using comma syntax for table joins
- Queries with multiple tables in FROM clause separated by commas
- WHERE clauses that should be JOIN conditions

### Example
```sql
-- Before (EXTREMELY INEFFICIENT - creates cartesian product)
SELECT c.customer_name, p.product_name
FROM customers c, products p
WHERE c.customer_tier = 'Gold' AND p.category = 'Electronics';

-- After (EFFICIENT - proper JOIN with conditions)
SELECT c.customer_name, p.product_name
FROM customers c
CROSS JOIN products p  -- Explicit cross join if intended
WHERE c.customer_tier = 'Gold' AND p.category = 'Electronics';

-- Or better yet, if there's a relationship:
SELECT c.customer_name, p.product_name
FROM customers c
JOIN customer_preferences cp ON c.customer_id = cp.customer_id
JOIN products p ON cp.product_id = p.product_id
WHERE c.customer_tier = 'Gold' AND p.category = 'Electronics';
```

### Expected Improvement
60-90% improvement by eliminating cartesian products.

### Documentation Reference
https://cloud.google.com/bigquery/docs/best-practices-performance-compute#optimize_your_join_patterns

---

## Unnecessary Operations Elimination

**Pattern ID**: `unnecessary_operations`
**Performance Impact**: 20-35% improvement
**Use Case**: Queries with unnecessary CAST, string operations

### Description
Remove unnecessary CAST operations, complex string manipulations, and other operations that prevent BigQuery from using optimized execution paths.

### When to Apply
- Queries with unnecessary CAST operations
- Complex string operations that can be simplified
- Functions that prevent index usage
- Redundant data type conversions

### Example
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

### Expected Improvement
20-35% improvement by enabling BigQuery's optimized execution paths.

### Documentation Reference
https://cloud.google.com/bigquery/docs/best-practices-performance-compute

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