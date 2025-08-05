"""Main BigQuery query optimizer that orchestrates all components."""

import asyncio
import time
from typing import Dict, List, Optional, Any
import requests

from config.settings import get_settings
from src.common.exceptions import OptimizationError, BigQueryConnectionError
from src.common.logger import QueryOptimizerLogger
from src.common.models import (
    OptimizationResult, 
    QueryAnalysis, 
    MCPRequest,
    PerformanceMetrics
)
from src.crawler.documentation_processor import DocumentationProcessor
from src.mcp_server.handlers import OptimizationHandler
from src.optimizer.ai_optimizer import GeminiQueryOptimizer
from src.optimizer.bigquery_client import BigQueryClient
from src.optimizer.validator import QueryValidator


class BigQueryOptimizer:
    """Main BigQuery query optimizer that coordinates all optimization components."""
    
    def __init__(
        self, 
        project_id: Optional[str] = None,
        use_mcp_server: bool = True,
        validate_results: bool = True
    ):
        self.settings = get_settings()
        self.logger = QueryOptimizerLogger(__name__)
        
        # Initialize components
        try:
            self.bq_client = BigQueryClient(project_id)
            self.documentation_processor = DocumentationProcessor()
            self.optimization_handler = OptimizationHandler(self.documentation_processor)
            self.ai_optimizer = GeminiQueryOptimizer()
            
            if validate_results:
                self.validator = QueryValidator(self.bq_client)
            else:
                self.validator = None
            
            self.use_mcp_server = use_mcp_server
            
            self.logger.logger.info("BigQuery optimizer initialized successfully")
            
        except Exception as e:
            self.logger.log_error(e, {"operation": "optimizer_initialization"})
            raise OptimizationError(f"Failed to initialize optimizer: {str(e)}")
    
    def optimize_query(
        self, 
        query: str,
        validate_results: bool = True,
        measure_performance: bool = False,
        sample_size: Optional[int] = 1000
    ) -> OptimizationResult:
        """Optimize a BigQuery SQL query end-to-end."""
        
        start_time = time.time()
        
        try:
            self.logger.logger.info(f"Starting optimization for query of length {len(query)}")
            
            # Step 1: Analyze the query
            analysis = asyncio.run(self.optimization_handler.analyze_query(query))
            
            # Step 2: Get applicable optimization patterns
            patterns = asyncio.run(self.optimization_handler.get_patterns_for_query(query))
            
            # Step 3: Get documentation context
            documentation_context = None
            if self.use_mcp_server:
                try:
                    doc_results = self.documentation_processor.search_documentation(
                        query, n_results=5
                    )
                    documentation_context = doc_results
                except Exception as e:
                    self.logger.logger.warning(f"Failed to get documentation context: {e}")
            
            # Step 4: Use AI to optimize the query
            optimization_result = self.ai_optimizer.optimize_query(
                query, analysis, patterns, documentation_context
            )
            
            # Step 5: Validate results if requested
            if validate_results and self.validator:
                validation_result = self.validator.validate_query_results(
                    query, 
                    optimization_result.optimized_query,
                    sample_size
                )
                
                optimization_result.results_identical = validation_result["identical"]
                if not validation_result["identical"]:
                    optimization_result.validation_error = validation_result.get("error")
            
            # Step 6: Measure performance if requested
            if measure_performance:
                try:
                    performance_comparison = self.bq_client.compare_query_performance(
                        query, 
                        optimization_result.optimized_query,
                        iterations=self.settings.performance_test_iterations
                    )
                    
                    if performance_comparison["success"]:
                        optimization_result.actual_improvement = performance_comparison["improvement_percentage"]
                        
                        # Create performance metrics
                        optimization_result.original_performance = PerformanceMetrics(
                            execution_time_ms=int(performance_comparison["original_avg_ms"])
                        )
                        optimization_result.optimized_performance = PerformanceMetrics(
                            execution_time_ms=int(performance_comparison["optimized_avg_ms"])
                        )
                        
                        self.logger.log_performance_comparison(
                            int(performance_comparison["original_avg_ms"]),
                            int(performance_comparison["optimized_avg_ms"]),
                            performance_comparison["improvement_percentage"]
                        )
                
                except Exception as e:
                    self.logger.logger.warning(f"Performance measurement failed: {e}")
            
            # Update processing time
            optimization_result.processing_time_seconds = time.time() - start_time
            
            # Log optimization summary
            self.logger.logger.info(
                "Query optimization completed",
                optimizations_applied=optimization_result.total_optimizations,
                estimated_improvement=optimization_result.estimated_improvement,
                actual_improvement=optimization_result.actual_improvement,
                results_identical=optimization_result.results_identical,
                processing_time=optimization_result.processing_time_seconds
            )
            
            return optimization_result
            
        except Exception as e:
            self.logger.log_error(e, {"operation": "optimize_query", "query_length": len(query)})
            
            # Return a failed optimization result
            return OptimizationResult(
                original_query=query,
                query_analysis=QueryAnalysis(
                    original_query=query,
                    query_hash="error",
                    complexity="simple",
                    table_count=0,
                    join_count=0,
                    subquery_count=0,
                    window_function_count=0,
                    aggregate_function_count=0,
                    potential_issues=[f"Optimization failed: {str(e)}"],
                    applicable_patterns=[]
                ),
                optimized_query=query,
                optimizations_applied=[],
                total_optimizations=0,
                processing_time_seconds=time.time() - start_time,
                validation_error=str(e)
            )
    
    def analyze_query_only(self, query: str) -> QueryAnalysis:
        """Analyze a query without optimizing it."""
        try:
            return asyncio.run(self.optimization_handler.analyze_query(query))
        except Exception as e:
            self.logger.log_error(e, {"operation": "analyze_query_only"})
            raise OptimizationError(f"Failed to analyze query: {str(e)}")
    
    def get_optimization_suggestions(self, query: str) -> Dict[str, Any]:
        """Get optimization suggestions without actually optimizing the query."""
        try:
            return asyncio.run(self.optimization_handler.get_optimization_suggestions(query))
        except Exception as e:
            self.logger.log_error(e, {"operation": "get_optimization_suggestions"})
            raise OptimizationError(f"Failed to get optimization suggestions: {str(e)}")
    
    def validate_optimization(
        self, 
        original_query: str, 
        optimized_query: str,
        sample_size: Optional[int] = 1000
    ) -> Dict[str, Any]:
        """Validate that an optimized query returns identical results."""
        if not self.validator:
            raise OptimizationError("Validator not initialized")
        
        try:
            return self.validator.comprehensive_validation(
                original_query, 
                optimized_query, 
                sample_size,
                self.settings.performance_threshold
            )
        except Exception as e:
            self.logger.log_error(e, {"operation": "validate_optimization"})
            raise OptimizationError(f"Failed to validate optimization: {str(e)}")
    
    def get_table_optimization_suggestions(
        self, 
        table_id: str, 
        sample_queries: Optional[List[str]] = None
    ) -> List[str]:
        """Get table-level optimization suggestions."""
        try:
            # Get table information
            table_info = self.bq_client.get_table_info(table_id)
            
            if "error" in table_info:
                raise OptimizationError(f"Failed to get table info: {table_info['error']}")
            
            # Use AI to suggest table optimizations
            if sample_queries:
                all_suggestions = []
                for query in sample_queries:
                    suggestions = self.ai_optimizer.suggest_table_optimizations(query, table_info)
                    all_suggestions.extend(suggestions)
                
                # Remove duplicates
                return list(set(all_suggestions))
            else:
                # Generic table optimization suggestions
                return self._generate_generic_table_suggestions(table_info)
                
        except Exception as e:
            self.logger.log_error(e, {"operation": "get_table_optimization_suggestions"})
            raise OptimizationError(f"Failed to get table suggestions: {str(e)}")
    
    def _generate_generic_table_suggestions(self, table_info: Dict[str, Any]) -> List[str]:
        """Generate generic table optimization suggestions."""
        suggestions = []
        
        # Check partitioning
        if not table_info["partitioning"]["type"]:
            suggestions.append("Consider partitioning this table by date/timestamp for better query performance")
        
        # Check clustering
        if not table_info["clustering"]["fields"]:
            suggestions.append("Consider adding clustering keys for frequently filtered columns")
        
        # Check table size
        if table_info["num_bytes"] and table_info["num_bytes"] > 1e9:  # > 1GB
            suggestions.append("Large table detected - ensure proper partitioning and clustering")
        
        return suggestions
    
    def batch_optimize_queries(
        self, 
        queries: List[str],
        validate_results: bool = True,
        max_concurrent: int = 3
    ) -> List[OptimizationResult]:
        """Optimize multiple queries in parallel."""
        
        async def optimize_batch():
            semaphore = asyncio.Semaphore(max_concurrent)
            
            async def optimize_single(query: str) -> OptimizationResult:
                async with semaphore:
                    # Run optimization in thread pool since it's not fully async
                    loop = asyncio.get_event_loop()
                    return await loop.run_in_executor(
                        None, 
                        self.optimize_query, 
                        query, 
                        validate_results, 
                        False  # Don't measure performance for batch
                    )
            
            tasks = [optimize_single(query) for query in queries]
            return await asyncio.gather(*tasks, return_exceptions=True)
        
        try:
            self.logger.logger.info(f"Starting batch optimization of {len(queries)} queries")
            results = asyncio.run(optimize_batch())
            
            # Handle any exceptions
            optimization_results = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    self.logger.log_error(result, {"operation": "batch_optimize", "query_index": i})
                    # Create a failed result
                    failed_result = OptimizationResult(
                        original_query=queries[i],
                        query_analysis=QueryAnalysis(
                            original_query=queries[i],
                            query_hash="batch_error",
                            complexity="simple",
                            table_count=0,
                            join_count=0,
                            subquery_count=0,
                            window_function_count=0,
                            aggregate_function_count=0,
                            potential_issues=[f"Batch optimization failed: {str(result)}"],
                            applicable_patterns=[]
                        ),
                        optimized_query=queries[i],
                        optimizations_applied=[],
                        total_optimizations=0,
                        validation_error=str(result)
                    )
                    optimization_results.append(failed_result)
                else:
                    optimization_results.append(result)
            
            self.logger.logger.info(f"Batch optimization completed: {len(optimization_results)} results")
            return optimization_results
            
        except Exception as e:
            self.logger.log_error(e, {"operation": "batch_optimize_queries"})
            raise OptimizationError(f"Batch optimization failed: {str(e)}")
    
    def test_connection(self) -> bool:
        """Test connections to all required services."""
        try:
            # Test BigQuery connection
            if not self.bq_client.test_connection():
                return False
            
            # Test documentation processor
            summary = self.documentation_processor.get_documentation_summary()
            if "error" in summary:
                return False
            
            # Test AI optimizer (simple test)
            # This would require an API call, so we'll just check if it's configured
            if not self.settings.gemini_api_key:
                return False
            
            return True
            
        except Exception as e:
            self.logger.log_error(e, {"operation": "test_connection"})
            return False
    
    def get_optimization_statistics(self) -> Dict[str, Any]:
        """Get statistics about available optimizations."""
        try:
            doc_summary = self.documentation_processor.get_documentation_summary()
            patterns = self.documentation_processor.optimization_patterns
            
            return {
                "available_patterns": len(patterns),
                "documentation_chunks": doc_summary.get("total_chunks", 0),
                "embedding_model": doc_summary.get("embedding_model"),
                "bigquery_project": self.bq_client.project_id,
                "patterns_by_type": {
                    pattern.optimization_type: [p.name for p in patterns if p.optimization_type == pattern.optimization_type]
                    for pattern in patterns
                }
            }
            
        except Exception as e:
            self.logger.log_error(e, {"operation": "get_optimization_statistics"})
            return {"error": str(e)}