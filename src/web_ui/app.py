"""FastAPI web application for BigQuery Query Optimizer."""

import time
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from config.settings import get_settings
from src.optimizer.query_optimizer import BigQueryOptimizer
from src.common.exceptions import OptimizationError, BigQueryConnectionError
from src.common.logger import QueryOptimizerLogger


# Request/Response models
class OptimizeRequest(BaseModel):
    query: str = Field(..., min_length=1, description="SQL query to optimize")
    validate_results: bool = Field(default=True, description="Validate query results")
    measure_performance: bool = Field(default=False, description="Measure performance")
    sample_size: Optional[int] = Field(default=1000, description="Sample size for validation")


class AnalyzeRequest(BaseModel):
    query: str = Field(..., min_length=1, description="SQL query to analyze")


class BatchOptimizeRequest(BaseModel):
    queries: List[str] = Field(..., min_items=1, description="List of SQL queries")
    validate_results: bool = Field(default=True, description="Validate query results")
    max_concurrent: int = Field(default=3, description="Maximum concurrent optimizations")


class HealthResponse(BaseModel):
    status: str
    timestamp: float
    version: str
    bigquery_connected: bool
    documentation_loaded: bool


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    
    settings = get_settings()
    logger = QueryOptimizerLogger(__name__)
    
    app = FastAPI(
        title="BigQuery Query Optimizer",
        description="AI-powered BigQuery SQL query optimizer with web interface",
        version="1.0.0"
    )
    
    # Templates and static files
    templates = Jinja2Templates(directory="src/web_ui/templates")
    app.mount("/static", StaticFiles(directory="src/web_ui/static"), name="static")
    
    # Initialize optimizer (lazy loading)
    _optimizer = None
    
    def get_optimizer() -> BigQueryOptimizer:
        nonlocal _optimizer
        if _optimizer is None:
            try:
                _optimizer = BigQueryOptimizer(validate_results=True)
            except Exception as e:
                logger.log_error(e, {"operation": "initialize_optimizer"})
                raise HTTPException(
                    status_code=503, 
                    detail=f"Failed to initialize optimizer: {str(e)}"
                )
        return _optimizer
    
    # Routes
    @app.get("/", response_class=HTMLResponse)
    async def home(request: Request):
        """Home page with query optimizer interface."""
        return templates.TemplateResponse("index.html", {"request": request})
    
    @app.get("/api/health", response_model=HealthResponse)
    async def health_check():
        """Health check endpoint."""
        try:
            optimizer = get_optimizer()
            bigquery_connected = optimizer.test_connection()
            stats = optimizer.get_optimization_statistics()
            documentation_loaded = stats.get("documentation_chunks", 0) > 0
            
            return HealthResponse(
                status="healthy" if bigquery_connected else "degraded",
                timestamp=time.time(),
                version="1.0.0",
                bigquery_connected=bigquery_connected,
                documentation_loaded=documentation_loaded
            )
        except Exception as e:
            logger.log_error(e, {"operation": "health_check"})
            return HealthResponse(
                status="unhealthy",
                timestamp=time.time(),
                version="1.0.0",
                bigquery_connected=False,
                documentation_loaded=False
            )
    
    @app.post("/api/optimize")
    async def optimize_query(request: OptimizeRequest):
        """Optimize a SQL query."""
        try:
            optimizer = get_optimizer()
            
            result = optimizer.optimize_query(
                request.query,
                validate_results=request.validate_results,
                measure_performance=request.measure_performance,
                sample_size=request.sample_size
            )
            
            # Convert to dict for JSON response
            response_data = result.model_dump()
            
            # Add summary for UI
            response_data["summary"] = result.get_summary()
            
            return response_data
            
        except OptimizationError as e:
            logger.log_error(e, {"operation": "optimize_query", "query_length": len(request.query)})
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            logger.log_error(e, {"operation": "optimize_query"})
            raise HTTPException(status_code=500, detail=f"Optimization failed: {str(e)}")
    
    @app.post("/api/analyze")
    async def analyze_query(request: AnalyzeRequest):
        """Analyze a SQL query without optimizing."""
        try:
            optimizer = get_optimizer()
            
            analysis = optimizer.analyze_query_only(request.query)
            
            return analysis.model_dump()
            
        except OptimizationError as e:
            logger.log_error(e, {"operation": "analyze_query"})
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            logger.log_error(e, {"operation": "analyze_query"})
            raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    
    @app.post("/api/batch-optimize")
    async def batch_optimize(request: BatchOptimizeRequest):
        """Optimize multiple queries in batch."""
        try:
            optimizer = get_optimizer()
            
            results = optimizer.batch_optimize_queries(
                request.queries,
                validate_results=request.validate_results,
                max_concurrent=request.max_concurrent
            )
            
            # Convert results to dict format
            response_data = {
                "total_queries": len(request.queries),
                "successful_optimizations": sum(1 for r in results if not r.validation_error),
                "results": [r.model_dump() for r in results]
            }
            
            return response_data
            
        except OptimizationError as e:
            logger.log_error(e, {"operation": "batch_optimize"})
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            logger.log_error(e, {"operation": "batch_optimize"})
            raise HTTPException(status_code=500, detail=f"Batch optimization failed: {str(e)}")
    
    @app.get("/api/suggestions")
    async def get_optimization_suggestions(query: str):
        """Get optimization suggestions without applying them."""
        try:
            optimizer = get_optimizer()
            
            suggestions = optimizer.get_optimization_suggestions(query)
            
            return suggestions
            
        except OptimizationError as e:
            logger.log_error(e, {"operation": "get_suggestions"})
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            logger.log_error(e, {"operation": "get_suggestions"})
            raise HTTPException(status_code=500, detail=f"Failed to get suggestions: {str(e)}")
    
    @app.get("/api/stats")
    async def get_optimization_stats():
        """Get optimization statistics."""
        try:
            optimizer = get_optimizer()
            
            stats = optimizer.get_optimization_statistics()
            
            return stats
            
        except Exception as e:
            logger.log_error(e, {"operation": "get_stats"})
            raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")
    
    @app.post("/api/validate")
    async def validate_optimization(
        original_query: str,
        optimized_query: str,
        sample_size: int = 1000
    ):
        """Validate that optimized query returns identical results."""
        try:
            optimizer = get_optimizer()
            
            validation_result = optimizer.validate_optimization(
                original_query,
                optimized_query,
                sample_size
            )
            
            return validation_result
            
        except OptimizationError as e:
            logger.log_error(e, {"operation": "validate_optimization"})
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            logger.log_error(e, {"operation": "validate_optimization"})
            raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")
    
    return app


if __name__ == "__main__":
    import uvicorn
    
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8080)