# BigQuery Query Optimizer REST API

This document describes the REST API and Web UI for the BigQuery Query Optimizer.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements-api.txt
   ```

2. **Set up environment variables:**
   ```bash
   export GOOGLE_CLOUD_PROJECT=your-project-id
   export GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
   export GEMINI_API_KEY=your-gemini-api-key
   ```

3. **Start the server:**
   ```bash
   python run_api_server.py
   ```

4. **Access the application:**
   - Web UI: http://localhost:8080
   - API Documentation: http://localhost:8080/docs
   - Interactive API: http://localhost:8080/redoc

## API Endpoints

### POST /api/v1/optimize
Optimize a BigQuery SQL query with AI-powered improvements.

**Request Body:**
```json
{
  "query": "SELECT * FROM orders WHERE date > '2024-01-01'",
  "project_id": "your-project-id",
  "validate": true,
  "measure_performance": false,
  "sample_size": 1000
}
```

**Response:**
```json
{
  "original_query": "SELECT * FROM orders WHERE date > '2024-01-01'",
  "optimized_query": "SELECT order_id, customer_id, total FROM orders WHERE _PARTITIONDATE >= '2024-01-01' AND date > '2024-01-01'",
  "optimizations_applied": [
    {
      "pattern_name": "Column Pruning",
      "description": "Replaced SELECT * with specific columns",
      "expected_improvement": 0.2
    }
  ],
  "total_optimizations": 2,
  "estimated_improvement": 0.6,
  "results_identical": true
}
```

### POST /api/v1/analyze
Analyze a SQL query without optimizing it.

**Request Body:**
```json
{
  "query": "SELECT * FROM orders WHERE date > '2024-01-01'",
  "project_id": "your-project-id"
}
```

**Response:**
```json
{
  "complexity": "moderate",
  "table_count": 1,
  "join_count": 0,
  "potential_issues": ["Using SELECT *", "Missing partition filter"],
  "applicable_patterns": ["column_pruning", "partition_filtering"]
}
```

### POST /api/v1/validate
Validate that optimized query returns identical results.

**Request Body:**
```json
{
  "original_query": "SELECT COUNT(*) FROM orders",
  "optimized_query": "SELECT APPROX_COUNT_DISTINCT(order_id) FROM orders",
  "project_id": "your-project-id",
  "sample_size": 1000
}
```

### POST /api/v1/batch
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

### GET /api/v1/suggestions
Get optimization suggestions without applying them.

**Query Parameters:**
- `query`: SQL query to analyze
- `project_id`: (optional) Google Cloud Project ID

### GET /api/v1/table-suggestions
Get table-level optimization suggestions.

**Query Parameters:**
- `table_id`: BigQuery table ID (project.dataset.table)
- `project_id`: (optional) Google Cloud Project ID
- `sample_queries`: (optional) Array of sample queries

### GET /api/v1/status
Get system status and health information.

**Response:**
```json
{
  "status": "healthy",
  "components": {
    "bigquery_connection": "connected",
    "documentation_loaded": true,
    "ai_model_configured": true,
    "available_patterns": 9
  },
  "statistics": {
    "documentation_chunks": 150,
    "available_patterns": 9,
    "bigquery_project": "your-project-id"
  }
}
```

### POST /api/v1/upload-queries
Upload a file containing SQL queries for batch processing.

**Request:** Multipart form data with file upload
**Supported formats:** JSON, TXT

## Web UI Features

The web interface provides:

1. **Query Input**: Large text area for SQL queries with syntax highlighting
2. **Configuration Options**: 
   - Project ID
   - Sample size for validation
   - Validation and performance measurement toggles
3. **Action Buttons**:
   - Optimize Query: Full optimization with results
   - Analyze Only: Query analysis without optimization
   - Get Suggestions: Optimization suggestions without applying them
4. **Results Display**:
   - Optimization results with before/after comparisons
   - Query analysis with complexity metrics
   - Optimization suggestions with documentation links
5. **System Status**: Modal showing system health and configuration
6. **Sample Queries**: Load example queries for testing

## Development

### Running in Development Mode
```bash
python run_api_server.py --reload --debug
```

### API Documentation
- Swagger UI: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc

### Adding New Endpoints
1. Add route function to `src/api/routes.py`
2. Define request/response models using Pydantic
3. Add error handling and logging
4. Update this documentation

### Customizing the UI
- HTML template: `src/api/templates/index.html`
- Static files: `src/api/static/`
- The UI uses Tailwind CSS and Prism.js for syntax highlighting

## Error Handling

All endpoints return appropriate HTTP status codes:
- 200: Success
- 400: Bad Request (invalid input)
- 503: Service Unavailable (connection issues)
- 500: Internal Server Error

Error responses include detailed error messages:
```json
{
  "detail": "Optimization failed: Invalid SQL syntax"
}
```

## Security Considerations

- The API accepts any origin for CORS (development setup)
- No authentication is implemented (add as needed)
- File uploads are limited to JSON/TXT files
- Batch operations are limited to 50 queries maximum

## Performance

- Batch operations run with configurable concurrency
- Large queries are handled with streaming where possible
- Results are not cached (add caching as needed)
- File uploads are processed in memory (consider disk storage for large files)

## Deployment

For production deployment:

1. **Use a production WSGI server:**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.api.server:create_app
   ```

2. **Set environment variables:**
   - `GOOGLE_CLOUD_PROJECT`
   - `GOOGLE_APPLICATION_CREDENTIALS`
   - `GEMINI_API_KEY`

3. **Configure reverse proxy** (nginx, Apache, etc.)

4. **Add authentication and rate limiting** as needed

5. **Set up monitoring and logging**