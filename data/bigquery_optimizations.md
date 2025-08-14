# BigQuery Query Optimization Patterns

This comprehensive guide contains optimization patterns extracted from Google Cloud BigQuery documentation to improve query performance while preserving business logic.

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

## Predicate Pushdown

**Pattern ID**: `predicate_pushdown`
**Performance Impact**: 25-45% improvement
**Use Case**: Filters applied after JOINs or in outer queries

### Description
Move WHERE conditions closer to data sources to filter data early and reduce processing. This optimization reduces the amount of data that needs to be processed in subsequent operations.

### When to Apply
- Filters in outer queries that can be moved to inner queries
- WHERE conditions applied after JOINs
- Subqueries with filters that can be pushed down
- Complex queries with multiple levels of nesting

### Example
```sql
-- Before (Filter applied late - processes more data)
SELECT * 
FROM (
    SELECT c.name, o.total, o.date
    FROM customers c 
    JOIN orders o ON c.customer_id = o.customer_id
) 
WHERE date >= '2024-01-01';

-- After (Filter applied early - processes less data)
SELECT c.name, o.total, o.date
FROM customers c 
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.date >= '2024-01-01';
```

### Expected Improvement
25-45% improvement by reducing data processing volume early in the query execution.

### Documentation Reference
https://cloud.google.com/bigquery/docs/best-practices-performance-compute

## HAVING to WHERE Conversion

**Pattern ID**: `having_to_where_conversion`
**Performance Impact**: 15-25% improvement
**Use Case**: HAVING clauses that can be WHERE clauses

### Description
Convert HAVING clauses on non-aggregate columns to WHERE clauses to filter data before grouping operations, reducing the amount of data processed during aggregation.

### When to Apply
- `HAVING` clauses that filter on non-aggregate columns
- Filters that can be applied before GROUP BY operations
- Queries where early filtering would reduce aggregation workload

### Example
```sql
-- Before (HAVING on non-aggregate column - filters after grouping)
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
15-25% improvement by filtering data before expensive aggregation operations.

### Documentation Reference
https://cloud.google.com/bigquery/docs/best-practices-performance-compute

## Unnecessary Operations Elimination

**Pattern ID**: `unnecessary_operations`
**Performance Impact**: 20-35% improvement
**Use Case**: Queries with unnecessary CAST, string operations

### Description
Remove unnecessary CAST operations, complex string manipulations, and other operations that prevent BigQuery from using optimized execution paths and indexes.

### When to Apply
- Queries with unnecessary CAST operations
- Complex string operations that can be simplified
- Functions that prevent efficient data access
- Redundant data type conversions
- Operations that can be replaced with direct comparisons

### Example
```sql
-- Before (INEFFICIENT - unnecessary operations prevent optimization)
SELECT *
FROM orders o
WHERE CAST(o.customer_id AS STRING) = CAST(c.customer_id AS STRING)
AND SUBSTR(CAST(o.order_date AS STRING), 1, 10) >= '2024-01-01'
AND LOWER(o.status) LIKE 'completed%';

-- After (OPTIMIZED - direct comparisons enable optimization)
SELECT order_id, customer_id, order_date, total_amount, status
FROM orders o
WHERE o.customer_id = c.customer_id
AND o.order_date >= '2024-01-01'
AND o.status = 'completed';
```

### Expected Improvement
20-35% improvement by enabling BigQuery's optimized execution paths and reducing unnecessary computation.

### Documentation Reference
https://cloud.google.com/bigquery/docs/best-practices-performance-compute

## Partition Filtering

**Pattern ID**: `partition_filtering`
**Performance Impact**: 40-70% improvement
**Use Case**: Queries on partitioned tables without partition filters

### Description
Add partition filters to dramatically reduce the amount of data scanned. This is one of the most effective optimizations for partitioned tables in BigQuery.

### When to Apply
- Queries on partitioned tables without _PARTITIONDATE filters
- Date-based filtering that can leverage partitioning
- Large table scans that can be reduced with partitioning
- Cost optimization for queries on large partitioned datasets

### Example
```sql
-- Before (INEFFICIENT - scans all partitions)
SELECT customer_id, SUM(total_amount)
FROM orders
WHERE order_date >= '2024-01-01'
GROUP BY customer_id;

