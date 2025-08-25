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
from src.mcp_server.optimization_analyzer import OptimizationAnalyzer
import os
import time
import subprocess
import json
from pathlib import Path
from datetime import date, datetime

router = APIRouter()
logger = QueryOptimizerLogger(__name__)

# Initialize MCP handler for direct SQL processing
try:
    optimization_analyzer = OptimizationAnalyzer()
    print("✅ Optimization analyzer initialized for direct SQL processing")
except Exception as e:
    print(f"⚠️ Optimization analyzer initialization failed: {e}")
    optimization_analyzer = None

# Request/Response Models
class OptimizeRequest(BaseModel):
    query: str
    project_id: Optional[str] = None
    validate_results: bool = True
    measure_performance: bool = False
    sample_size: int = 1000


class AnalyzeRequest(BaseModel):
    """Request model for query analysis."""
    query: str = Field(..., description="SQL query to analyze")
    project_id: Optional[str] = Field(None, description="Google Cloud Project ID")


class ValidateRequest(BaseModel):
    original_query: str
    optimized_query: str
    project_id: Optional[str] = None


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
    include_execution_results: bool = Field(True, description="Include full execution and comparison results")


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
        
        # Enhanced workflow with MCP server integration
        print(f"📡 Using direct SQL processing workflow")
        
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
            measure_performance=True,  # Always measure performance for test suites
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


