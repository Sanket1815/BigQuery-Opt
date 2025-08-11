"""API routes for BigQuery Query Optimizer."""

import json
from pathlib import Path
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, BackgroundTasks, UploadFile, File
from pydantic import BaseModel, Field

from src.optimizer.query_optimizer import BigQueryOptimizer
from src.common.exceptions import OptimizationError, BigQueryConnectionError
from src.common.logger import QueryOptimizerLogger
from src.common.models import OptimizationResult, QueryAnalysis
import os
import time
import subprocess
import json
from pathlib import Path

router = APIRouter()
logger = QueryOptimizerLogger(__name__)


# Request/Response Models
class OptimizeRequest(BaseModel):
    """Request model for query optimization."""
    query: str = Field(..., description="SQL query to optimize")
    project_id: Optional[str] = Field(None, description="Google Cloud Project ID")
    validate_results: bool = Field(True, description="Validate query results")
    measure_performance: bool = Field(False, description="Measure actual performance")
    sample_size: int = Field(1000, description="Sample size for validation")


class AnalyzeRequest(BaseModel):
    """Request model for query analysis."""
    query: str = Field(..., description="SQL query to analyze")
    project_id: Optional[str] = Field(None, description="Google Cloud Project ID")


class ValidateRequest(BaseModel):
    """Request model for query validation."""
    original_query: str = Field(..., description="Original SQL query")
    optimized_query: str = Field(..., description="Optimized SQL query")
    project_id: Optional[str] = Field(None, description="Google Cloud Project ID")
    sample_size: int = Field(1000, description="Sample size for validation")


class BatchOptimizeRequest(BaseModel):
    """Request model for batch optimization."""
    queries: List[str] = Field(..., description="List of SQL queries to optimize")
    project_id: Optional[str] = Field(None, description="Google Cloud Project ID")
    validate_results: bool = Field(True, description="Validate query results")
    max_concurrent: int = Field(3, description="Maximum concurrent optimizations")


class StatusResponse(BaseModel):
    """Response model for system status."""
    status: str
    components: Dict[str, Any]
    statistics: Dict[str, Any]


class TestSuiteRequest(BaseModel):
    """Request model for running test suite."""
    project_id: Optional[str] = Field(None, description="Google Cloud Project ID")
    test_type: str = Field("sandbox", description="Type of tests to run")
    cleanup: bool = Field(True, description="Clean up test data after tests")


class TestSuiteSelectionRequest(BaseModel):
    """Request model for selecting and running specific test suite."""
    test_suite: str = Field(..., description="Test suite to run")
    project_id: Optional[str] = Field(None, description="Google Cloud Project ID")
    validate_results: bool = Field(True, description="Validate query results")
    measure_performance: bool = Field(False, description="Measure actual performance")


class TestCaseResult(BaseModel):
    """Result of a single test case."""
    name: str
    description: str
    original_query: str
    original_results: Optional[List[Dict[str, Any]]] = None
    optimization_result: OptimizationResult
    optimized_results: Optional[List[Dict[str, Any]]] = None
    execution_time: float


class TestSuiteResult(BaseModel):
    """Result of running a test suite."""
    suite_name: str
    description: str
    execution_time: float
    test_cases: List[TestCaseResult]


class TestResult(BaseModel):
    """Response model for test results."""
    success: bool
    test_type: str
    total_tests: int
    passed_tests: int
    failed_tests: int
    execution_time: float
    results: List[Dict[str, Any]]
    error_message: Optional[str] = None