-- After (OPTIMIZED - scans only relevant partitions)
SELECT customer_id, SUM(total_amount)
FROM orders
WHERE _PARTITIONDATE >= '2024-01-01'
AND order_date >= '2024-01-01'
GROUP BY customer_id;
```

### Expected Improvement
40-70% improvement by dramatically reducing data scanning on partitioned tables.

### Documentation Reference
https://cloud.google.com/bigquery/docs/partitioned-tables

## Clustering Optimization

**Pattern ID**: `clustering_optimization`
**Performance Impact**: 20-35% improvement
**Use Case**: Queries on clustered tables

### Description
Leverage clustering keys in WHERE clauses to improve query performance on clustered tables. BigQuery can skip entire blocks of data when clustering keys are used effectively.

### When to Apply
- Queries on clustered tables
- Equality filters on clustered columns
- Range queries on clustered columns
- Queries that can benefit from data co-location

### Example
```sql
-- Before (Not leveraging clustering)
SELECT * FROM clustered_orders 
WHERE region = 'US-West' 
AND order_date >= '2024-01-01';

-- After (Leveraging clustering keys)
SELECT * FROM clustered_orders 
WHERE customer_id BETWEEN 1000 AND 2000  -- Clustering key first
AND region = 'US-West' 
AND order_date >= '2024-01-01';
```

### Expected Improvement
20-35% improvement by leveraging BigQuery's physical data organization.

### Documentation Reference
https://cloud.google.com/bigquery/docs/clustered-tables

## Materialized View Suggestions

**Pattern ID**: `materialized_view_suggestion`
**Performance Impact**: 60-90% improvement
**Use Case**: Frequently accessed aggregations

### Description
Suggest creating materialized views for frequently executed aggregation queries. Materialized views pre-compute and store query results for instant access.

### When to Apply
- Frequently executed aggregation queries
- Complex calculations repeated often
- Dashboard queries with consistent patterns
- Reports that run multiple times per day

### Example
```sql
-- Frequently run query (slow every time)
SELECT 
    region,
    DATE(order_date) as order_day,
    COUNT(*) as daily_orders,
    SUM(total_amount) as daily_revenue
FROM orders 
WHERE order_date >= '2024-01-01'
GROUP BY region, DATE(order_date);

-- Suggestion: Create materialized view (fast access)
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
60-90% improvement for frequently accessed aggregations by pre-computing results.

### Documentation Reference
https://cloud.google.com/bigquery/docs/materialized-views-intro

## CASE WHEN Optimization

**Pattern ID**: `case_when_optimization`
**Performance Impact**: 15-25% improvement
**Use Case**: Complex conditional logic

### Description
Optimize CASE WHEN statements by reordering conditions for better performance and reducing redundant evaluations.

### When to Apply
- Complex CASE WHEN statements with multiple conditions
- Redundant condition checking
- Nested conditional logic that can be simplified

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
15-25% improvement by reducing redundant condition evaluations.

### Documentation Reference
https://cloud.google.com/bigquery/docs/reference/standard-sql/conditional_expressions

## String Function Optimization

**Pattern ID**: `string_function_optimization`
**Performance Impact**: 15-25% improvement
**Use Case**: Inefficient string operations

### Description
Optimize string functions and operations to improve query performance and enable better optimization by BigQuery.

### When to Apply
- Queries with complex string operations
- LIKE patterns that can be simplified
- String functions that prevent index usage
- Case-insensitive comparisons

### Example
```sql
-- Before (Inefficient string operations)
SELECT * FROM customers 
WHERE UPPER(customer_name) = 'JOHN DOE'
AND SUBSTR(email, 1, 10) = 'john.doe@';

-- After (Optimized string operations)
SELECT * FROM customers 
WHERE customer_name ILIKE 'john doe'
AND email LIKE 'john.doe@%';
```

### Expected Improvement
15-25% improvement by enabling better optimization and reducing string processing overhead.

### Documentation Reference
https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions

## Date Function Optimization

**Pattern ID**: `date_function_optimization`
**Performance Impact**: 20-30% improvement
**Use Case**: Inefficient date operations

### Description
Optimize date functions and operations to improve performance and enable partition pruning.

### When to Apply
- Functions applied to date columns in WHERE clauses
- Date extractions that can be replaced with range comparisons
- Operations that prevent partition pruning

### Example
```sql
-- Before (Function on column prevents optimization)
SELECT * FROM orders 
WHERE EXTRACT(YEAR FROM order_date) = 2024
AND EXTRACT(MONTH FROM order_date) >= 6;

-- After (Range comparison enables optimization)
SELECT * FROM orders 
WHERE order_date >= '2024-06-01' 
AND order_date < '2025-01-01';
```