@router.post("/optimize-gemini")
async def optimize_query_gemini(request: OptimizeRequest):
    """
    Optimize a BigQuery SQL query using Gemini API directly.
    
    This endpoint sends the raw SQL query directly to Gemini API with all MD documentation
    without any validation or analysis. Returns optimized query with validation results.
    """
    try:
        logger.logger.info(f"Gemini optimization for query of length {len(request.query)}")
        
        # Use MCP server for Gemini-based optimization
        print(f"🤖 Using Gemini API optimization workflow")
        
        # Import the handler directly for this endpoint
        from src.mcp_server.handlers import DirectSQLOptimizationHandler
        
        handler = DirectSQLOptimizationHandler()
        
        # Send directly to Gemini API
        result = handler.optimize_with_gemini(request.query, request.project_id)
        
        if not result["success"]:
            raise HTTPException(
                status_code=400,
                detail=result.get("error", "Gemini optimization failed")
            )
        
        logger.logger.info(
            f"Gemini optimization completed: {result.get('total_optimizations', 0)} optimizations applied"
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.log_error(e, {"endpoint": "/optimize-gemini"})
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/validate-schemas")
async def validate_query_schemas(request: ValidateRequest):
    """
    Validate that both original and optimized queries reference valid schemas and tables.
    """
    try:
        logger.logger.info("Validating query schemas and tables")
        
        # Import the handler for schema validation
        from src.mcp_server.handlers import DirectSQLOptimizationHandler
        
        handler = DirectSQLOptimizationHandler()
        
        # Basic schema validation (check for valid table references)
        validation_result = {
            "success": True,
            "original_query_valid": True,
            "optimized_query_valid": True,
            "schema_issues": [],
            "table_references": {
                "original": [],
                "optimized": []
            }
        }
        
        # Extract table references from queries (simplified)
        import re
        
        # Simple regex to find table references
        table_pattern = r'FROM\s+`?([^`\s]+)`?\s+|JOIN\s+`?([^`\s]+)`?\s+'
        
        original_tables = re.findall(table_pattern, request.original_query, re.IGNORECASE)
        optimized_tables = re.findall(table_pattern, request.optimized_query, re.IGNORECASE)
        
        # Flatten and clean table references
        validation_result["table_references"]["original"] = [t for t in original_tables if t]
        validation_result["table_references"]["optimized"] = [t for t in optimized_tables if t]
        
        # Check if optimized query has more table references (potential issue)
        if len(validation_result["table_references"]["optimized"]) > len(validation_result["table_references"]["original"]):
            validation_result["schema_issues"].append("Optimized query references more tables than original")
        
        return validation_result
        
    except Exception as e:
        logger.log_error(e, {"endpoint": "/validate-schemas"})
        return {
            "success": False,
            "error": str(e),
            "message": "Schema validation failed"
        }


@router.post("/execute-and-compare")
async def execute_and_compare_queries(request: ValidateRequest):
    """
    Execute both original and optimized queries and compare results using hashing.
    """
    try:
        logger.logger.info("Executing and comparing queries")
        
        # Import BigQuery client for execution
        from src.optimizer.bigquery_client import BigQueryClient
        
        bq_client = BigQueryClient(project_id=request.project_id)
        
        # Execute original query
        original_result = bq_client.execute_query(request.original_query, dry_run=False)
        
        # Execute optimized query
        optimized_result = bq_client.execute_query(request.optimized_query, dry_run=False)
        
        if not original_result["success"]:
            raise Exception(f"Original query execution failed: {original_result.get('error')}")
        
        if not optimized_result["success"]:
            raise Exception(f"Optimized query execution failed: {optimized_result.get('error')}")
        
        # Compare results using hashing
        import hashlib
        import json
        from datetime import date, datetime
        
        class BigQueryJSONEncoder(json.JSONEncoder):
            """Custom JSON encoder for BigQuery data types."""
            def default(self, obj):
                if isinstance(obj, (date, datetime)):
                    return obj.isoformat()
                elif hasattr(obj, 'isoformat'):  # Handle other date-like objects
                    return obj.isoformat()
                elif hasattr(obj, '__dict__'):  # Handle custom objects
                    return str(obj)
                return super().default(obj)
        
        def hash_results(results):
            """Create hash of query results for comparison."""
            if not results:
                return hashlib.md5(b"no_results").hexdigest()
            
            try:
                # Normalize and sort results for consistent hashing
                normalized_results = []
                for row in results:
                    normalized_row = {}
                    for key, value in sorted(row.items()):
                        # Normalize the value for consistent hashing
                        if isinstance(value, (date, datetime)):
                            normalized_row[key] = value.isoformat()
                        elif hasattr(value, 'isoformat'):
                            normalized_row[key] = value.isoformat()
                        elif isinstance(value, (int, float)):
                            # Ensure consistent numeric representation
                            if isinstance(value, float):
                                normalized_row[key] = round(value, 6)  # Consistent decimal places
                            else:
                                normalized_row[key] = value
                        elif value is None:
                            normalized_row[key] = "NULL"
                        else:
                            normalized_row[key] = str(value).strip()
                    normalized_results.append(normalized_row)
                
                # Sort rows by a consistent key (first available key)
                if normalized_results and normalized_results[0]:
                    first_key = list(normalized_results[0].keys())[0]
                    normalized_results.sort(key=lambda x: str(x.get(first_key, '')))
                
                # Create hash from normalized data
                json_str = json.dumps(normalized_results, cls=BigQueryJSONEncoder, sort_keys=True)
                return hashlib.md5(json_str.encode()).hexdigest()
                
            except (TypeError, ValueError) as e:
                # Fallback: convert to string representation for hashing
                logger.logger.warning(f"JSON serialization failed, using string fallback: {e}")
                try:
                    # Convert results to string representation with consistent formatting
                    result_strings = []
                    for row in results:
                        row_str = []
                        for key, value in sorted(row.items()):
                            if isinstance(value, (date, datetime)):
                                row_str.append(f"{key}:{value.isoformat()}")
                            elif hasattr(value, 'isoformat'):
                                row_str.append(f"{key}:{value.isoformat()}")
                            elif isinstance(value, (int, float)):
                                if isinstance(value, float):
                                    row_str.append(f"{key}:{round(value, 6)}")
                                else:
                                    row_str.append(f"{key}:{value}")
                            elif value is None:
                                row_str.append(f"{key}:NULL")
                            else:
                                row_str.append(f"{key}:{str(value).strip()}")
                        result_strings.append("|".join(row_str))
                    
                    # Sort rows consistently
                    sorted_strings = sorted(result_strings)
                    return hashlib.md5("||".join(sorted_strings).encode()).hexdigest()
                except Exception as fallback_error:
                    logger.logger.error(f"Fallback hashing also failed: {fallback_error}")
                    return hashlib.md5(f"fallback_hash_{len(results)}".encode()).hexdigest()
        
        original_hash = hash_results(original_result.get("results", []))
        optimized_hash = hash_results(optimized_result.get("results", []))
        
        # Calculate actual performance improvements
        original_time = original_result.get("execution_time_ms", 0)
        optimized_time = optimized_result.get("execution_time_ms", 0)
        original_bytes = original_result.get("bytes_processed", 0)
        optimized_bytes = optimized_result.get("bytes_processed", 0)
        
        # Calculate actual improvements (not expected)
        time_improvement = 0
        bytes_improvement = 0
        cost_improvement = 0
        time_saved_ms = 0
        bytes_saved = 0
        cost_saved = 0
        
        if original_time > 0:
            time_improvement = (original_time - optimized_time) / original_time
            time_saved_ms = original_time - optimized_time
        
        if original_bytes > 0:
            bytes_improvement = (original_bytes - optimized_bytes) / original_bytes
            bytes_saved = original_bytes - optimized_bytes
        
        # Estimate cost improvements (BigQuery pricing: $5 per TB processed)
        if original_bytes > 0:
            original_cost = (original_bytes / (1024**4)) * 5  # Convert bytes to TB, then multiply by $5
            optimized_cost = (optimized_bytes / (1024**4)) * 5
            if original_cost > 0:
                cost_improvement = (original_cost - optimized_cost) / original_cost
                cost_saved = original_cost - optimized_cost
        
        comparison_result = {
            "success": True,
            "original_query_results": original_result.get("results", []),
            "optimized_query_results": optimized_result.get("results", []),
            "original_row_count": len(original_result.get("results", [])),
            "optimized_row_count": len(optimized_result.get("results", [])),
            "results_identical": original_hash == optimized_hash,
            "original_hash": original_hash,
            "optimized_hash": optimized_hash,
            "performance_metrics": {
                "success": True,
                "original_time_ms": original_time,
                "optimized_time_ms": optimized_time,
                "original_bytes": original_bytes,
                "optimized_bytes": optimized_bytes,
                "original_cost": round(original_cost, 6) if original_bytes > 0 else 0,
                "optimized_cost": round(optimized_cost, 6) if optimized_bytes > 0 else 0,
                # Actual improvements achieved (not expected)
                "time_improvement": max(0, time_improvement),
                "bytes_improvement": max(0, bytes_improvement),
                "cost_improvement": max(0, cost_improvement),
                "time_saved_ms": max(0, time_saved_ms),
                "bytes_saved": max(0, bytes_saved),
                "cost_saved": round(max(0, cost_saved), 6),
                "performance_summary": f"Time: {time_improvement*100:.1f}% faster, Data: {bytes_improvement*100:.1f}% less, Cost: {cost_improvement*100:.1f}% savings" if time_improvement > 0 else "No performance improvement detected"
            }
        }
        
        return comparison_result
        
    except Exception as e:
        logger.log_error(e, {"endpoint": "/execute-and-compare"})
        return {
            "success": False,
            "error": str(e),
            "message": "Query execution and comparison failed"
        }


@router.post("/analyze", response_model=QueryAnalysis)
async def analyze_query(request: AnalyzeRequest):
    """
    Analyze a SQL query without optimizing it.
    
    This endpoint provides detailed analysis of query structure, complexity,
    and potential optimization opportunities.
    """
    try:
        logger.logger.info(f"Analyzing query of length {len(request.query)}")
        
        # Use MCP server for enhanced analysis
        print(f"📊 Using direct SQL analysis")
        
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
        
        print(f"🔍 Validating optimization with result comparison")
        
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
        
        print(f"📦 Batch optimization using optimization analyzer workflow")
        
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
    Now includes MCP server status.
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
            "available_patterns": stats.get("available_patterns", 0),
            "direct_sql_handler_available": True,
            "llm_optimizer_status": "initialized"
        }
        
        status = "healthy" if all([
            connection_ok,
            components["documentation_loaded"],
            components["available_patterns"] > 0,
            components["direct_sql_handler_available"]
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
    
    🚀 UNIFIED WORKFLOW: Test suites now use the EXACT SAME implementation as single queries:
    1. Raw SQL → Gemini API → Regex Syntax Fix → LLM Cleanup → Schema Validation → LLM Final Cleanup → Execution & Comparison
    
    This ensures consistent behavior and results between single queries and test suites.
    
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
        "description": "Basic SELECT with inefficient WHERE clause (Column Pruning, Predicate Pushdown).",
        "test_cases": [
            {
                "name": "SELECT * with Date",
                "description": "Triggers Column Pruning (SELECT *).",
                "query": f"""SELECT *
FROM `{request.project_id or 'your-project'}.optimizer_test_dataset.customers`
WHERE `customer_tier` = 'Premium'
  AND region IN ('US-East', 'US-West')
  AND signup_date >= '2020-01-01'
  LIMIT 100;"""
            },
            {
                "name": "SELECT * with Multiple Filters on Customers",
                "description": "Triggers Column Pruning; uses backticked `customer tier`.",
                "query": f"""SELECT *
FROM `{request.project_id or 'your-project'}.optimizer_test_dataset.customers`
WHERE `customer_tier` = 'Premium'
  AND region IN ('US-East', 'US-West')
  AND signup_date >= '2020-01-01'"""
            },
            {
                "name": "Filter Applied Late in Outer Query",
                "description": "Triggers Predicate Pushdown (move WHERE into base query).",
                "query": f"""SELECT *
FROM (
  SELECT order_id, customer_id, total_amount, order_date
  FROM `{request.project_id or 'your-project'}.optimizer_test_dataset.orders`
) t
WHERE t.order_date >= '2024-01-01'"""
            }
        ]
    },

    "complex_join": {
        "name": "Complex JOIN Test",
        "description": "Multi-table JOIN with suboptimal ordering (JOIN Reordering, Column Pruning, Predicate Pushdown).",
        "test_cases": [
            {
                "name": "4-Table JOIN with Large Table First",
                "description": "Triggers JOIN Reordering (3+ joins).",
                "query": f"""SELECT
  c.customer_name,
  o.order_id,
  p.product_name,
  oi.quantity,
  o.total_amount
FROM `{request.project_id or 'your-project'}.optimizer_test_dataset.products` p
JOIN `{request.project_id or 'your-project'}.optimizer_test_dataset.order_items` oi ON p.product_id = oi.product_id
JOIN `{request.project_id or 'your-project'}.optimizer_test_dataset.orders`      o ON oi.order_id  = o.order_id
JOIN `{request.project_id or 'your-project'}.optimizer_test_dataset.customers`   c ON o.customer_id = c.customer_id
WHERE p.category IN ('Electronics','Appliances')
  AND o.status = 'completed'
ORDER BY o.total_amount DESC
LIMIT 100"""
            },
#             {
#                 "name": "LEFT JOIN with SELECT *",
#                 "description": "Triggers Column Pruning across a JOIN; may also hint JOIN Reordering.",
#                 "query": f"""SELECT *
# FROM `{request.project_id or 'your-project'}.optimizer_test_dataset.customers` c
# LEFT JOIN `{request.project_id or 'your-project'}.optimizer_test_dataset.orders` o
#   ON c.customer_id = o.customer_id
# LEFT JOIN `{request.project_id or 'your-project'}.optimizer_test_dataset.products` p
#   ON o.product_id = p.product_id
# WHERE c.region = 'Europe'
# LIMIT 100;"""
#             },
            {
                "name": "JOINs with Late Filter in Outer Query",
                "description": "Triggers Predicate Pushdown for join pipelines.",
                "query": f"""SELECT *
FROM (
  SELECT c.customer_name, o.total_amount, o.order_date
  FROM `{request.project_id or 'your-project'}.optimizer_test_dataset.customers` c
  JOIN `{request.project_id or 'your-project'}.optimizer_test_dataset.orders` o
    ON c.customer_id = o.customer_id
) t
WHERE t.order_date >= '2024-01-01'"""
            }
        ]
    },

    "aggregation": {
        "name": "Aggregation Test",
        "description": "GROUP BY without proper optimization (Approximate Aggregation, MV Suggestion, HAVING→WHERE).",
        "test_cases": [
            {
                "name": "COUNT DISTINCT on Large Join",
                "description": "Triggers Approximate Aggregation (APPROX_COUNT_DISTINCT).",
                "query": f"""SELECT 
  c.region,
  COUNT(*) AS total_orders,
  COUNT(DISTINCT o.customer_id) AS unique_customers,
  SUM(o.total_amount) AS total_revenue
FROM `{request.project_id or 'your-project'}.optimizer_test_dataset.orders` o
JOIN `{request.project_id or 'your-project'}.optimizer_test_dataset.customers` c 
  ON o.customer_id = c.customer_id
WHERE o.order_date >= '2024-01-01'
GROUP BY c.region"""
            },
            {
                "name": "Daily Revenue Summary by Region",
                "description": "Triggers Materialized View Suggestion for a frequent report pattern.",
                "query": f"""SELECT
  c.region,
  DATE_TRUNC(o.order_date, WEEK) AS order_week,
  COUNT(*) AS weekly_orders,
  SUM(o.total_amount) AS weekly_revenue
FROM `{request.project_id or 'your-project'}.optimizer_test_dataset.orders` o
JOIN `{request.project_id or 'your-project'}.optimizer_test_dataset.customers` c ON o.customer_id = c.customer_id
WHERE o.order_date >= '2024-01-01'
GROUP BY c.region, DATE_TRUNC(o.order_date, WEEK);"""
            },
            {
                "name": "HAVING on Non-Aggregate Column",
                "description": "Triggers HAVING→WHERE Conversion.",
                "query": f"""SELECT product_id, COUNT(*) AS line_items
FROM `{request.project_id or 'your-project'}.optimizer_test_dataset.order_items`
GROUP BY product_id
HAVING product_id IN (
  SELECT product_id
  FROM `your-project.optimizer_test_dataset.products`
  WHERE category = 'Electronics'
);"""
            }
        ]
    },

    "window_function": {
        "name": "Window Function Test",
        "description": "Inefficient window specs (Window Function Optimization; one case also hits Column Pruning).",
        "test_cases": [
#             {
#                 "name": "ROW_NUMBER without PARTITION",
#                 "description": "Triggers Window Function Optimization.",
#                 "query": f"""SELECT 
#   customer_id,
#   order_id,
#   order_date,
#   total_amount,
#   ROW_NUMBER() OVER (ORDER BY total_amount DESC) AS overall_rank
# FROM `{request.project_id or 'your-project'}.optimizer_test_dataset.orders`
# WHERE order_date >= '2024-06-01'"""
#             },
            {
                "name": "Multiple Windows Unpartitioned",
                "description": "Triggers Window Function Optimization.",
                "query": f"""SELECT 
  customer_id,
  order_date,
  total_amount,
  LAG(total_amount) OVER (ORDER BY order_date) AS prev_amount,
  LEAD(total_amount) OVER (ORDER BY order_date) AS next_amount,
  SUM(total_amount) OVER (ORDER BY order_date ROWS UNBOUNDED PRECEDING) AS running_total
FROM `{request.project_id or 'your-project'}.optimizer_test_dataset.orders`
WHERE customer_id <= 100"""
            },
            {
                "name": "Window with SELECT *",
                "description": "Triggers Column Pruning + Window Function Optimization.",
                "query": f"""SELECT *,
  NTILE(4) OVER (ORDER BY total_amount) AS quartile,
  PERCENT_RANK() OVER (ORDER BY order_date) AS date_percentile
FROM `{request.project_id or 'your-project'}.optimizer_test_dataset.orders`
WHERE order_date >= '2024-01-01'
LIMIT 500"""
            }
        ]
    },

    "nested_query": {
        "name": "Nested Query Test",
        "description": "Deeply nested subqueries that can be flattened (Subquery→JOIN Conversion).",
        "test_cases": [
            {
                "name": "EXISTS Subquery",
                "description": "Triggers Subquery→JOIN Conversion.",
                "query": f"""SELECT c.customer_name
FROM `{request.project_id or 'your-project'}.optimizer_test_dataset.customers` c
WHERE EXISTS (
  SELECT 1
  FROM `{request.project_id or 'your-project'}.optimizer_test_dataset.orders` o
  WHERE o.customer_id = c.customer_id
    AND o.status = 'completed'
)"""
            },
            {
                "name": "Nested IN Subqueries across 3 tables",
                "description": "Triggers Subquery→JOIN Conversion.",
                "query": f"""SELECT DISTINCT c.customer_name
FROM `{request.project_id or 'your-project'}.optimizer_test_dataset.customers` c
WHERE c.customer_id IN (
  SELECT o.customer_id
  FROM `{request.project_id or 'your-project'}.optimizer_test_dataset.orders` o
  WHERE o.order_id IN (
    SELECT oi.order_id
    FROM `{request.project_id or 'your-project'}.optimizer_test_dataset.order_items` oi
    WHERE oi.product_id IN (
      SELECT p.product_id
      FROM `{request.project_id or 'your-project'}.optimizer_test_dataset.products` p
      WHERE p.category = 'Electronics'
    )
  )
)"""
            },
#             {
#                 "name": "Correlated Subqueries in SELECT",
#                 "description": "Triggers Subquery→JOIN Conversion.",
#                 "query": f"""SELECT 
#   c.customer_id,
#   c.customer_name,
#   (SELECT COUNT(*) 
#    FROM `{request.project_id or 'your-project'}.optimizer_test_dataset.orders` o 
#    WHERE o.customer_id = c.customer_id 
#      AND o.status = 'completed') AS completed_orders,
#   (SELECT SUM(total_amount) 
#    FROM `{request.project_id or 'your-project'}.optimizer_test_dataset.orders` o2 
#    WHERE o2.customer_id = c.customer_id 
#      AND o2.order_date >= '2024-01-01') AS total_spent_2024
# FROM `{request.project_id or 'your-project'}.optimizer_test_dataset.customers` c
# WHERE `customer tier` IN ('Premium', 'Gold')"""
#             }
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
                
                # Use Gemini-based optimization workflow for test suites
                try:
                    from src.mcp_server.handlers import DirectSQLOptimizationHandler
                    
                    handler = DirectSQLOptimizationHandler()
                    
                    # Send directly to Gemini API for optimization
                    logger.logger.info(f"Starting Gemini optimization for test case: {test_case['name']}")
                    logger.logger.info(f"Test query: {test_query[:200]}...")
                    logger.logger.info(f"Project ID: {actual_project_id}")
                    
                    gemini_result = handler.optimize_with_gemini(test_query, actual_project_id)
                    
                    logger.logger.info(f"Gemini result for {test_case['name']}: success={gemini_result.get('success')}, optimizations={len(gemini_result.get('optimizations_applied', []))}")
                    
                    if gemini_result.get("success"):
                        # Convert Gemini result to OptimizationResult format
                        from src.common.models import OptimizationResult, QueryAnalysis, AppliedOptimization
                        
                        # Create QueryAnalysis
                        query_analysis = QueryAnalysis(
                            original_query=test_query,
                            query_hash=gemini_result.get("original_hash", "unknown"),
                            complexity="moderate",  # Default complexity
                            table_count=gemini_result.get("table_count", 0),
                            join_count=gemini_result.get("join_count", 0),
                            subquery_count=gemini_result.get("subquery_count", 0),
                            window_function_count=gemini_result.get("window_function_count", 0),
                            aggregate_function_count=gemini_result.get("aggregate_function_count", 0),
                            potential_issues=gemini_result.get("potential_issues", []),
                            applicable_patterns=gemini_result.get("applicable_patterns", [])
                        )
                        
                        # Create AppliedOptimization list
                        optimizations_applied = []
                        if gemini_result.get("optimizations_applied"):
                            for opt in gemini_result["optimizations_applied"]:
                                applied_opt = AppliedOptimization(
                                    pattern_id=opt.get("pattern_id", "gemini_optimization"),
                                    pattern_name=opt.get("name", "AI-Generated Optimization"),
                                    description=opt.get("description", "Optimization applied"),
                                    before_snippet=opt.get("before_snippet", ""),
                                    after_snippet=opt.get("after_snippet", ""),
                                    documentation_reference=opt.get("documentation_reference"),
                                    expected_improvement=opt.get("expected_improvement"),
                                    confidence_score=opt.get("confidence_score", 1.0)
                                )
                                optimizations_applied.append(applied_opt)
                        
                        # Create OptimizationResult
                        optimization_result = OptimizationResult(
                            original_query=test_query,
                            query_analysis=query_analysis,
                            optimized_query=gemini_result.get("optimized_query", test_query),
                            optimizations_applied=optimizations_applied,
                            total_optimizations=len(optimizations_applied),
                            estimated_improvement=gemini_result.get("estimated_improvement"),
                            results_identical=gemini_result.get("results_identical", False),
                            execution_results=gemini_result.get("execution_results")
                        )
                        
                        logger.logger.info(f"Gemini optimization successful for test case: {test_case['name']}")
                        
                    else:
                        # Fallback to basic optimization if Gemini fails
                        error_msg = gemini_result.get('error', 'Unknown error')
                        logger.logger.warning(f"Gemini optimization failed for {test_case['name']}, using fallback: {error_msg}")
                        
                        # Create a minimal optimization result for failed Gemini cases
                        from src.common.models import OptimizationResult, QueryAnalysis, AppliedOptimization
                        
                        # Create minimal QueryAnalysis
                        query_analysis = QueryAnalysis(
                            original_query=test_query,
                            query_hash="gemini_failed",
                            complexity="moderate",  # Use valid enum value instead of "unknown"
                            table_count=0,
                            join_count=0,
                            subquery_count=0,
                            window_function_count=0,
                            aggregate_function_count=0,
                            potential_issues=[f"Gemini optimization failed: {error_msg}"],
                            applicable_patterns=[]
                        )
                        
                        # Create minimal OptimizationResult
                        optimization_result = OptimizationResult(
                            original_query=test_query,
                            query_analysis=query_analysis,
                            optimized_query=test_query,  # No optimization applied
                            optimizations_applied=[],
                            total_optimizations=0,
                            estimated_improvement=0.0,
                            results_identical=True,  # Same query = same results
                            validation_error=f"Gemini optimization failed: {error_msg}",
                            potential_issues=[f"Gemini optimization failed: {error_msg}"]
                        )
                
                except Exception as gemini_error:
                    logger.logger.warning(f"Gemini optimization failed for {test_case['name']}, using fallback: {gemini_error}")
                    
                    # Create a minimal optimization result for failed Gemini cases
                    from src.common.models import OptimizationResult, QueryAnalysis, AppliedOptimization
                    
                    # Create minimal QueryAnalysis
                    query_analysis = QueryAnalysis(
                        original_query=test_query,
                        query_hash="gemini_exception",
                        complexity="moderate",  # Use valid enum value instead of "unknown"
                        table_count=0,
                        join_count=0,
                        subquery_count=0,
                        window_function_count=0,
                        aggregate_function_count=0,
                        potential_issues=[f"Gemini optimization exception: {str(gemini_error)}"],
                        applicable_patterns=[]
                    )
                    
                    # Create minimal OptimizationResult
                    optimization_result = OptimizationResult(
                        original_query=test_query,
                        query_analysis=query_analysis,
                        optimized_query=test_query,  # No optimization applied
                        optimizations_applied=[],
                        total_optimizations=0,
                        estimated_improvement=0.0,
                        results_identical=True,  # Same query = same results
                        validation_error=f"Gemini optimization exception: {str(gemini_error)}",
                        potential_issues=[f"Gemini optimization exception: {str(gemini_error)}"]
                    )
                
                # Apply schema validation and correction if Gemini optimization was successful
                if gemini_result.get("success") and gemini_result.get("optimized_query"):
                    try:
                        # The optimize_with_gemini method already handles the complete workflow:
                        # 1. Syntax validation and fixing
                        # 2. LLM cleanup after syntax fixes  
                        # 3. Schema validation and correction
                        # 4. LLM final cleanup after schema validation
                        # 5. Execution and comparison
                        
                        # No need to manually call schema validation - it's already done!
                        # The gemini_result contains the fully processed and validated query
                        
                        logger.logger.info(f"Gemini optimization completed with full workflow for {test_case['name']}")
                        logger.logger.info(f"Final optimized query: {gemini_result.get('optimized_query', '')[:200]}...")
                        
                        # The optimization_result already contains the final optimized query
                        # from the complete workflow, so no additional processing is needed
                        
                    except Exception as workflow_error:
                        logger.logger.warning(f"Error accessing workflow results for {test_case['name']}: {workflow_error}")
                        # Continue with the results from optimize_with_gemini
                else:
                    logger.logger.info(f"Gemini optimization workflow completed for {test_case['name']}")
                
                # Enhanced execution and comparison for test suites
                if request.validate_results and request.project_id and request.include_execution_results:
                    # Initialize result variables
                    original_results = None
                    optimized_results = None
                    
                    try:
                        # The optimize_with_gemini method already executed and compared both queries
                        # Use those results directly instead of re-executing
                        if gemini_result.get("success") and gemini_result.get("execution_results"):
                            # Use Gemini's execution results (same as single queries)
                            execution_results = gemini_result["execution_results"]
                            
                            if execution_results.get("success"):
                                # Update the optimization result with execution results
                                optimization_result.execution_results = execution_results
                                optimization_result.results_identical = execution_results.get("results_identical", False)
                                
                                # Use the results from the workflow (same as single queries)
                                if execution_results.get("original_query_results"):
                                    original_results = execution_results["original_query_results"]
                                if execution_results.get("optimized_query_results"):
                                    optimized_results = execution_results["optimized_query_results"]
                                
                                logger.logger.info(f"Using execution results from Gemini workflow for test case: {test_case['name']}")
                                logger.logger.info(f"Results identical: {execution_results.get('results_identical', False)}")
                                
                                # Also update performance metrics from the workflow
                                if execution_results.get("performance_metrics"):
                                    logger.logger.info(f"Performance metrics from workflow: {execution_results['performance_metrics'].get('performance_summary', 'N/A')}")
                            else:
                                logger.logger.warning(f"Gemini execution results failed for {test_case['name']}, falling back to manual execution")
                                # Fall back to manual execution only if workflow execution failed
                                original_results, optimized_results = await _execute_queries_manually(test_case, test_query, optimization_result, actual_project_id)
                        else:
                            # No execution results from workflow, fall back to manual execution
                            logger.logger.info(f"No execution results from workflow for {test_case['name']}, using manual execution")
                            original_results, optimized_results = await _execute_queries_manually(test_case, test_query, optimization_result, actual_project_id)
                        
                    except Exception as exec_error:
                        logger.logger.warning(f"Could not get execution results for {test_case['name']}: {exec_error}")
                        # Fall back to basic execution
                        original_results, optimized_results = await _execute_queries_manually(test_case, test_query, optimization_result, actual_project_id)
                else:
                    # Basic execution without project ID
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
                        logger.logger.warning(f"Could not execute queries for result comparison: {e}")
                
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
                        complexity="moderate",  # Use valid enum value
                        table_count=0,
                        join_count=0,
                        subquery_count=0,
                        window_function_count=0,
                        aggregate_function_count=0,
                        potential_issues=[f"Test case execution failed: {str(e)}"],
                        applicable_patterns=[]
                    ),
                    optimized_query=test_case["query"],
                    optimizations_applied=[],
                    total_optimizations=0,
                    validation_error=str(e),
                    potential_issues=[f"Test case execution failed: {str(e)}"]
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


# Helper function for manual query execution in test suites
async def _execute_queries_manually(test_case, test_query, optimization_result, actual_project_id):
    """
    Fallback function to manually execute queries when the Gemini workflow doesn't provide execution results.
    This ensures test suites can still show results even if the main workflow fails.
    """
    try:
        from src.optimizer.bigquery_client import BigQueryClient
        
        # Initialize BigQuery client
        bq_client = BigQueryClient(project_id=actual_project_id)
        
        # Fix project ID in test query before execution
        test_query_fixed = test_query
        if 'your-project' in test_query_fixed:
            test_query_fixed = test_query_fixed.replace('your-project', actual_project_id)
        
        # Get original query results
        original_results = None
        original_exec = bq_client.execute_query(test_query_fixed, dry_run=False)
        if original_exec["success"]:
            original_results = original_exec["results"][:1000]  # Get more rows for better comparison
        
        # Get optimized query results
        optimized_results = None
        optimized_query_fixed = optimization_result.optimized_query
        if 'your-project' in optimized_query_fixed:
            optimized_query_fixed = optimized_query_fixed.replace('your-project', actual_project_id)
        
        optimized_exec = bq_client.execute_query(optimized_query_fixed, dry_run=False)
        if optimized_exec["success"]:
            optimized_results = optimized_exec["results"][:1000]  # Get more rows for better comparison
        
        logger.logger.info(f"Manual execution completed for {test_case['name']}")
        return original_results, optimized_results
        
    except Exception as e:
        logger.logger.warning(f"Manual execution failed for {test_case['name']}: {e}")
        return None, None


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


@router.post("/debug-hashing")
async def debug_hashing(request: ValidateRequest):
    """
    Debug endpoint to show detailed hashing information for troubleshooting.
    """
    try:
        logger.logger.info("Debugging hashing process")
        
        # Import BigQuery client for execution
        from src.optimizer.bigquery_client import BigQueryClient
        
        bq_client = BigQueryClient(project_id=request.project_id)
        
        # Execute both queries
        original_result = bq_client.execute_query(request.original_query, dry_run=False)
        optimized_result = bq_client.execute_query(request.optimized_query, dry_run=False)
        
        if not original_result["success"]:
            raise Exception(f"Original query execution failed: {original_result.get('error')}")
        
        if not optimized_result["success"]:
            raise Exception(f"Optimized query execution failed: {optimized_result.get('error')}")
        
        # Get the hashing function from the execute-and-compare endpoint
        import hashlib
        import json
        from datetime import date, datetime
        
        class BigQueryJSONEncoder(json.JSONEncoder):
            """Custom JSON encoder for BigQuery data types."""
            def default(self, obj):
                if isinstance(obj, (date, datetime)):
                    return obj.isoformat()
                elif hasattr(obj, 'isoformat'):
                    return obj.isoformat()
                elif hasattr(obj, '__dict__'):
                    return str(obj)
                return super().default(obj)
        
        def hash_results_debug(results):
            """Debug version of hash_results that shows the process."""
            if not results:
                return {
                    "hash": hashlib.md5(b"no_results").hexdigest(),
                    "normalized_data": [],
                    "process": "empty_results"
                }
            
            try:
                # Normalize and sort results for consistent hashing
                normalized_results = []
                for i, row in enumerate(results):
                    normalized_row = {}
                    for key, value in sorted(row.items()):
                        # Normalize the value for consistent hashing
                        if isinstance(value, (date, datetime)):
                            normalized_row[key] = value.isoformat()
                        elif hasattr(value, 'isoformat'):
                            normalized_row[key] = value.isoformat()
                        elif isinstance(value, (int, float)):
                            if isinstance(value, float):
                                normalized_row[key] = round(value, 6)
                            else:
                                normalized_row[key] = value
                        elif value is None:
                            normalized_row[key] = "NULL"
                        else:
                            normalized_row[key] = str(value).strip()
                    normalized_results.append(normalized_row)
                
                # Sort rows by first available key
                if normalized_results and normalized_results[0]:
                    first_key = list(normalized_results[0].keys())[0]
                    normalized_results.sort(key=lambda x: str(x.get(first_key, '')))
                
                # Create hash from normalized data
                json_str = json.dumps(normalized_results, cls=BigQueryJSONEncoder, sort_keys=True)
                hash_value = hashlib.md5(json_str.encode()).hexdigest()
                
                return {
                    "hash": hash_value,
                    "normalized_data": normalized_results,
                    "json_string": json_str,
                    "process": "json_normalization",
                    "row_count": len(results)
                }
                
            except Exception as e:
                # Fallback hashing
                try:
                    result_strings = []
                    for row in results:
                        row_str = []
                        for key, value in sorted(row.items()):
                            if isinstance(value, (date, datetime)):
                                row_str.append(f"{key}:{value.isoformat()}")
                            elif hasattr(value, 'isoformat'):
                                row_str.append(f"{key}:{value.isoformat()}")
                            elif isinstance(value, (int, float)):
                                if isinstance(value, float):
                                    row_str.append(f"{key}:{round(value, 6)}")
                                else:
                                    row_str.append(f"{key}:{value}")
                            elif value is None:
                                row_str.append(f"{key}:NULL")
                            else:
                                row_str.append(f"{key}:{str(value).strip()}")
                        result_strings.append("|".join(row_str))
                    
                    sorted_strings = sorted(result_strings)
                    combined = "||".join(sorted_strings)
                    hash_value = hashlib.md5(combined.encode()).hexdigest()
                    
                    return {
                        "hash": hash_value,
                        "normalized_data": result_strings,
                        "combined_string": combined,
                        "process": "string_fallback",
                        "row_count": len(results),
                        "error": str(e)
                    }
                except Exception as fallback_error:
                    return {
                        "hash": hashlib.md5(f"fallback_hash_{len(results)}".encode()).hexdigest(),
                        "process": "ultimate_fallback",
                        "row_count": len(results),
                        "error": f"JSON: {str(e)}, Fallback: {str(fallback_error)}"
                    }
        
        # Get debug info for both queries
        original_debug = hash_results_debug(original_result.get("results", []))
        optimized_debug = hash_results_debug(optimized_result.get("results", []))
        
        return {
            "success": True,
            "original_query": {
                "hash": original_debug["hash"],
                "process": original_debug["process"],
                "row_count": original_debug["row_count"],
                "normalized_data": original_debug.get("normalized_data", []),
                "json_string": original_debug.get("json_string", ""),
                "combined_string": original_debug.get("combined_string", ""),
                "error": original_debug.get("error", "")
            },
            "optimized_query": {
                "hash": optimized_debug["hash"],
                "process": optimized_debug["process"],
                "row_count": optimized_debug["row_count"],
                "normalized_data": optimized_debug.get("normalized_data", []),
                "json_string": optimized_debug.get("json_string", ""),
                "combined_string": optimized_debug.get("combined_string", ""),
                "error": optimized_debug.get("error", "")
            },
            "comparison": {
                "hashes_identical": original_debug["hash"] == optimized_debug["hash"],
                "processes_identical": original_debug["process"] == optimized_debug["process"],
                "row_counts_identical": original_debug["row_count"] == optimized_debug["row_count"]
            }
        }
        
    except Exception as e:
        logger.log_error(e, {"endpoint": "/debug-hashing"})
        return {
            "success": False,
            "error": str(e),
            "message": "Hashing debug failed"
        }