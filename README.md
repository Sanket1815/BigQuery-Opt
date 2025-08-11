# BigQuery Query Optimizer

An AI-powered BigQuery SQL query optimizer that automatically improves query performance while preserving exact business logic and results.

## Problem Statement

Organizations using BigQuery often have queries written by humans that fail to meet performance SLAs. These underperforming queries cost money through inefficient compute usage, delay business insights, and frustrate end users. While BigQuery documentation contains extensive optimization best practices, developers often lack the time or expertise to apply these consistently across hundreds or thousands of queries.

## Solution

AI-powered BigQuery query optimizer that:
- **Input**: Underperforming BigQuery SQL query
- **Output**: Optimized query with identical results but improved performance
- **Additional Output**: Clear explanation of optimizations applied and why

## Success Metrics

1. **Functional Accuracy**: 100% - Optimized queries must return identical results to original queries
2. **Performance Improvement**: Target 30-50% reduction in query execution time
3. **Documentation Coverage**: Tool references 20+ distinct BigQuery optimization patterns
4. **Explanation Quality**: Each optimization includes specific documentation references
5. **Test Coverage**: Comprehensive test scenarios demonstrating various optimization patterns

## Quick Start

1. **Setup Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure Google Cloud**:
   ```bash
   export GOOGLE_CLOUD_PROJECT=your-project-id
   export GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
   export GEMINI_API_KEY=your-gemini-api-key
   ```

3. **Start the Web Interface**:
   ```bash
   python run_api_server.py
   ```
   
   **Optional - Start MCP Server separately** (for advanced usage):
   ```bash
   python -m src.mcp_server.server
   # Runs on http://localhost:8001 (different from main API on 8080)
   ```

4. **Open http://localhost:8080** and start optimizing queries!

## Architecture

### **Complete Workflow Integration**:

1. **Documentation Crawler** (`src/crawler/`): Crawls Google Cloud BigQuery documentation for best practices
2. **MCP Server** (`src/mcp_server/`): Model Context Protocol server (Port 8001) that serves documentation and optimization suggestions  
3. **Schema Extractor** (`src/optimizer/query_optimizer.py`): Extracts actual table schemas and column names from BigQuery
4. **Query Optimizer** (`src/optimizer/`): Main optimization engine with MCP integration and schema validation
5. **AI Optimizer** (`src/optimizer/ai_optimizer.py`): Gemini-powered optimization enhanced with MCP context and schema awareness
6. **BigQuery Client** (`src/optimizer/bigquery_client.py`): BigQuery service wrapper with performance measurement
7. **Result Validator** (`src/optimizer/validator.py`): Ensures optimized queries return identical results
8. **Web Interface** (`src/api/`): REST API (Port 8080) and web UI for easy interaction

### **Key Enhancements**:
- ✅ **Schema Validation**: Only uses existing table columns in optimized queries
- ✅ **MCP Integration**: Documentation-backed optimization suggestions
- ✅ **Port Separation**: Main API (8080) and MCP Server (8001) on different ports
- ✅ **Error Prevention**: No more "column not found" errors

## Optimization Patterns (20+ Supported)

The optimizer applies Google's official BigQuery best practices:

- **Partition Filtering**: Add partition filters to reduce data scanned
- **Column Pruning**: Replace SELECT * with specific columns
- **Subquery to JOIN Conversion**: Convert subqueries to JOINs for better performance
- **JOIN Reordering**: Optimize JOIN order based on table sizes
- **Approximate Aggregation**: Use approximate functions for large datasets
- **Window Function Optimization**: Improve window function specifications
- **Predicate Pushdown**: Move filters closer to data sources
- **Clustering Optimization**: Leverage clustering keys in WHERE clauses
- **Materialized View Suggestions**: Identify opportunities for materialized views
- **And 10+ more patterns...**

## Usage Examples

### Web Interface
1. Open http://localhost:8080
2. Enter your BigQuery SQL query
3. Configure your Google Cloud Project ID
4. Click "Optimize Query"
5. View optimized query with MCP-enhanced suggestions and documentation references

### Command Line
```bash
# Optimize a single query
python -m src.optimizer.main optimize --query "SELECT * FROM orders WHERE date > '2024-01-01'"

# Optimize from file
python -m src.optimizer.main optimize --file queries/slow_query.sql

# Analyze without optimizing
python -m src.optimizer.main analyze --query "SELECT * FROM customers"

# Batch optimization
python -m src.optimizer.main batch --queries-file queries/batch_queries.json
```

### Python API
```python
from src.optimizer.query_optimizer import BigQueryOptimizer

optimizer = BigQueryOptimizer()
result = optimizer.optimize_query("""
    SELECT * FROM orders 
    WHERE order_date >= '2024-01-01'
""")

print(f"Optimized Query:\n{result.optimized_query}")
print(f"Optimizations Applied: {result.total_optimizations}")
print(f"Expected Improvement: {result.estimated_improvement:.1%}")
print(f"Documentation References: {len(result.optimizations_applied)} patterns with official docs")
```

## Testing

Run the comprehensive test suite:

```bash
# Run all tests
python -m pytest tests/

# Run specific test categories
python -m pytest tests/unit/
python -m pytest tests/integration/

# Run with coverage
python -m pytest --cov=src tests/
```

### Test Scenarios

The test suite includes:
1. **Documentation Crawler Test**: Verifies Google Cloud docs are properly crawled
2. **MCP Server Test**: Tests Model Context Protocol server functionality
3. **Simple Query Test**: Basic SELECT with inefficient WHERE clause
4. **Complex JOIN Test**: Multi-table JOIN with suboptimal ordering
5. **Aggregation Test**: GROUP BY without proper partitioning
6. **Window Function Test**: Inefficient window specifications
7. **Nested Query Test**: Deeply nested subqueries that can be flattened
8. **Business Logic Preservation**: Ensures 100% identical results
9. **Performance Benchmarks**: Validates 30-50% improvement targets
10. **MCP Integration Test**: Verifies MCP server enhances optimization quality

## Key Features

### Business Logic Preservation
- **100% Functional Accuracy**: Optimized queries return identical results
- **Comprehensive Validation**: Row-by-row comparison of query results
- **Visual Proof**: Side-by-side display of original vs optimized results
- **Zero Tolerance**: Any difference in results fails the optimization

### Performance Optimization
- **30-50% Target**: Aims for significant performance improvements
- **Real Measurements**: Actual BigQuery performance metrics
- **Cost Reduction**: Reduces bytes processed and compute costs
- **SLA Compliance**: Helps queries meet performance requirements

### AI-Powered Intelligence
- **Google's Best Practices**: Applies official BigQuery optimization patterns
- **MCP Server Integration**: Enhanced with Model Context Protocol for better documentation access
- **Context Awareness**: Considers table metadata and query structure
- **Documentation References**: Each optimization links to official docs
- **Explanation Quality**: Clear explanations of why optimizations were applied

### Developer Experience
- **Web Interface**: Easy-to-use browser-based interface
- **Command Line Tools**: Scriptable CLI for automation
- **Python API**: Programmatic access for integration
- **Batch Processing**: Optimize hundreds of queries at once

## Documentation

- [Architecture Guide](docs/architecture.md)
- [API Documentation](docs/api.md)
- [Optimization Patterns](docs/optimization_patterns.md)
- [Performance Testing](docs/performance_testing.md)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
- Check the documentation
- Review test examples
- Open an issue on GitHub

---

**Transform your underperforming BigQuery queries into optimized, cost-effective solutions while preserving exact business logic!**