### Expected Improvement
20-30% improvement by enabling partition pruning and reducing function overhead.

### Documentation Reference
https://cloud.google.com/bigquery/docs/reference/standard-sql/date_functions

## UNION Optimization

**Pattern ID**: `union_optimization`
**Performance Impact**: 20-30% improvement
**Use Case**: UNION operations that can be optimized

### Description
Optimize UNION operations by using UNION ALL when duplicates don't matter and optimizing the structure of UNION queries.

### When to Apply
- UNION operations where duplicates are not a concern
- Multiple UNION operations that can be simplified
- UNION with large datasets

### Example
```sql
-- Before (UNION removes duplicates - slower)
SELECT customer_id FROM active_customers
UNION
SELECT customer_id FROM premium_customers;

-- After (UNION ALL when duplicates don't matter - faster)
SELECT customer_id FROM active_customers
UNION ALL
SELECT customer_id FROM premium_customers;
```

### Expected Improvement
20-30% improvement by avoiding duplicate removal when not needed.

### Documentation Reference
https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax#union

## DISTINCT Optimization

**Pattern ID**: `distinct_optimization`
**Performance Impact**: 20-30% improvement
**Use Case**: DISTINCT operations that can be optimized

### Description
Optimize DISTINCT operations by using GROUP BY when appropriate or combining with other optimizations.

### When to Apply
- DISTINCT on large result sets
- DISTINCT that can be replaced with GROUP BY
- Multiple DISTINCT operations in the same query

### Example
```sql
-- Before (DISTINCT on large result set)
SELECT DISTINCT customer_id, order_date
FROM large_orders_view
WHERE order_date >= '2024-01-01';

-- After (GROUP BY for better performance)
SELECT customer_id, order_date
FROM large_orders_view
WHERE order_date >= '2024-01-01'
GROUP BY customer_id, order_date;
```

### Expected Improvement
20-30% improvement by using more efficient grouping operations.

### Documentation Reference
https://cloud.google.com/bigquery/docs/best-practices-performance-compute

## CTE Optimization

**Pattern ID**: `cte_optimization`
**Performance Impact**: 20-35% improvement
**Use Case**: Common Table Expressions that can be optimized

### Description
Optimize Common Table Expressions (CTEs) by flattening unnecessary CTEs and combining operations where possible.

### When to Apply
- CTEs that add unnecessary complexity
- Multiple CTEs that can be combined
- CTEs that can be replaced with direct queries

### Example
```sql
-- Before (Unnecessary CTE)
WITH customer_orders AS (
    SELECT * FROM orders WHERE customer_id > 0
)
SELECT * FROM customer_orders 
WHERE order_date >= '2024-01-01';

-- After (Flattened query)
SELECT * FROM orders 
WHERE customer_id > 0 
AND order_date >= '2024-01-01';
```

### Expected Improvement
20-35% improvement by reducing query complexity and intermediate processing.

### Documentation Reference
https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax#with_clause

## NULL Handling Optimization

**Pattern ID**: `null_handling_optimization`
**Performance Impact**: 15-25% improvement
**Use Case**: Inefficient NULL handling

### Description
Optimize NULL handling operations to improve performance and enable better optimization by BigQuery.

### When to Apply
- Complex NULL handling that can be simplified
- COALESCE operations that can be optimized
- NULL comparisons that can be improved

### Example
```sql
-- Before (Inefficient NULL handling)
SELECT COALESCE(customer_name, 'Unknown Customer') as name
FROM customers
WHERE COALESCE(status, 'inactive') = 'active';

-- After (Optimized NULL handling)
SELECT IFNULL(customer_name, 'Unknown Customer') as name
FROM customers
WHERE IFNULL(status, 'inactive') = 'active';
```

### Expected Improvement
15-25% improvement by using more efficient NULL handling functions.

### Documentation Reference
https://cloud.google.com/bigquery/docs/reference/standard-sql/conditional_expressions

## LIMIT Optimization

**Pattern ID**: `limit_optimization`
**Performance Impact**: Variable (can be 50%+ for large sorts)
**Use Case**: LIMIT with ORDER BY on large datasets

### Description
Optimize LIMIT operations, especially when combined with ORDER BY, to reduce the amount of data that needs to be sorted.

