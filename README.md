# BigQuery Query Optimizer

An AI-powered BigQuery SQL query optimizer with **MCP server integration** and **schema validation** that automatically improves query performance while preserving exact business logic and preventing column errors.

## Problem Statement

Organizations using BigQuery often have queries written by humans that fail to meet performance SLAs. These underperforming queries cost money through inefficient compute usage, delay business insights, and frustrate end users. While BigQuery documentation contains extensive optimization best practices, developers often lack the time or expertise to apply these consistently across hundreds or thousands of queries.

## Solution

Enhanced AI-powered BigQuery query optimizer with MCP integration that:
- **Input**: Underperforming BigQuery SQL query
- **Output**: Schema-validated optimized query with identical results but improved performance
- **Additional Output**: MCP-enhanced explanations with official documentation references
- **NEW**: Schema validation prevents column errors and BigQuery failures

## Success Metrics

1. **Functional Accuracy**: 100% - Optimized queries must return identical results to original queries
2. **Performance Improvement**: Target 30-50% reduction in query execution time
3. **Documentation Coverage**: Tool references 20+ distinct BigQuery optimization patterns
4. **Explanation Quality**: Each optimization includes specific documentation references
5. **Test Coverage**: Comprehensive test scenarios demonstrating various optimization patterns
6. **Schema Validation**: 100% - No column errors or BigQuery failures
7. **MCP Integration**: Documentation-backed optimization suggestions

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
   # Main API on port 8080 with embedded MCP components
   ```
   
   **Optional - Start MCP Server separately** (for advanced debugging):
   ```bash
   python -m src.mcp_server.server
   # Runs on http://localhost:8001 (documentation service)
   ```

4. **Open http://localhost:8080** and start optimizing queries!

## Architecture

### **Enhanced Workflow Integration**:

1. **Enhanced Documentation Crawler** (`src/crawler/`): Crawls Google Cloud BigQuery documentation with better pattern extraction
2. **MCP Server** (`src/mcp_server/`): Model Context Protocol server (Port 8001) serving documentation-backed suggestions  
3. **Enhanced Schema Extractor** (`src/optimizer/query_optimizer.py`): Extracts actual table schemas and validates column usage
4. **Enhanced Query Optimizer** (`src/optimizer/`): Main optimization engine with MCP integration and schema validation
5. **Enhanced AI Optimizer** (`src/optimizer/ai_optimizer.py`): Gemini-powered optimization with MCP context and schema awareness
6. **Enhanced BigQuery Client** (`src/optimizer/bigquery_client.py`): BigQuery service wrapper with schema extraction
7. **Enhanced Result Validator** (`src/optimizer/validator.py`): Ensures optimized queries return identical results with schema validation
8. **Enhanced Web Interface** (`src/api/`): REST API (Port 8080) and web UI with MCP integration indicators

### **Enhanced Key Features**:
- ✅ **Schema Validation**: Extracts actual column names and validates usage
- ✅ **MCP Integration**: Documentation-backed optimization suggestions with official references
- ✅ **Port Separation**: Main API (8080) and MCP Server (8001) with no conflicts
- ✅ **Error Prevention**: Comprehensive validation prevents BigQuery failures
- ✅ **Enhanced Context**: AI optimization with official documentation backing

## Optimization Patterns (20+ Supported)

The optimizer applies Google's official BigQuery best practices:

- **Enhanced Column Pruning**: Replace SELECT * with actual schema columns (prevents errors)
- **Enhanced JOIN Reordering**: Optimize JOIN order with schema awareness
- **Enhanced Subquery Conversion**: Convert subqueries to JOINs with schema validation
- **Enhanced Approximate Aggregation**: Use approximate functions with MCP documentation backing
- **Enhanced Window Function Optimization**: Improve specifications with official best practices
- **Enhanced Predicate Pushdown**: Move filters with schema awareness
- **Enhanced Clustering Optimization**: Leverage clustering with actual table metadata
- **Enhanced Materialized View Suggestions**: Identify opportunities with MCP context
- **And 14+ more enhanced patterns with schema validation and MCP backing...**

## Usage Examples

### Web Interface
1. Open http://localhost:8080
2. See "Enhanced with Model Context Protocol (MCP) Server Integration"
3. Enter your BigQuery SQL query
4. Configure your Google Cloud Project ID
5. Click "Optimize Query"
6. View schema-validated optimized query with MCP-enhanced suggestions and documentation references

### Command Line
```bash
# Optimize a single query
python -m src.optimizer.main optimize --query "SELECT * FROM orders WHERE date > '2024-01-01'"
# Enhanced with MCP integration and schema validation

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

