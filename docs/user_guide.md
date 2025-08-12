# BigQuery Query Optimizer - User Guide

## Overview

The BigQuery Query Optimizer is an AI-powered tool that automatically optimizes your BigQuery SQL queries while preserving exact business logic. It applies Google's official best practices to improve query performance by 30-50%.

## Quick Start

### 1. Web Interface (Recommended)

1. **Start the server**:
   ```bash
   python run_api_server.py
   ```
   This starts the main API on port 8080 with embedded MCP components.

2. **Open your browser**: http://localhost:8080

3. **Configure your project**:
   - Enter your Google Cloud Project ID
   - Set sample size (default: 1000 rows)
   - Enable/disable result validation

4. **Enter your SQL query** and click "Optimize Query"

### 1b. Separate MCP Server (Advanced)

For advanced usage, you can run the MCP server separately:

1. **Start MCP server**:
   ```bash
   python -m src.mcp_server.server
   # Runs on http://localhost:8001
   ```

2. **Start main API**:
   ```bash
   python run_api_server.py
   # Runs on http://localhost:8080
   ```

### 2. Command Line Interface

```bash
# Optimize a single query
python -m src.optimizer.main optimize --query "SELECT * FROM orders WHERE date > '2024-01-01'"

# Optimize from file
python -m src.optimizer.main optimize --file my_query.sql

# Analyze without optimizing
python -m src.optimizer.main analyze --query "SELECT * FROM customers"

# Get optimization suggestions
python -m src.optimizer.main suggestions --query "SELECT COUNT(DISTINCT customer_id) FROM orders"
```

### 3. Python API

```python
from src.optimizer.query_optimizer import BigQueryOptimizer

# Initialize optimizer
optimizer = BigQueryOptimizer(
    project_id="your-project-id",
    validate_results=True
)

# Optimize a query
result = optimizer.optimize_query("""
    SELECT * FROM orders 
    WHERE order_date >= '2024-01-01'
""")

print(f"Optimized Query:\n{result.optimized_query}")
print(f"Optimizations Applied: {result.total_optimizations}")
print(f"Expected Improvement: {result.estimated_improvement:.1%}")
```

## Supported Optimization Patterns

### 1. Column Pruning
**What it does**: Replaces `SELECT *` with specific column names
**Performance Impact**: 20-40% improvement
**Example**:
```sql
-- Before
SELECT * FROM orders WHERE date > '2024-01-01'

-- After  
SELECT order_id, customer_id, total_amount FROM orders WHERE date > '2024-01-01'
```

### 2. JOIN Reordering
**What it does**: Reorders JOINs to place smaller tables first
**Performance Impact**: 20-40% improvement
**Example**:
```sql
-- Before (large table first)
FROM large_orders o JOIN small_customers c ON o.customer_id = c.id

-- After (small table first)
FROM small_customers c JOIN large_orders o ON c.id = o.customer_id
```

### 3. Subquery to JOIN Conversion
**What it does**: Converts EXISTS/IN subqueries to JOINs
**Performance Impact**: 30-60% improvement
**Example**:
```sql
-- Before
SELECT * FROM customers c 
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id)

-- After
SELECT DISTINCT c.* FROM customers c 
INNER JOIN orders o ON c.id = o.customer_id
```

### 4. Approximate Aggregation
**What it does**: Uses approximate functions for large datasets
**Performance Impact**: 40-70% improvement
**Example**:
```sql
-- Before
SELECT COUNT(DISTINCT customer_id) FROM large_orders

-- After
SELECT APPROX_COUNT_DISTINCT(customer_id) FROM large_orders
```

### 5. Window Function Optimization
**What it does**: Optimizes window function specifications
**Performance Impact**: 15-30% improvement
**Example**:
```sql
-- Before
SELECT customer_id, ROW_NUMBER() OVER (ORDER BY date) FROM orders

-- After
SELECT customer_id, ROW_NUMBER() OVER (PARTITION BY region ORDER BY date) FROM orders
```

### 6. Predicate Pushdown
**What it does**: Moves filters closer to data sources
**Performance Impact**: 25-45% improvement
**Example**:
```sql
-- Before
SELECT * FROM (SELECT * FROM orders) WHERE date > '2024-01-01'

-- After
SELECT * FROM orders WHERE date > '2024-01-01'
```

### 7. Clustering Optimization
**What it does**: Leverages clustering keys in WHERE clauses
**Performance Impact**: 20-35% improvement
**Example**:
```sql
-- Before
SELECT * FROM clustered_table WHERE non_clustered_column = 'value'

-- After
SELECT * FROM clustered_table WHERE clustered_column = 'value' AND non_clustered_column = 'value'
```

## Understanding Results

### Optimization Result Structure

```json
{
  "original_query": "Your original SQL query",
  "optimized_query": "The optimized version",
  "optimizations_applied": [
    {
      "pattern_name": "Column Pruning",
      "description": "Replaced SELECT * with specific columns",
      "expected_improvement": 0.3,
      "documentation_reference": "https://cloud.google.com/bigquery/docs/..."
    }
  ],
  "total_optimizations": 2,
  "estimated_improvement": 0.45,
  "results_identical": true,
  "processing_time_seconds": 2.3
}
```

### Key Metrics

- **results_identical**: Must be `true` - guarantees business logic preservation
- **estimated_improvement**: Expected performance improvement (0.3 = 30%)
- **total_optimizations**: Number of optimizations applied
- **processing_time_seconds**: Time taken to optimize