### When to Apply
- ORDER BY with LIMIT on large datasets
- Queries that sort entire datasets for small result sets
- Top-N queries that can be optimized

### Example
```sql
-- Before (Sorts entire dataset for small result)
SELECT * FROM large_orders 
ORDER BY order_date DESC 
LIMIT 10;

-- After (Optimized with filtering to reduce sort scope)
SELECT * FROM large_orders 
WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
ORDER BY order_date DESC 
LIMIT 10;
```

### Expected Improvement
Variable improvement, can be 50%+ for large datasets with small LIMIT values.

### Documentation Reference
https://cloud.google.com/bigquery/docs/best-practices-performance-compute

## Array and Struct Optimization

**Pattern ID**: `array_struct_optimization`
**Performance Impact**: 20-30% improvement
**Use Case**: Inefficient array and struct operations

### Description
Optimize operations on arrays and structs to improve performance and reduce processing overhead.

### When to Apply
- Complex array operations that can be simplified
- Struct access patterns that can be optimized
- UNNEST operations that can be improved

### Example
```sql
-- Before (Inefficient array operations)
SELECT customer_id 
FROM orders 
WHERE order_id IN UNNEST([1,2,3,4,5]);

-- After (Optimized array handling)
SELECT customer_id 
FROM orders 
WHERE order_id IN (1,2,3,4,5);
```

### Expected Improvement
20-30% improvement by using more efficient array and struct operations.

### Documentation Reference
https://cloud.google.com/bigquery/docs/reference/standard-sql/arrays

## Regular Expression Optimization

**Pattern ID**: `regex_optimization`
**Performance Impact**: 15-25% improvement
**Use Case**: Complex regular expressions

### Description
Optimize regular expression operations by simplifying patterns or replacing with more efficient string operations.

### When to Apply
- Complex regex patterns that can be simplified
- REGEXP_CONTAINS that can be replaced with LIKE
- Multiple regex operations that can be combined

### Example
```sql
-- Before (Complex regex)
SELECT * FROM customers 
WHERE REGEXP_CONTAINS(email, r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$');

-- After (Simpler pattern)
SELECT * FROM customers 
WHERE email LIKE '%@%.%' 
AND email NOT LIKE '%@%@%';
```

### Expected Improvement
15-25% improvement by using simpler, more efficient pattern matching.

### Documentation Reference
https://cloud.google.com/bigquery/docs/reference/standard-sql/string_functions

## Cross JOIN Elimination

**Pattern ID**: `cross_join_elimination`
**Performance Impact**: 30-50% improvement
**Use Case**: Accidental cross joins

### Description
Eliminate accidental cross joins by converting them to proper INNER JOINs with explicit conditions.

### When to Apply
- Comma-separated table lists without proper JOIN conditions
- Queries that accidentally create Cartesian products
- Missing JOIN conditions that create cross joins

### Example
```sql
-- Before (Accidental CROSS JOIN - very inefficient)
SELECT * FROM customers c, orders o 
WHERE c.customer_id = o.customer_id;

-- After (Explicit INNER JOIN - much more efficient)
SELECT * FROM customers c 
INNER JOIN orders o ON c.customer_id = o.customer_id;
```

### Expected Improvement
30-50% improvement by eliminating expensive Cartesian products.

### Documentation Reference
https://cloud.google.com/bigquery/docs/best-practices-performance-compute#optimize_your_join_patterns

## Aggregation Function Optimization

**Pattern ID**: `aggregation_optimization`
**Performance Impact**: 20-40% improvement
**Use Case**: Inefficient aggregation patterns

### Description
Optimize aggregation functions and GROUP BY operations for better performance.

### When to Apply
- Multiple aggregation functions that can be optimized
- GROUP BY operations on large datasets
- Aggregations that can leverage approximate functions

### Example
```sql
-- Before (Multiple exact aggregations - slow on large data)
SELECT 
    region,
    COUNT(*) as total_orders,
    COUNT(DISTINCT customer_id) as unique_customers,
    AVG(total_amount) as avg_amount
FROM large_orders 
GROUP BY region;

-- After (Mixed exact and approximate - much faster)
SELECT 
    region,
    COUNT(*) as total_orders,
    APPROX_COUNT_DISTINCT(customer_id) as unique_customers,
    AVG(total_amount) as avg_amount
FROM large_orders 
GROUP BY region;
```

### Expected Improvement
20-40% improvement by using appropriate aggregation strategies.

### Documentation Reference
https://cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions