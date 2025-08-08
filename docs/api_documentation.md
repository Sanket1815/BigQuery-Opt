# BigQuery Query Optimizer - API Documentation

## Overview

The BigQuery Query Optimizer provides multiple APIs for integrating AI-powered SQL optimization into your applications and workflows.

## REST API Endpoints

### Base URL
```
http://localhost:8080/api/v1
```

### Authentication
Currently no authentication required for development. For production, implement API keys or OAuth.

---

## Core Optimization Endpoints

### POST `/optimize`
Optimize a BigQuery SQL query with AI-powered improvements.

**Request Body:**
```json
{
  "query": "SELECT * FROM orders WHERE order_date >= '2024-01-01'",
  "project_id": "your-project-id",
  "validate": true,
  "measure_performance": false,
  "sample_size": 1000
}
```

**Parameters:**
- `query` (string, required): SQL query to optimize
- `project_id` (string, optional): Google Cloud Project ID
- `validate` (boolean, default: true): Validate query results are identical
- `measure_performance` (boolean, default: false): Measure actual performance
- `sample_size` (integer, default: 1000): Sample size for validation

**Response:**
```json
{
  "original_query": "SELECT * FROM orders WHERE order_date >= '2024-01-01'",
  "optimized_query": "SELECT order_id, customer_id, total_amount FROM orders WHERE order_date >= '2024-01-01'",
  "optimizations_applied": [
    {
      "pattern_id": "column_pruning",
      "pattern_name": "Column Pruning",
      "description": "Replaced SELECT * with specific columns to reduce data transfer",
      "before_snippet": "SELECT *",
      "after_snippet": "SELECT order_id, customer_id, total_amount",
      "expected_improvement": 0.25,
      "confidence_score": 0.9,
      "documentation_reference": "https://cloud.google.com/bigquery/docs/best-practices-performance-input"
    }
  ],
  "total_optimizations": 1,
  "estimated_improvement": 0.25,
  "actual_improvement": 0.32,
  "results_identical": true,
  "validation_error": null,
  "processing_time_seconds": 2.3,
  "detailed_comparison": {
    "results_identical": true,
    "original_row_count": 150,
    "optimized_row_count": 150,
    "comparison_summary": "Results are identical (150 rows)",
    "sample_original": [...],
    "sample_optimized": [...]
  }
}
```

**Status Codes:**
- `200`: Success
- `400`: Bad request (invalid SQL, missing parameters)
- `503`: Service unavailable (BigQuery/AI connection failed)
- `500`: Internal server error

---

### POST `/analyze`
Analyze a SQL query without optimizing it.

**Request Body:**
```json
{
  "query": "SELECT * FROM orders WHERE order_date >= '2024-01-01'",
  "project_id": "your-project-id"
}
```

**Response:**
```json
{
  "original_query": "SELECT * FROM orders WHERE order_date >= '2024-01-01'",
  "query_hash": "abc123...",
  "complexity": "moderate",
  "table_count": 1,
  "join_count": 0,
  "subquery_count": 0,
  "window_function_count": 0,
  "aggregate_function_count": 0,
  "has_partition_filter": false,
  "has_clustering_filter": true,
  "potential_issues": [
    "Using SELECT * may retrieve unnecessary columns",
    "Consider adding partition filter if table is partitioned by date"
  ],
  "applicable_patterns": [
    "column_pruning",
    "partition_filtering"
  ],
  "analyzed_at": "2024-01-15T10:30:00Z"
}
```

---

### POST `/validate`
Validate that optimized query returns identical results to original.

**Request Body:**
```json
{
  "original_query": "SELECT COUNT(*) FROM orders",
  "optimized_query": "SELECT APPROX_COUNT_DISTINCT(order_id) FROM orders",
  "project_id": "your-project-id",
  "sample_size": 1000
}
```

**Response:**
```json
{
  "overall_success": true,
  "summary": "Validation successful: Results identical",
  "results_validation": {
    "identical": true,
    "validation_type": "content_match",
    "original_count": 1500,
    "optimized_count": 1500
  },
  "performance_validation": {
    "performance_improved": true,
    "improvement_percentage": 0.35,
    "original_avg_ms": 2000,
    "optimized_avg_ms": 1300,
    "meets_threshold": true
  }
}
```

---

### POST `/batch`
Optimize multiple queries in batch.

**Request Body:**
```json
{
  "queries": [
    "SELECT * FROM orders",
    "SELECT COUNT(DISTINCT customer_id) FROM orders"
  ],
  "project_id": "your-project-id",
  "validate": true,
  "max_concurrent": 3
}
```

**Response:**
```json
[
  {
    "original_query": "SELECT * FROM orders",
    "optimized_query": "SELECT order_id, customer_id, total_amount FROM orders",
    "optimizations_applied": [...],
    "total_optimizations": 1,
    "results_identical": true
  },
  {
    "original_query": "SELECT COUNT(DISTINCT customer_id) FROM orders",
    "optimized_query": "SELECT APPROX_COUNT_DISTINCT(customer_id) FROM orders",
    "optimizations_applied": [...],
    "total_optimizations": 1,
    "results_identical": true
  }
]
```

---

## Utility Endpoints

### GET `/status`
Get system status and health information.

**Response:**
```json
{
  "status": "healthy",
  "components": {
    "bigquery_connection": "connected",
    "documentation_loaded": true,
    "ai_model_configured": true,
    "available_patterns": 22
  },
  "statistics": {
    "documentation_chunks": 150,
    "available_patterns": 22,
    "bigquery_project": "your-project-id",
    "success_metrics": {
      "functional_accuracy_target": "100%",
      "performance_improvement_target": "30-50%",
      "documentation_coverage": "20+ patterns",
      "test_coverage": "220+ test cases"
    }
  }
}
```

### GET `/suggestions`
Get optimization suggestions without applying them.

**Query Parameters:**
- `query` (string, required): SQL query to analyze
- `project_id` (string, optional): Google Cloud Project ID

**Response:**
```json
{
  "analysis": {...},
  "applicable_patterns": ["column_pruning", "join_reordering"],
  "specific_suggestions": [
    {
      "pattern_name": "Column Pruning",
      "description": "Replace SELECT * with specific column names",
      "expected_improvement": 0.25,
      "specific_advice": "Specify only the columns you need instead of using SELECT *",
      "documentation_reference": "https://cloud.google.com/bigquery/docs/best-practices-performance-input",
      "priority": 85
    }
  ],
  "documentation_references": {...},
  "priority_optimizations": ["column_pruning", "join_reordering"]
}
```

### POST `/upload-queries`
Upload a file containing SQL queries for batch processing.

**Request:** Multipart form data with file upload
**Supported formats:** JSON, TXT

**Response:**
```json
{
  "message": "Successfully parsed 5 queries",
  "queries": ["SELECT ...", "SELECT ..."],
  "total_count": 5
}
```

### POST `/run-tests`
Run the comprehensive test suite.

**Request Body:**
```json
{
  "project_id": "your-project-id",
  "test_type": "sandbox",
  "cleanup": true
}
```

**Response:**
```json
{
  "success": true,
  "test_type": "sandbox",
  "total_tests": 25,
  "passed_tests": 24,
  "failed_tests": 1,
  "execution_time": 45.2,
  "results": [
    {
      "name": "test_column_pruning",
      "status": "PASSED",
      "message": "Column pruning optimization applied successfully"
    }
  ]
}
```

---

## Python API

### Basic Usage

```python
from src.optimizer.query_optimizer import BigQueryOptimizer

# Initialize optimizer
optimizer = BigQueryOptimizer(
    project_id="your-project-id",
    validate_results=True
)

# Optimize a query
result = optimizer.optimize_query(
    query="SELECT * FROM orders WHERE date > '2024-01-01'",
    validate_results=True,
    measure_performance=True,
    sample_size=1000
)

# Check results
if result.results_identical:
    print(f"✅ Optimization successful!")
    print(f"📈 Improvement: {result.estimated_improvement:.1%}")
    print(f"🔧 Optimizations: {result.total_optimizations}")
else:
    print(f"❌ Optimization failed: {result.validation_error}")
```

### Advanced Usage

```python
# Batch optimization
queries = [
    "SELECT * FROM customers",
    "SELECT COUNT(DISTINCT customer_id) FROM orders",
    "SELECT c.name, o.total FROM customers c JOIN orders o ON c.id = o.customer_id"
]

results = optimizer.batch_optimize_queries(
    queries,
    validate_results=True,
    max_concurrent=3
)

for i, result in enumerate(results):
    print(f"Query {i+1}: {result.total_optimizations} optimizations applied")

# Analysis only
analysis = optimizer.analyze_query_only(
    "SELECT customer_id, SUM(amount) FROM orders GROUP BY customer_id"
)

print(f"Complexity: {analysis.complexity}")
print(f"Issues: {analysis.potential_issues}")
print(f"Patterns: {analysis.applicable_patterns}")

# Get suggestions
suggestions = optimizer.get_optimization_suggestions(
    "SELECT COUNT(DISTINCT customer_id) FROM large_table"
)

for suggestion in suggestions["specific_suggestions"]:
    print(f"💡 {suggestion['pattern_name']}: {suggestion['description']}")
```

### Error Handling

```python
from src.common.exceptions import OptimizationError, BigQueryConnectionError

try:
    result = optimizer.optimize_query(your_query)
except BigQueryConnectionError as e:
    print(f"❌ BigQuery connection failed: {e}")
except OptimizationError as e:
    print(f"❌ Optimization failed: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
```

---

## Command Line Interface

### Basic Commands

```bash
# Optimize a query
python -m src.optimizer.main optimize --query "SELECT * FROM table"

# Optimize from file
python -m src.optimizer.main optimize --file query.sql --output optimized.sql

# Analyze query structure
python -m src.optimizer.main analyze --query "SELECT * FROM table"

# Validate optimization
python -m src.optimizer.main validate --original "SELECT COUNT(*)" --optimized "SELECT APPROX_COUNT_DISTINCT(id)"

# Batch optimization
python -m src.optimizer.main batch --queries-file queries.json --output-dir results/

# System status
python -m src.optimizer.main status
```

### Output Formats

```bash
# JSON output
python -m src.optimizer.main optimize --query "SELECT * FROM table" --format json

# Table output
python -m src.optimizer.main optimize --query "SELECT * FROM table" --format table

# Text output (default)
python -m src.optimizer.main optimize --query "SELECT * FROM table" --format text
```

---

## Error Handling

### Common Error Responses

#### 400 Bad Request
```json
{
  "detail": "Invalid SQL syntax: Expected SELECT but found FROM"
}
```

#### 503 Service Unavailable
```json
{
  "detail": "Failed to connect to BigQuery service"
}
```

#### 500 Internal Server Error
```json
{
  "detail": "Optimization failed: AI service temporarily unavailable"
}
```

### Error Categories

1. **Query Errors**: Invalid SQL syntax, unsupported features
2. **Connection Errors**: BigQuery/AI service unavailable
3. **Validation Errors**: Result comparison failures
4. **Configuration Errors**: Missing credentials, invalid project ID
5. **Resource Errors**: Query timeout, memory limits

---

## Rate Limits and Quotas

### BigQuery Limits
- **Query Timeout**: 300 seconds (5 minutes)
- **Result Size**: Limited by BigQuery quotas
- **Concurrent Queries**: Limited by BigQuery slots

### AI Service Limits
- **Gemini API**: Subject to Google AI quotas
- **Request Size**: Max 100KB per request
- **Rate Limiting**: Implemented with exponential backoff

### System Limits
- **Batch Size**: Maximum 50 queries per batch
- **File Upload**: Maximum 10MB
- **Concurrent Requests**: 10 per client