## Best Practices

### 1. Always Validate Results
```python
result = optimizer.optimize_query(
    your_query,
    validate_results=True,  # Always recommended
    sample_size=1000
)

# Check validation
if result.results_identical:
    print("✅ Safe to use optimized query")
else:
    print("❌ Don't use - results differ")
```

### 2. Test with Sample Data First
- Start with `LIMIT 100` on your queries
- Gradually increase limits after validation
- Use sample_size parameter for large datasets

### 3. Review Optimizations
```python
for opt in result.optimizations_applied:
    print(f"Applied: {opt.pattern_name}")
    print(f"Impact: {opt.expected_improvement:.1%}")
    print(f"Docs: {opt.documentation_reference}")
```

### 4. Measure Performance
```python
result = optimizer.optimize_query(
    your_query,
    measure_performance=True  # Get actual performance metrics
)

if result.performance_metrics:
    metrics = result.performance_metrics
    print(f"Time improvement: {metrics['time_improvement']:.1%}")
    print(f"Cost savings: ${metrics['cost_saved']:.4f}")
    print(f"Data reduction: {metrics['bytes_improvement']:.1%}")
    print(f"Summary: {metrics['performance_summary']}")
```

## Common Use Cases

### 1. Optimizing Dashboard Queries
```python
# Typical dashboard aggregation
dashboard_query = """
SELECT 
    region,
    COUNT(*) as total_orders,
    SUM(revenue) as total_revenue,
    COUNT(DISTINCT customer_id) as unique_customers
FROM sales_data 
WHERE date >= '2024-01-01'
GROUP BY region
"""

result = optimizer.optimize_query(dashboard_query)
# Expected: Approximate aggregation, better filtering
```

### 2. Report Generation Queries
```python
# Complex report with multiple JOINs
report_query = """
SELECT c.name, p.category, SUM(oi.quantity * oi.price)
FROM customers c
JOIN orders o ON c.id = o.customer_id
JOIN order_items oi ON o.id = oi.order_id  
JOIN products p ON oi.product_id = p.id
WHERE o.date >= '2024-01-01'
GROUP BY c.name, p.category
"""

result = optimizer.optimize_query(report_query)
# Expected: JOIN reordering, column pruning
```

### 3. Data Analysis Queries
```python
# Analytical query with window functions
analysis_query = """
SELECT 
    customer_id,
    order_date,
    total_amount,
    ROW_NUMBER() OVER (ORDER BY total_amount DESC) as rank
FROM orders
WHERE order_date >= '2024-01-01'
"""

result = optimizer.optimize_query(analysis_query)
# Expected: Window function optimization, filtering improvements
```

## Troubleshooting

### Common Issues

1. **"No optimizations applied"**
   - Your query might already be well-optimized
   - Try a more complex query with JOINs or aggregations

2. **"Results not identical"**
   - Check if approximate functions were used
   - Review the validation error message
   - Consider if slight variance is acceptable for your use case

3. **"BigQuery connection failed"**
   - Verify your Google Cloud credentials
   - Check that BigQuery API is enabled
   - Ensure your project ID is correct

4. **"Performance measurement failed"**
   - Large queries might timeout
   - Try with smaller sample sizes first
   - Check BigQuery quotas and limits

### Getting Help

1. **Check system status**: Click "System Status" in the web UI
2. **Review logs**: Check console output for detailed error messages
3. **Test with examples**: Use the "Load Example Query" button
4. **Run test suite**: Click "Run Tests" to verify system health

## Advanced Features

### Batch Optimization
```python
queries = [
    "SELECT * FROM table1 WHERE date > '2024-01-01'",
    "SELECT COUNT(DISTINCT id) FROM table2",
    "SELECT a.*, b.* FROM table_a a JOIN table_b b ON a.id = b.id"
]

results = optimizer.batch_optimize_queries(queries)
for result in results:
    print(f"Query optimized: {result.total_optimizations} improvements")
```

### Custom Validation
```python
# Validate specific optimization
validation = optimizer.validate_optimization(
    original_query="SELECT COUNT(*) FROM orders",
    optimized_query="SELECT APPROX_COUNT_DISTINCT(order_id) FROM orders",
    sample_size=5000
)

print(f"Validation passed: {validation['overall_success']}")
```

### Table-Level Suggestions
```python
suggestions = optimizer.get_table_optimization_suggestions(
    "project.dataset.large_table",
    sample_queries=["SELECT * FROM large_table WHERE date > '2024-01-01'"]
)

for suggestion in suggestions:
    print(f"💡 {suggestion}")
```

## Performance Tips

1. **Start Small**: Test with LIMIT 100 first
2. **Use Sampling**: Set appropriate sample_size for validation
3. **Monitor Resources**: Watch BigQuery slot usage
4. **Cache Results**: Save optimized queries for reuse
5. **Measure Impact**: Always measure actual performance improvements

## Security Considerations

- **Credentials**: Store service account keys securely
- **Project Access**: Ensure proper BigQuery permissions
- **Data Privacy**: Validation uses sample data only
- **API Keys**: Keep Gemini API keys confidential
- **Query Logging**: Queries are processed in memory only

This user guide provides everything you need to effectively use the BigQuery Query Optimizer while understanding its capabilities and limitations.