optimizer = BigQueryOptimizer()  # Enhanced with MCP + schema integration
result = optimizer.optimize_query("""
    SELECT * FROM orders 
    WHERE order_date >= '2024-01-01'
""")

print(f"Optimized Query:\n{result.optimized_query}")
print(f"Optimizations Applied: {result.total_optimizations}")
print(f"Expected Improvement: {result.estimated_improvement:.1%}")
print(f"Schema Validated: No column errors")
print(f"MCP Enhanced: {len(result.optimizations_applied)} patterns with official documentation backing")
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

The enhanced test suite includes:
1. **Enhanced Documentation Crawler Test**: Verifies Google Cloud docs with better pattern extraction
2. **Enhanced MCP Server Test**: Tests Model Context Protocol server with schema integration
3. **Enhanced Simple Query Test**: Basic SELECT with schema validation
4. **Enhanced Complex JOIN Test**: Multi-table JOIN with schema-aware optimization
5. **Enhanced Aggregation Test**: GROUP BY with schema validation and MCP context
6. **Enhanced Window Function Test**: Window functions with schema awareness
7. **Enhanced Nested Query Test**: Nested subqueries with schema validation
8. **Enhanced Business Logic Preservation**: Ensures 100% identical results with schema validation
9. **Enhanced Performance Benchmarks**: Validates 30-50% improvement with MCP enhancement
10. **Enhanced MCP Integration Test**: Verifies MCP server enhances optimization quality
11. **NEW: Schema Validation Test**: Ensures no column errors in optimized queries
12. **NEW: Column Error Prevention Test**: Validates schema-aware optimization

## Key Features

### Business Logic Preservation
- **100% Functional Accuracy**: Optimized queries return identical results
- **Enhanced Validation**: Row-by-row comparison with schema validation
- **Enhanced Visual Proof**: Side-by-side display with schema information
- **Zero Tolerance**: Any difference in results fails the optimization
- **NEW: Schema Safety**: Prevents column errors and BigQuery failures

### Performance Optimization
- **30-50% Target**: Aims for significant performance improvements
- **Real Measurements**: Actual BigQuery performance metrics
- **Enhanced Cost Reduction**: Reduces bytes processed with schema-aware optimization
- **SLA Compliance**: Helps queries meet performance requirements
- **NEW: Error Prevention**: Schema validation prevents production failures

### AI-Powered Intelligence
- **Enhanced Google's Best Practices**: Applies official patterns with schema awareness
- **Enhanced MCP Server Integration**: Model Context Protocol with documentation backing
- **Enhanced Context Awareness**: Considers table schemas, metadata, and MCP suggestions
- **Enhanced Documentation References**: Each optimization links to official docs via MCP
- **Enhanced Explanation Quality**: Clear explanations with official documentation backing
- **NEW: Schema Intelligence**: AI understands actual table structures

### Developer Experience
- **Enhanced Web Interface**: Browser-based interface with MCP integration indicators
- **Enhanced Command Line Tools**: CLI with schema validation and MCP integration
- **Enhanced Python API**: Programmatic access with schema awareness
- **Enhanced Batch Processing**: Optimize hundreds of queries with schema validation

## Documentation

- [Architecture Guide](docs/architecture.md)
- [Enhanced Workflow Integration](docs/workflow_integration.md)
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

**Transform your underperforming BigQuery queries into schema-validated, MCP-enhanced, optimized solutions while preserving exact business logic and preventing errors!**