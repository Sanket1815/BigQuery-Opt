# BigQuery Query Optimizer

An AI-powered BigQuery SQL query optimizer with **direct SQL processing** and **markdown pattern files** that automatically improves query performance while preserving exact business logic.

## Problem Statement

Organizations using BigQuery often have queries written by humans that fail to meet performance SLAs. These underperforming queries cost money through inefficient compute usage, delay business insights, and frustrate end users. While BigQuery documentation contains extensive optimization best practices, developers often lack the time or expertise to apply these consistently across hundreds or thousands of queries.

## Solution

Simplified AI-powered BigQuery query optimizer with direct SQL processing that:
- **Input**: Underperforming BigQuery SQL query
- **Output**: Optimized query with identical results but improved performance
- **Additional Output**: LLM-generated explanations with pattern-based optimizations
- **NEW**: Direct SQL processing with separate markdown pattern files

## Success Metrics

1. **Functional Accuracy**: 100% - Optimized queries must return identical results to original queries
2. **Performance Improvement**: Target 30-50% reduction in query execution time
3. **Pattern Coverage**: Tool uses 8+ distinct BigQuery optimization patterns from separate files
4. **Explanation Quality**: Each optimization includes specific documentation references
5. **Test Coverage**: Comprehensive test scenarios demonstrating various optimization patterns
6. **Direct Processing**: Raw SQL queries processed without complex transformations
7. **Modular Patterns**: Optimization patterns stored as separate markdown files

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
   # Main API on port 8080 with direct SQL processing
   ```
   
   **Optional - Start MCP Server separately** (for direct SQL processing):
   ```bash
   python -m src.mcp_server.server
   # Runs on http://localhost:8001 (direct SQL processing service)
   ```

4. **Open http://localhost:8080** and start optimizing queries!

## Architecture

### **Simplified Workflow**:

1. **Pattern Files** (`data/optimization_patterns/*.md`): Individual markdown files for each optimization pattern
2. **MCP Server** (`src/mcp_server/`): Direct SQL processing server (Port 8001)
3. **SQL Handler** (`src/mcp_server/handlers.py`): Direct SQL query processing with pattern matching
4. **Query Optimizer** (`src/optimizer/`): Simplified orchestration engine
5. **LLM Optimizer** (`src/optimizer/llm_optimizer.py`): Direct LLM optimization with system/user prompts
6. **BigQuery Client** (`src/optimizer/bigquery_client.py`): Table and column validation
7. **Web Interface** (`src/api/`): REST API (Port 8080) and web UI

### **Key Features**:
- ✅ **Direct SQL Processing**: Raw SQL queries processed without complex transformations
- ✅ **Modular Pattern Files**: Each optimization pattern stored as separate markdown file
- ✅ **LLM Direct Integration**: System and user prompts sent directly to LLM
- ✅ **Simplified Architecture**: Streamlined workflow with fewer components
- ✅ **Pattern-Based Optimization**: Documentation context sent directly to LLM

## Optimization Patterns (8+ Supported)

The optimizer applies Google's official BigQuery best practices:

- **Column Pruning**: Replace SELECT * with specific columns (30-50% improvement)
- **JOIN Reordering**: Optimize JOIN order for better performance (25-50% improvement)
- **Subquery Conversion**: Convert subqueries to JOINs (40-70% improvement)
- **Approximate Aggregation**: Use APPROX_COUNT_DISTINCT for large datasets (50-80% improvement)
- **Window Function Optimization**: Add proper PARTITION BY clauses (25-40% improvement)
- **Predicate Pushdown**: Move filters closer to data sources (25-45% improvement)
- **HAVING to WHERE Conversion**: Convert HAVING to WHERE when possible (15-25% improvement)
- **Unnecessary Operations**: Remove unnecessary CAST/string operations (20-35% improvement)

## Usage Examples

### Web Interface
1. Open http://localhost:8080
2. See "Simplified with Direct SQL Processing and Pattern Files"
3. Enter your BigQuery SQL query
4. Configure your Google Cloud Project ID
5. Click "Optimize Query"
6. View optimized query with LLM-generated improvements and pattern explanations

### Command Line
```bash
# Optimize a single query
python -m src.optimizer.main optimize --query "SELECT * FROM orders WHERE date > '2024-01-01'"
# Simplified with direct SQL processing

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

optimizer = BigQueryOptimizer()  # Simplified with direct processing
result = optimizer.optimize_query("""
    SELECT * FROM orders 
    WHERE order_date >= '2024-01-01'
""")

print(f"Optimized Query:\n{result.optimized_query}")
print(f"Optimizations Applied: {result.total_optimizations}")
print(f"Expected Improvement: {result.estimated_improvement:.1%}")
print(f"Pattern-Based: {len(result.optimizations_applied)} patterns applied")
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

The simplified test suite includes:
1. **Direct SQL Processing Test**: Verifies raw SQL processing workflow
2. **Pattern File Loading Test**: Tests markdown pattern file loading
3. **Simple Query Test**: Basic SELECT with direct processing
4. **Complex JOIN Test**: Multi-table JOIN with pattern-based optimization
5. **Aggregation Test**: GROUP BY with LLM optimization
6. **Window Function Test**: Window functions with direct LLM processing
7. **Nested Query Test**: Nested subqueries with pattern-based conversion
8. **Business Logic Preservation**: Ensures 100% identical results
9. **Performance Benchmarks**: Validates 30-50% improvement
10. **LLM Integration Test**: Verifies direct LLM optimization quality
11. **Table Validation Test**: Ensures valid table and column references
12. **Pattern Coverage Test**: Validates all patterns are applicable

## Key Features

### Business Logic Preservation
- **100% Functional Accuracy**: Optimized queries return identical results
- **Direct Validation**: Row-by-row comparison with table validation
- **Visual Proof**: Side-by-side display with optimization explanations
- **Zero Tolerance**: Any difference in results fails the optimization
- **Table Safety**: Validates table and column existence

### Performance Optimization
- **30-50% Target**: Aims for significant performance improvements
- **Real Measurements**: Actual BigQuery performance metrics
- **Cost Reduction**: Reduces bytes processed with pattern-based optimization
- **SLA Compliance**: Helps queries meet performance requirements
- **Error Prevention**: Table validation prevents production failures

### AI-Powered Intelligence
- **Google's Best Practices**: Applies official patterns from markdown files
- **Direct LLM Integration**: System and user prompts with documentation context
- **Pattern Awareness**: Uses separate pattern files for optimization guidance
- **Documentation References**: Each optimization links to official BigQuery docs
- **Clear Explanations**: LLM-generated explanations with pattern context
- **Table Intelligence**: Validates against actual BigQuery table structures

### Developer Experience
- **Simplified Web Interface**: Browser-based interface with direct processing
- **Command Line Tools**: CLI with direct SQL optimization
- **Python API**: Programmatic access with LLM integration
- **Batch Processing**: Optimize multiple queries with pattern-based optimization

## Documentation

- [Architecture Guide](docs/architecture.md)
- [Simplified Workflow](docs/workflow_integration.md)
- [Optimization Patterns](docs/optimization_patterns.md)
- [User Guide](docs/user_guide.md)

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

**Transform your underperforming BigQuery queries into pattern-optimized, LLM-enhanced solutions with direct processing while preserving exact business logic!**