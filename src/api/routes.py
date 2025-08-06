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
import subprocess
import json
from pathlib import Path
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
    validate: bool = Field(True, description="Validate query results")
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
    validate: bool = Field(True, description="Validate query results")
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
class TestSuiteRequest(BaseModel):
    """Request model for running test suite."""
    project_id: Optional[str] = Field(None, description="Google Cloud Project ID")
    test_type: str = Field("sandbox", description="Type of tests to run")
    cleanup: bool = Field(True, description="Clean up test data after tests")


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
            validate_results=request.validate
        )
        
        # Test connection first
        if not optimizer.test_connection():
            raise HTTPException(
                status_code=503, 
                detail="Failed to connect to required services"
            )
        
        result = optimizer.optimize_query(
            request.query,
            validate_results=request.validate,
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
            validate_results=request.validate
        )
        
        results = optimizer.batch_optimize_queries(
            request.queries,
            validate_results=request.validate,
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
        project_id = settings.google_cloud_project or "your-project-id"
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
        
    except OptimizationError as e:
        logger.log_error(e, {"endpoint": "/table-suggestions"})
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.log_error(e, {"endpoint": "/table-suggestions"})
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
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
        project_id = settings.google_cloud_project or "your-project-id"
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
        
    except OptimizationError as e:
        logger.log_error(e, {"endpoint": "/table-suggestions"})
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.log_error(e, {"endpoint": "/table-suggestions"})
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")