# API Endpoints
@router.post("/optimize", response_model=OptimizationResult)
async def optimize_query(request: OptimizeRequest):
    """
    Optimize a BigQuery SQL query.
    
    This endpoint analyzes the provided SQL query and applies AI-powered optimizations
    to improve performance while maintaining identical results.
    """
    try:
        logger.logger.info(f"Optimizing query of length {len(request.query)}")
        
        optimizer = BigQueryOptimizer(
            project_id=request.project_id,
            validate_results=request.validate_results
        )
        
        # Test connection first
        if not optimizer.test_connection():
            raise HTTPException(
                status_code=503, 
                detail="Failed to connect to required services"
            )
        
        result = optimizer.optimize_query(
            request.query,
            validate_results=request.validate_results,
            measure_performance=request.measure_performance,
            sample_size=request.sample_size
        )
        
        logger.logger.info(
            f"Optimization completed: {result.total_optimizations} optimizations applied"
        )
        
        return result
        
    except OptimizationError as e:
        logger.log_error(e, {"endpoint": "/optimize"})
        raise HTTPException(status_code=400, detail=str(e))
    except BigQueryConnectionError as e:
        logger.log_error(e, {"endpoint": "/optimize"})
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.log_error(e, {"endpoint": "/optimize"})
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/analyze", response_model=QueryAnalysis)
async def analyze_query(request: AnalyzeRequest):
    """
    Analyze a SQL query without optimizing it.
    
    This endpoint provides detailed analysis of query structure, complexity,
    and potential optimization opportunities.
    """
    try:
        logger.logger.info(f"Analyzing query of length {len(request.query)}")
        
        optimizer = BigQueryOptimizer(
            project_id=request.project_id,
            validate_results=False
        )
        
        analysis = optimizer.analyze_query_only(request.query)
        
        logger.logger.info(f"Analysis completed: {analysis.complexity} complexity")
        return analysis
        
    except OptimizationError as e:
        logger.log_error(e, {"endpoint": "/analyze"})
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.log_error(e, {"endpoint": "/analyze"})
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/validate")
async def validate_queries(request: ValidateRequest):
    """
    Validate that optimized query returns identical results to original.
    
    This endpoint compares the results of two queries to ensure they return
    identical data, which is crucial for optimization validation.
    """
    try:
        logger.logger.info("Validating query optimization")
        
        optimizer = BigQueryOptimizer(
            project_id=request.project_id,
            validate_results=True
        )
        
        validation_result = optimizer.validate_optimization(
            request.original_query,
            request.optimized_query,
            request.sample_size
        )
        
        logger.logger.info(f"Validation completed: {validation_result['overall_success']}")
        return validation_result
        
    except OptimizationError as e:
        logger.log_error(e, {"endpoint": "/validate"})
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.log_error(e, {"endpoint": "/validate"})
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/batch", response_model=List[OptimizationResult])
async def batch_optimize(request: BatchOptimizeRequest, background_tasks: BackgroundTasks):
    """
    Optimize multiple queries in batch.
    
    This endpoint processes multiple SQL queries concurrently for optimization,
    useful for bulk optimization tasks.
    """
    try:
        logger.logger.info(f"Starting batch optimization of {len(request.queries)} queries")
        
        if len(request.queries) > 50:  # Reasonable limit
            raise HTTPException(
                status_code=400, 
                detail="Too many queries. Maximum 50 queries per batch."
            )
        
        optimizer = BigQueryOptimizer(
            project_id=request.project_id,
            validate_results=request.validate_results
        )
        
        results = optimizer.batch_optimize_queries(
            request.queries,
            validate_results=request.validate_results,
            max_concurrent=request.max_concurrent
        )
        
        successful = sum(1 for r in results if not r.validation_error)
        logger.logger.info(f"Batch optimization completed: {successful}/{len(results)} successful")
        
        return results
        
    except OptimizationError as e:
        logger.log_error(e, {"endpoint": "/batch"})
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.log_error(e, {"endpoint": "/batch"})
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/status", response_model=StatusResponse)
async def get_status():
    """
    Get system status and configuration.
    
    This endpoint provides information about the system's health,
    configuration, and available optimization capabilities.
    """
    try:
        optimizer = BigQueryOptimizer(validate_results=False)
        
        # Test connections
        connection_ok = optimizer.test_connection()
        
        # Get statistics
        stats = optimizer.get_optimization_statistics()
        
        components = {
            "bigquery_connection": "connected" if connection_ok else "failed",
            "documentation_loaded": stats.get("documentation_chunks", 0) > 0,
            "ai_model_configured": "gemini_api_key" in str(stats),
            "available_patterns": stats.get("available_patterns", 0)
        }
        
        status = "healthy" if all([
            connection_ok,
            components["documentation_loaded"],
            components["available_patterns"] > 0
        ]) else "degraded"
        
        return StatusResponse(
            status=status,
            components=components,
            statistics=stats
        )
        
    except Exception as e:
        logger.log_error(e, {"endpoint": "/status"})
        return StatusResponse(
            status="error",
            components={"error": str(e)},
            statistics={}
        )