---

## Integration Examples

### Web Application Integration

```javascript
// Frontend JavaScript
async function optimizeQuery(sqlQuery) {
    const response = await fetch('/api/v1/optimize', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            query: sqlQuery,
            project_id: 'your-project-id',
            validate: true
        })
    });
    
    const result = await response.json();
    
    if (result.results_identical) {
        console.log('✅ Optimization successful!');
        console.log('Optimized query:', result.optimized_query);
    } else {
        console.log('❌ Optimization failed:', result.validation_error);
    }
}
```

### Python Application Integration

```python
import requests

def optimize_query_via_api(query: str, project_id: str) -> dict:
    """Optimize query using REST API."""
    
    response = requests.post(
        'http://localhost:8080/api/v1/optimize',
        json={
            'query': query,
            'project_id': project_id,
            'validate': True,
            'measure_performance': True
        }
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API error: {response.status_code} - {response.text}")

# Usage
result = optimize_query_via_api(
    "SELECT * FROM orders WHERE date > '2024-01-01'",
    "your-project-id"
)

print(f"Optimizations applied: {result['total_optimizations']}")
```

### CI/CD Pipeline Integration

```yaml
# GitHub Actions example
- name: Optimize SQL Queries
  run: |
    python -m src.optimizer.main batch \
      --queries-file sql/queries.json \
      --output-dir optimized/ \
      --validate
    
    # Check if any optimizations failed
    if grep -q "validation_error" optimized/batch_results.json; then
      echo "❌ Some query optimizations failed validation"
      exit 1
    fi
```

---

## SDK and Client Libraries

### Python SDK

```python
# Install
pip install bigquery-query-optimizer

# Usage
from bigquery_optimizer import BigQueryOptimizer

optimizer = BigQueryOptimizer(project_id="your-project")
result = optimizer.optimize("SELECT * FROM table")
```

### Node.js Client (Future)

```javascript
// Future implementation
const { BigQueryOptimizer } = require('bigquery-optimizer');

const optimizer = new BigQueryOptimizer({
    projectId: 'your-project-id',
    apiKey: 'your-api-key'
});

const result = await optimizer.optimize('SELECT * FROM table');
```

---

## Monitoring and Observability

### Health Check Endpoint

```bash
curl http://localhost:8080/api/v1/status
```

### Metrics Collection

The API automatically collects:
- **Request Count**: Number of optimization requests
- **Success Rate**: Percentage of successful optimizations
- **Average Improvement**: Mean performance improvement
- **Processing Time**: Time per optimization
- **Error Rates**: Errors by category

### Logging

All API requests are logged with:
- Request timestamp and duration
- Query characteristics (length, complexity)
- Optimization results
- Validation outcomes
- Error details

---

## Security Considerations

### Data Privacy
- **No Query Storage**: Queries are processed in memory only
- **Secure Transmission**: HTTPS recommended for production
- **Credential Management**: Service account keys handled securely

### Access Control
- **IP Whitelisting**: Configure allowed IP ranges
- **API Authentication**: Implement for production use
- **Rate Limiting**: Prevent abuse and resource exhaustion

### Audit Trail
- **Request Logging**: All optimization requests logged
- **Result Tracking**: Optimization outcomes recorded
- **Error Monitoring**: Failed requests and errors tracked

---

## Performance Optimization

### Caching Strategy
- **Documentation Cache**: 24-hour TTL
- **Query Analysis Cache**: 1-hour TTL for repeated queries
- **Connection Pooling**: Reuse BigQuery connections

### Async Processing
- **Non-blocking Operations**: Long-running optimizations don't block API
- **Background Tasks**: Batch processing in background
- **Progress Tracking**: Monitor long-running operations

### Resource Management
- **Memory Limits**: Prevent memory exhaustion
- **Query Timeouts**: Prevent hanging requests
- **Concurrent Limits**: Control resource usage

This API documentation provides comprehensive guidance for integrating the BigQuery Query Optimizer into your applications and workflows.