@router.post("/upload-queries")
async def upload_queries_file(file: UploadFile = File(...)):
    """
    Upload a file containing SQL queries for batch processing.
    
    Accepts JSON files with queries in the format:
    {"queries": ["SELECT ...", "SELECT ..."]}
    or
    ["SELECT ...", "SELECT ..."]
    """
    try:
        if not file.filename.endswith(('.json', '.txt')):
            raise HTTPException(
                status_code=400,
                detail="Only JSON and TXT files are supported"
            )
        
        content = await file.read()
        
        if file.filename.endswith('.json'):
            data = json.loads(content.decode('utf-8'))
            
            if isinstance(data, list):
                queries = data
            elif isinstance(data, dict) and 'queries' in data:
                queries = data['queries']
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid JSON format. Expected array of queries or object with 'queries' key"
                )
        else:  # .txt file
            queries = [q.strip() for q in content.decode('utf-8').split('\n') if q.strip()]
        
        return {
            "message": f"Successfully parsed {len(queries)} queries",
            "queries": queries[:5],  # Return first 5 as preview
            "total_count": len(queries)
        }
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON file")
    except Exception as e:
        logger.log_error(e, {"endpoint": "/upload-queries"})
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@router.get("/suggestions")
async def get_optimization_suggestions(
    query: str,
    project_id: Optional[str] = None
):
    """
    Get optimization suggestions for a query without applying them.
    
    This endpoint provides detailed suggestions and documentation references
    for potential optimizations without actually modifying the query.
    """
    try:
        optimizer = BigQueryOptimizer(
            project_id=project_id,
            validate_results=False
        )
        
        suggestions = optimizer.get_optimization_suggestions(query)
        return suggestions
        
    except OptimizationError as e:
        logger.log_error(e, {"endpoint": "/suggestions"})
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.log_error(e, {"endpoint": "/suggestions"})
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/table-suggestions")
async def get_table_suggestions(
    table_id: str,
    project_id: Optional[str] = None,
    sample_queries: Optional[List[str]] = None
):
    """
    Get table-level optimization suggestions.
    
    This endpoint analyzes table structure and usage patterns to suggest
    optimizations like partitioning, clustering, and schema improvements.
    """
    try:
        optimizer = BigQueryOptimizer(
            project_id=project_id,
            validate_results=False
        )
        
        suggestions = optimizer.get_table_optimization_suggestions(
            table_id,
            sample_queries
        )
        
        return {
            "table_id": table_id,
            "suggestions": suggestions,
            "total_suggestions": len(suggestions)
        }
        
    except OptimizationError as e:
        logger.log_error(e, {"endpoint": "/table-suggestions"})
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.log_error(e, {"endpoint": "/table-suggestions"})
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
@router.post("/run-test-suite", response_model=TestSuiteResult)
async def run_test_suite(request: TestSuiteSelectionRequest):
    """
    Run a specific test suite with 3 test cases each.
    
    Available test suites:
    - simple_query: Basic SELECT with inefficient WHERE clause
    - complex_join: Multi-table JOIN with suboptimal ordering  
    - aggregation: GROUP BY without proper partitioning
    - window_function: Inefficient window specifications
    - nested_query: Deeply nested subqueries that can be flattened
    """
    try:
        logger.logger.info(f"Running test suite: {request.test_suite}")
        
        # Define test suites with 3 test cases each
        test_suites = {
            "simple_query": {
                "name": "Simple Query Test",
                "description": "Basic SELECT queries with inefficient WHERE clauses that need column pruning and filtering optimization",
                "test_cases": [
                    {
                        "name": "SELECT * with Date Filter",
                        "description": "Basic SELECT * query that needs column pruning optimization",
                        "query": f"""SELECT *
FROM `{request.project_id or 'your-project'}.optimizer_test_dataset.orders`
WHERE order_date >= '2024-06-01'
AND status = 'completed'
ORDER BY total_amount DESC
LIMIT 100"""
                    },
                    {
                        "name": "SELECT * with Multiple Filters",
                        "description": "SELECT * with multiple WHERE conditions needing optimization",
                        "query": f"""SELECT *
FROM `{request.project_id or 'your-project'}.optimizer_test_dataset.customers`
WHERE customer_tier = 'Premium'
AND region IN ('US-East', 'US-West')
AND signup_date >= '2020-01-01'"""
                    },
                    {
                        "name": "SELECT * with Aggregation",
                        "description": "SELECT * in subquery with aggregation that needs column pruning",
                        "query": f"""SELECT customer_tier, COUNT(*) as customer_count
FROM (
    SELECT * FROM `{request.project_id or 'your-project'}.optimizer_test_dataset.customers`
    WHERE region = 'US-East'
) 
GROUP BY customer_tier"""
                    }
                ]
            },
            "complex_join": {
                "name": "Complex JOIN Test", 
                "description": "Multi-table JOIN queries with suboptimal ordering that need JOIN reordering and optimization",
                "test_cases": [
                    {
                        "name": "4-Table JOIN with Large Table First",
                        "description": "Complex JOIN starting with largest table - needs reordering",
                        "query": f"""SELECT 
    c.customer_name,
    o.order_id,
    o.total_amount,
    p.product_name,
    oi.quantity
FROM `gen-lang-client-0064110488.optimizer_test_dataset.order_items` oi
JOIN `gen-lang-client-0064110488.optimizer_test_dataset.orders` o 
    ON oi.order_id = o.order_id
JOIN `gen-lang-client-0064110488.optimizer_test_dataset.customers` c 
    ON o.customer_id = c.customer_id
JOIN `gen-lang-client-0064110488.optimizer_test_dataset.products` p 
    ON oi.product_id = p.product_id
WHERE o.order_date >= '2024-01-01'
  AND p.category IS NOT NULL
ORDER BY o.total_amount DESC
LIMIT 100;
"""
                    },
                    {
                        "name": "LEFT JOIN with SELECT *",
                        "description": "LEFT JOIN query with SELECT * needing both JOIN and column optimization",
                        "query": f"""SELECT *
FROM `gen-lang-client-0064110488.optimizer_test_dataset.customers` c
LEFT JOIN `gen-lang-client-0064110488.optimizer_test_dataset.orders` o
    ON c.customer_id = o.customer_id
LEFT JOIN `gen-lang-client-0064110488.optimizer_test_dataset.products` p
    ON o.product_id = p.product_id
WHERE c.region = 'Europe'
LIMIT 100;
"""
                    },
                    {
                        "name": "Cross JOIN Pattern",
                        "description": "Implicit cross join that needs conversion to proper JOIN",
                        "query": f"""SELECT c.customer_name, p.product_name
FROM `gen-lang-client-0064110488.optimizer_test_dataset.customers` c,
     `gen-lang-client-0064110488.optimizer_test_dataset.products` p
WHERE c.customer_tier = 'Gold'
AND p.category = 'Electronics'
LIMIT 50"""
                    }
                ]
            },
            "aggregation": {
                "name": "Aggregation Test",
                "description": "GROUP BY queries without proper optimization that need approximate aggregation and better filtering",
                "test_cases": [
                    {
                        "name": "COUNT DISTINCT without Optimization",
                        "description": "COUNT DISTINCT that should use approximate aggregation",
                        "query": f"""SELECT 
    c.region,
    COUNT(*) as total_orders,
    COUNT(DISTINCT o.customer_id) as unique_customers,
    SUM(o.total_amount) as total_revenue,
    AVG(o.total_amount) as avg_order_value
FROM `gen-lang-client-0064110488.optimizer_test_dataset.orders` o
JOIN `gen-lang-client-0064110488.optimizer_test_dataset.customers` c 
    ON o.customer_id = c.customer_id
WHERE o.order_date >= '2024-01-01'
GROUP BY c.region
ORDER BY total_revenue DESC"""
                    },
                    {
                        "name": "Multiple COUNT DISTINCT",
                        "description": "Query with multiple COUNT DISTINCT operations needing optimization",
                        "query": f"""SELECT
  c.category,
  (SELECT COUNT(DISTINCT oi.order_id)
   FROM `gen-lang-client-0064110488.optimizer_test_dataset.order_items` oi
   JOIN `gen-lang-client-0064110488.optimizer_test_dataset.orders` o ON oi.order_id = o.order_id
   JOIN `gen-lang-client-0064110488.optimizer_test_dataset.products` p2 ON oi.product_id = p2.product_id
   WHERE CAST(o.order_date AS STRING) >= '2024-01-01' AND p2.category = c.category) AS unique_orders,
  (SELECT COUNT(DISTINCT o.customer_id)
   FROM `gen-lang-client-0064110488.optimizer_test_dataset.order_items` oi
   JOIN `gen-lang-client-0064110488.optimizer_test_dataset.orders` o ON oi.order_id = o.order_id
   JOIN `gen-lang-client-0064110488.optimizer_test_dataset.products` p2 ON oi.product_id = p2.product_id
   WHERE CAST(o.order_date AS STRING) >= '2024-01-01' AND p2.category = c.category) AS unique_customers,
  (SELECT COUNT(DISTINCT oi.product_id)
   FROM `gen-lang-client-0064110488.optimizer_test_dataset.order_items` oi
   JOIN `gen-lang-client-0064110488.optimizer_test_dataset.orders` o ON oi.order_id = o.order_id
   JOIN `gen-lang-client-0064110488.optimizer_test_dataset.products` p2 ON oi.product_id = p2.product_id
   WHERE CAST(o.order_date AS STRING) >= '2024-01-01' AND p2.category = c.category) AS unique_products
FROM (
  SELECT DISTINCT category
  FROM `gen-lang-client-0064110488.optimizer_test_dataset.products`
) c
ORDER BY c.category;
"""
                    },
                    {
                        "name": "Heavy Aggregation with SELECT *",
                        "description": "Complex aggregation with SELECT * needing multiple optimizations",
                        "query": f"""SELECT
  (ANY_VALUE(t)).*,
  COUNT(DISTINCT t.customer_id) AS unique_customers
FROM (
  SELECT o.*
  FROM `gen-lang-client-0064110488.optimizer_test_dataset.orders` o
  WHERE SUBSTR(CAST(o.order_date AS STRING), 1, 10) >= '2024-01-01'
    AND (LOWER(o.status) LIKE 'completed%' OR o.status = 'completed')
) AS t
CROSS JOIN UNNEST(GENERATE_ARRAY(1, 5)) AS blowup   -- pointless row duplication
GROUP BY FORMAT_DATE('%Y-%m-%d', DATE(t.order_date))
ORDER BY RAND();
"""
                    }
                ]
            },
            "window_function": {
                "name": "Window Function Test",
                "description": "Window function queries with inefficient specifications that need partitioning and optimization",
                "test_cases": [
                    {
                        "name": "ROW_NUMBER without PARTITION",
                        "description": "ROW_NUMBER without PARTITION BY clause - needs optimization",
                        "query": f"""SELECT 
    customer_id,
    order_id,
    order_date,
    total_amount,
    ROW_NUMBER() OVER (ORDER BY total_amount DESC) as overall_rank,
    RANK() OVER (ORDER BY order_date) as date_rank
FROM `gen-lang-client-0064110488.optimizer_test_dataset.orders`
WHERE order_date >= '2024-06-01'
ORDER BY total_amount DESC
LIMIT 1000"""
                    },
                    {
                        "name": "Multiple Window Functions",
                        "description": "Multiple window functions that can be optimized with better partitioning",
                        "query": f"""SELECT 
    customer_id,
    order_date,
    total_amount,
    LAG(total_amount) OVER (ORDER BY order_date) as prev_amount,
    LEAD(total_amount) OVER (ORDER BY order_date) as next_amount,
    SUM(total_amount) OVER (ORDER BY order_date ROWS UNBOUNDED PRECEDING) as running_total
FROM `gen-lang-client-0064110488.optimizer_test_dataset.orders`
WHERE customer_id <= 100"""
                    },
                    {
                        "name": "Window Function with SELECT *",
                        "description": "Window function query with SELECT * needing both optimizations",
                        "query": f"""SELECT *,
    NTILE(4) OVER (ORDER BY total_amount) as quartile,
    PERCENT_RANK() OVER (ORDER BY order_date) as date_percentile
FROM `gen-lang-client-0064110488.optimizer_test_dataset.orders`
WHERE order_date >= '2024-01-01'
LIMIT 500"""
                    }
                ]
            },
            "nested_query": {
                "name": "Nested Query Test",
                "description": "Deeply nested subqueries that can be flattened into JOINs for better performance",
                "test_cases": [
                    {
                        "name": "Triple Nested IN Subqueries",
                        "description": "Deeply nested IN subqueries that should be converted to JOINs",
                        "query": f"""SELECT DISTINCT c.customer_name
FROM `gen-lang-client-0064110488.optimizer_test_dataset.customers` c
WHERE CAST(c.customer_id AS STRING) NOT IN (
  SELECT CAST(o1.customer_id AS STRING)
  FROM `gen-lang-client-0064110488.optimizer_test_dataset.orders` o1
  WHERE CAST(o1.order_id AS STRING) IN (
    SELECT CAST(oi.order_id AS STRING)
    FROM `gen-lang-client-0064110488.optimizer_test_dataset.order_items` oi
    WHERE oi.product_id IN (
      SELECT p.product_id
      FROM `gen-lang-client-0064110488.optimizer_test_dataset.products` p
      WHERE LOWER(p.category) LIKE '%electronic%'
    )
  )
);"""
                    },
                    {
                        "name": "EXISTS with Nested Subquery",
                        "description": "EXISTS subquery with nested conditions that can be flattened",
                        "query": f"""SELECT *
FROM `gen-lang-client-0064110488.optimizer_test_dataset.customers` c
WHERE EXISTS (
  SELECT 1
  FROM `gen-lang-client-0064110488.optimizer_test_dataset.orders` o
  WHERE CAST(o.customer_id AS STRING) = CAST(c.customer_id AS STRING)
    AND SUBSTR(CAST(o.order_date AS STRING),1,10) >= '2024-01-01'
    AND EXISTS (
      SELECT 1 FROM `gen-lang-client-0064110488.optimizer_test_dataset.order_items` oi
      WHERE oi.order_id = o.order_id AND CAST(oi.quantity AS STRING) > '3'
    )
);
"""
                    },
                    {
                        "name": "Correlated Subquery in SELECT",
                        "description": "Correlated subquery in SELECT clause that can be optimized",
                        "query": f"""SELECT 
    customer_id,
    customer_name,
    (SELECT COUNT(*) 
     FROM `gen-lang-client-0064110488.optimizer_test_dataset.orders` o 
     WHERE o.customer_id = c.customer_id 
     AND o.status = 'completed') as completed_orders,
    (SELECT SUM(total_amount) 
     FROM `gen-lang-client-0064110488.optimizer_test_dataset.orders` o2 
     WHERE o2.customer_id = c.customer_id 
     AND o2.order_date >= '2024-01-01') as total_spent_2024
FROM `gen-lang-client-0064110488.optimizer_test_dataset.customers` c
WHERE c.customer_tier IN ('Premium', 'Gold')"""
                    }
                ]
            }
        }
        
        if request.test_suite not in test_suites:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown test suite: {request.test_suite}. Available: {list(test_suites.keys())}"
            )
        
        suite_config = test_suites[request.test_suite]
        start_time = time.time()
        
        # Initialize optimizer
        optimizer = BigQueryOptimizer(
            project_id=request.project_id,
            validate_results=request.validate_results
        )
        
        # Test connection
        if not optimizer.test_connection():
            raise HTTPException(
                status_code=503,
                detail="Failed to connect to BigQuery service"
            )
        
        # Run test cases
        test_results = []
        
        for test_case in suite_config["test_cases"]:
            case_start_time = time.time()
            
            try:
                # Fix project ID in test case query
                actual_project_id = request.project_id or optimizer.bq_client.project_id
                test_query = test_case["query"]
                if 'your-project' in test_query:
                    test_query = test_query.replace('your-project', actual_project_id)
                
                # Run optimization on the test query
                optimization_result = optimizer.optimize_query(
                    test_query,
                    validate_results=request.validate_results,
                    measure_performance=request.measure_performance,
                    sample_size=100  # Use smaller sample for tests
                )
                
                # Execute original query to get results
                original_results = None
                optimized_results = None
                
                try:
                    # Fix project ID in test query before execution
                    actual_project_id = request.project_id or optimizer.bq_client.project_id
                    test_query = test_case["query"]
                    if 'your-project' in test_query:
                        test_query = test_query.replace('your-project', actual_project_id)
                    
                    # Get original query results
                    original_exec = optimizer.bq_client.execute_query(test_query, dry_run=False)
                    if original_exec["success"]:
                        original_results = original_exec["results"][:5]  # First 5 rows
                    
                    # Get optimized query results
                    optimized_query_fixed = optimization_result.optimized_query
                    if 'your-project' in optimized_query_fixed:
                        optimized_query_fixed = optimized_query_fixed.replace('your-project', actual_project_id)
                    
                    optimized_exec = optimizer.bq_client.execute_query(optimized_query_fixed, dry_run=False)
                    if optimized_exec["success"]:
                        optimized_results = optimized_exec["results"][:5]  # First 5 rows
                        
                except Exception as e:
                    print(f"Warning: Could not execute queries for result comparison: {e}")
                
                case_execution_time = time.time() - case_start_time
                
                test_results.append(TestCaseResult(
                    name=test_case["name"],
                    description=test_case["description"],
                    original_query=test_query,
                    original_results=original_results,
                    optimization_result=optimization_result,
                    optimized_results=optimized_results,
                    execution_time=case_execution_time
                ))
                
                logger.logger.info(f"Test case completed: {test_case['name']}")
                
            except Exception as e:
                case_execution_time = time.time() - case_start_time
                
                # Create a minimal optimization result for failed cases
                failed_result = OptimizationResult(
                    original_query=test_case["query"],
                    query_analysis=QueryAnalysis(
                        original_query=test_case["query"],
                        query_hash="failed",
                        complexity="unknown",
                        table_count=0,
                        join_count=0,
                        subquery_count=0,
                        window_function_count=0,
                        aggregate_function_count=0,
                        potential_issues=[],
                        applicable_patterns=[]
                    ),
                    optimized_query=test_case["query"],
                    optimizations_applied=[],
                    total_optimizations=0,
                    validation_error=str(e)
                )
                
                test_results.append(TestCaseResult(
                    name=test_case["name"],
                    description=test_case["description"],
                    original_query=test_case["query"],
                    original_results=None,
                    optimization_result=failed_result,
                    optimized_results=None,
                    execution_time=case_execution_time
                ))
                
                logger.log_error(e, {"test_case": test_case["name"], "test_suite": request.test_suite})
        
        total_execution_time = time.time() - start_time
        
        logger.logger.info(f"Test suite completed: {request.test_suite}")
        
        return TestSuiteResult(
            suite_name=suite_config["name"],
            description=suite_config["description"],
            execution_time=total_execution_time,
            test_cases=test_results
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.log_error(e, {"endpoint": "/run-test-suite", "test_suite": request.test_suite})
        raise HTTPException(
            status_code=500,
            detail=f"Test suite execution failed: {str(e)}"
        )


@router.post("/run-tests", response_model=TestResult)
async def run_test_suite(request: TestSuiteRequest):
    """
    Run the BigQuery optimizer test suite.
    
    This endpoint runs the comprehensive test suite including:
    - Simple Query Test
    - Complex JOIN Test  
    - Aggregation Test
    - Window Function Test
    - Nested Query Test
    """
    try:
        logger.logger.info(f"Running {request.test_type} test suite")
        
        # Set project ID if provided
        env = os.environ.copy()
        if request.project_id:
            env["GOOGLE_CLOUD_PROJECT"] = request.project_id
        
        # Prepare test command
        test_script = Path(__file__).parent.parent.parent / "tests" / "test_runner.py"
        cmd = [
            "python", str(test_script),
            "--type", request.test_type,
            "--verbose"
        ]
        
        if request.cleanup:
            cmd.append("--cleanup")
        
        # Run tests
        import time
        start_time = time.time()
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            env=env,
            timeout=1800  # 30 minutes timeout
        )
        
        execution_time = time.time() - start_time
        
        # Parse test results from output
        output_lines = result.stdout.split('\n')
        test_results = []
        total_tests = 0
        passed_tests = 0
        failed_tests = 0
        
        # Simple parsing of pytest output
        for line in output_lines:
            if "PASSED" in line:
                passed_tests += 1
                total_tests += 1
                test_results.append({
                    "name": line.split("::")[1] if "::" in line else line,
                    "status": "PASSED",
                    "message": ""
                })
            elif "FAILED" in line:
                failed_tests += 1
                total_tests += 1
                test_results.append({
                    "name": line.split("::")[1] if "::" in line else line,
                    "status": "FAILED", 
                    "message": line
                })
            elif "✅" in line:
                test_results.append({
                    "name": line.split(":")[0].replace("✅", "").strip(),
                    "status": "SUCCESS",
                    "message": line
                })
        
        success = result.returncode == 0
        
        logger.logger.info(
            f"Test suite completed: {passed_tests}/{total_tests} passed"
        )
        
        return TestResult(
            success=success,
            test_type=request.test_type,
            total_tests=total_tests,
            passed_tests=passed_tests,
            failed_tests=failed_tests,
            execution_time=execution_time,
            results=test_results,
            error_message=result.stderr if not success else None
        )
        
    except subprocess.TimeoutExpired:
        logger.log_error(Exception("Test timeout"), {"endpoint": "/run-tests"})
        return TestResult(
            success=False,
            test_type=request.test_type,
            total_tests=0,
            passed_tests=0,
            failed_tests=0,
            execution_time=1800,
            results=[],
            error_message="Test suite timed out after 30 minutes"
        )
    except Exception as e:
        logger.log_error(e, {"endpoint": "/run-tests"})
        return TestResult(
            success=False,
            test_type=request.test_type,
            total_tests=0,
            passed_tests=0,
            failed_tests=0,
            execution_time=0,
            results=[],
            error_message=str(e)
        )


@router.get("/test-queries")
async def get_test_queries():
    """
    Get predefined test queries for each test category.
    
    Returns sample inefficient queries that can be used for testing
    the optimization functionality.
    """
    try:
        from config.settings import get_settings
        settings = get_settings()
        project_id = settings.google_cloud_project or "gen-lang-client-0064110488"
        dataset_id = "optimizer_test_dataset"
        
        test_queries = {
            "simple_query": {
                "name": "Simple Query Test",
                "description": "Basic SELECT with inefficient WHERE clause",
                "inefficient_query": f"""SELECT *
FROM `{project_id}.{dataset_id}.orders`
WHERE order_date >= '2024-06-01'
AND status = 'completed'
ORDER BY total_amount DESC
LIMIT 100""",
                "expected_optimizations": ["Column Pruning", "Partition Filtering"],
                "expected_improvement": "30-50%"
            },
            "complex_join": {
                "name": "Complex JOIN Test", 
                "description": "Multi-table JOIN with suboptimal ordering",
                "inefficient_query": f"""SELECT 
    c.customer_name,
    o.order_id,
    o.total_amount,
    p.product_name,
    oi.quantity
FROM `{project_id}.{dataset_id}.order_items` oi
JOIN `{project_id}.{dataset_id}.orders` o 
    ON oi.order_id = o.order_id
JOIN `{project_id}.{dataset_id}.customers` c 
    ON o.customer_id = c.customer_id
JOIN `{project_id}.{dataset_id}.products` p 
    ON oi.product_id = p.product_id
WHERE o.order_date >= '2024-06-01'
AND c.customer_tier = 'Premium'
AND p.category = 'Electronics'""",
                "expected_optimizations": ["JOIN Reordering", "Partition Filtering"],
                "expected_improvement": "20-40%"
            },
            "aggregation": {
                "name": "Aggregation Test",
                "description": "GROUP BY without proper partitioning", 
                "inefficient_query": f"""SELECT 
    c.region,
    COUNT(*) as total_orders,
    COUNT(DISTINCT o.customer_id) as unique_customers,
    SUM(o.total_amount) as total_revenue,
    AVG(o.total_amount) as avg_order_value
FROM `{project_id}.{dataset_id}.orders` o
JOIN `{project_id}.{dataset_id}.customers` c 
    ON o.customer_id = c.customer_id
WHERE o.order_date >= '2024-01-01'
GROUP BY c.region
ORDER BY total_revenue DESC""",
                "expected_optimizations": ["Partition Filtering", "Approximate Aggregation"],
                "expected_improvement": "40-60%"
            },
            "window_function": {
                "name": "Window Function Test",
                "description": "Inefficient window specifications",
                "inefficient_query": f"""SELECT 
    customer_id,
    order_id,
    order_date,
    total_amount,
    ROW_NUMBER() OVER (ORDER BY total_amount DESC) as overall_rank,
    RANK() OVER (ORDER BY order_date) as date_rank,
    SUM(total_amount) OVER (ORDER BY order_date ROWS UNBOUNDED PRECEDING) as running_total
FROM `{project_id}.{dataset_id}.orders`
WHERE order_date >= '2024-06-01'
ORDER BY total_amount DESC
LIMIT 1000""",
                "expected_optimizations": ["Window Function Optimization", "Partition Filtering"],
                "expected_improvement": "15-30%"
            },
            "nested_query": {
                "name": "Nested Query Test",
                "description": "Deeply nested subqueries that can be flattened",
                "inefficient_query": f"""SELECT 
    customer_name
FROM `{project_id}.{dataset_id}.customers` c
WHERE customer_id IN (
    SELECT customer_id 
    FROM `{project_id}.{dataset_id}.orders` o1
    WHERE order_id IN (
        SELECT order_id
        FROM `{project_id}.{dataset_id}.order_items` oi
        WHERE product_id IN (
            SELECT product_id
            FROM `{project_id}.{dataset_id}.products` p
            WHERE category = 'Electronics'
        )
        AND quantity > 2
    )
    AND o1.order_date >= '2024-06-01'
    AND o1.status = 'completed'
)""",
                "expected_optimizations": ["Subquery to JOIN Conversion", "Partition Filtering"],
                "expected_improvement": "25-45%"
            }
        }
        
        return {
            "test_queries": test_queries,
            "setup_instructions": {
                "description": "To run these tests, you need to create sample data in BigQuery",
                "steps": [
                    "Set your Google Cloud Project ID in environment variables",
                    "Ensure BigQuery API is enabled",
                    "Run the test suite to automatically create sample data",
                    "Use the provided queries to test optimization"
                ]
            }
        }
        
    except Exception as e:
        logger.log_error(e, {"endpoint": "/test-queries"})
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/setup-test-data")
async def setup_test_data(request: TestSuiteRequest):
    """
    Setup test dataset and tables in BigQuery.
    
    This endpoint creates the optimizer_test_dataset and all required tables
    with sample data for testing the optimization functionality.
    """
    try:
        logger.logger.info("Setting up test dataset and tables")
        
        # Set project ID if provided
        env = os.environ.copy()
        if request.project_id:
            env["GOOGLE_CLOUD_PROJECT"] = request.project_id
        
        # Import required modules
        from config.settings import get_settings
        from src.optimizer.bigquery_client import BigQueryClient
        from google.cloud import bigquery
        from google.cloud.exceptions import Conflict
        
        settings = get_settings()
        if request.project_id:
            # Temporarily override project ID
            original_project = settings.google_cloud_project
            settings.google_cloud_project = request.project_id
        
        bq_client = BigQueryClient(project_id=request.project_id)
        dataset_id = "optimizer_test_dataset"
        
        start_time = time.time()
        
        # Create dataset
        try:
            dataset_full_id = f"{settings.google_cloud_project}.{dataset_id}"
            dataset = bigquery.Dataset(dataset_full_id)
            dataset.location = "US"
            dataset.description = "Test dataset for BigQuery Query Optimizer"
            
            dataset = bq_client.client.create_dataset(dataset, exists_ok=True)
            print(f"✅ Dataset {dataset.dataset_id} created successfully")
        except Exception as e:
            print(f"⚠️ Dataset creation warning: {e}")
        
        # Create tables with data
        tables_created = []
        
        # Customers table
        customers_sql = f"""
        CREATE OR REPLACE TABLE `{settings.google_cloud_project}.{dataset_id}.customers` AS
        SELECT 
            customer_id,
            CONCAT('Customer_', CAST(customer_id AS STRING)) as customer_name,
            CASE 
                WHEN MOD(customer_id, 4) = 0 THEN 'Premium'
                WHEN MOD(customer_id, 4) = 1 THEN 'Gold'
                WHEN MOD(customer_id, 4) = 2 THEN 'Silver'
                ELSE 'Bronze'
            END as customer_tier,
            CASE 
                WHEN MOD(customer_id, 5) = 0 THEN 'US-West'
                WHEN MOD(customer_id, 5) = 1 THEN 'US-East'
                WHEN MOD(customer_id, 5) = 2 THEN 'Europe'
                WHEN MOD(customer_id, 5) = 3 THEN 'Asia'
                ELSE 'Other'
            END as region,
            DATE_ADD('2020-01-01', INTERVAL MOD(customer_id, 1000) DAY) as signup_date
        FROM UNNEST(GENERATE_ARRAY(1, 1000)) as customer_id
        """
        
        result = bq_client.execute_query(customers_sql, dry_run=False)
        if result["success"]:
            tables_created.append("customers")
        else:
            raise Exception(f"Failed to create customers table: {result['error']}")
        
        # Orders table (partitioned)
        orders_sql = f"""
        CREATE OR REPLACE TABLE `{settings.google_cloud_project}.{dataset_id}.orders` 
        PARTITION BY order_date
        CLUSTER BY customer_id, status
        AS
        SELECT 
            order_id,
            MOD(order_id, 1000) + 1 as customer_id,
            DATE_ADD(DATE('2024-01-01'), INTERVAL MOD(order_id, 365) DAY) as order_date,
            ROUND(RAND() * 1000 + 50, 2) as total_amount,
            CASE 
                WHEN MOD(order_id, 10) = 0 THEN 'cancelled'
                WHEN MOD(order_id, 10) = 1 THEN 'pending'
                WHEN MOD(order_id, 10) = 2 THEN 'processing'
                ELSE 'completed'
            END as status,
            MOD(order_id, 50) + 1 as product_id
        FROM UNNEST(GENERATE_ARRAY(1, 50000)) as order_id
        """
        
        result = bq_client.execute_query(orders_sql, dry_run=False)
        if result["success"]:
            tables_created.append("orders")
        else:
            raise Exception(f"Failed to create orders table: {result['error']}")
        
        # Products table
        products_sql = f"""
        CREATE OR REPLACE TABLE `{settings.google_cloud_project}.{dataset_id}.products` AS
        SELECT 
            product_id,
            CONCAT('Product_', CAST(product_id AS STRING)) as product_name,
            CASE 
                WHEN MOD(product_id, 5) = 0 THEN 'Electronics'
                WHEN MOD(product_id, 5) = 1 THEN 'Clothing'
                WHEN MOD(product_id, 5) = 2 THEN 'Books'
                WHEN MOD(product_id, 5) = 3 THEN 'Home'
                ELSE 'Sports'
            END as category,
            ROUND(RAND() * 500 + 10, 2) as price
        FROM UNNEST(GENERATE_ARRAY(1, 50)) as product_id
        """
        
        result = bq_client.execute_query(products_sql, dry_run=False)
        if result["success"]:
            tables_created.append("products")
        else:
            raise Exception(f"Failed to create products table: {result['error']}")
        
        # Order items table (partitioned)
        order_items_sql = f"""
        CREATE OR REPLACE TABLE `{settings.google_cloud_project}.{dataset_id}.order_items`
        PARTITION BY order_date
        CLUSTER BY order_id
        AS
        SELECT 
            (order_id - 1) * 2 + item_seq as item_id,
            order_id,
            MOD((order_id - 1) * 2 + item_seq, 50) + 1 as product_id,
            CAST(RAND() * 5 + 1 AS INT64) as quantity,
            ROUND(RAND() * 100 + 10, 2) as unit_price,
            DATE_ADD(DATE('2024-01-01'), INTERVAL MOD(order_id, 365) DAY) as order_date
        FROM UNNEST(GENERATE_ARRAY(1, 25000)) as order_id,
        UNNEST(GENERATE_ARRAY(1, 2)) as item_seq
        """
        
        result = bq_client.execute_query(order_items_sql, dry_run=False)
        if result["success"]:
            tables_created.append("order_items")
        else:
            raise Exception(f"Failed to create order_items table: {result['error']}")
        
        execution_time = time.time() - start_time
        
        return {
            "success": True,
            "message": "Test dataset and tables created successfully",
            "dataset_id": "optimizer_test_dataset",
            "tables_created": tables_created,
            "execution_time": execution_time,
            "project_id": settings.google_cloud_project
        }
        
    except Exception as e:
        logger.log_error(e, {"endpoint": "/setup-test-data"})
        return {
            "success": False,
            "error_message": str(e),
            "message": "Failed to setup test data"
        }