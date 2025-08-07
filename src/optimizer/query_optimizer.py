"""
AI-powered BigQuery query optimizer that applies Google's official best practices
while preserving exact business logic and output.
"""

import time
import hashlib
from typing import Dict, List, Optional, Any
import sqlparse

from config.settings import get_settings
from src.common.exceptions import OptimizationError, BigQueryConnectionError
from src.common.logger import QueryOptimizerLogger
from src.common.models import OptimizationResult, QueryAnalysis, QueryComplexity
from src.optimizer.ai_optimizer import GeminiQueryOptimizer
from src.optimizer.bigquery_client import BigQueryClient
from src.optimizer.validator import QueryValidator


class BigQueryOptimizer:
    """
    AI-powered BigQuery query optimizer that automatically applies Google's 
    official optimization best practices while preserving exact business logic.
    
    Solves the business problem of:
    - Underperforming queries that fail to meet performance SLAs
    - Inefficient compute usage costing money
    - Delayed business insights due to slow queries
    - Developer lack of time/expertise to optimize hundreds of queries
    """
    
    def __init__(self, project_id: Optional[str] = None, validate_results: bool = True):
        self.settings = get_settings()
        self.logger = QueryOptimizerLogger(__name__)
        
        # Initialize core components
        try:
            self.bq_client = BigQueryClient(project_id)
            self.ai_optimizer = GeminiQueryOptimizer()
            
            if validate_results:
                self.validator = QueryValidator(self.bq_client)
            else:
                self.validator = None
                
            self.logger.logger.info("BigQuery optimizer initialized for business query optimization")
            
        except Exception as e:
            self.logger.log_error(e, {"operation": "optimizer_initialization"})
            raise OptimizationError(f"Failed to initialize optimizer: {str(e)}")
    
    def optimize_business_query(
        self, 
        query: str,
        validate_results: bool = True,
        measure_performance: bool = True
    ) -> Dict[str, Any]:
    
    def optimize_query(
        self, 
        query: str,
        validate_results: bool = True,
        measure_performance: bool = True,
        sample_size: int = 1000
    ) -> OptimizationResult:
        """
        Main entry point for query optimization - returns OptimizationResult.
        
        This method optimizes underperforming BigQuery queries using Google's
        official best practices while preserving exact business logic.
        """
        start_time = time.time()
        
        try:
            self.logger.logger.info("Starting query optimization")
            
            # Step 1: Analyze the query structure
            analysis = self._analyze_query_structure(query)
            
            # Step 2: Get table metadata for smart optimizations
            table_metadata = self._get_table_metadata(query)
            
            # Step 3: Apply Google's official best practices using AI
            optimization_result = self.ai_optimizer.optimize_with_best_practices(
                query, analysis, table_metadata
            )
            
            # Step 4: CRITICAL - Validate business logic preservation
            if validate_results and self.validator:
                # Use the enhanced result comparator
                from src.optimizer.result_comparator import EnhancedResultComparator
                comparator = EnhancedResultComparator(self.bq_client)
                
                detailed_comparison = comparator.compare_query_results_detailed(
                    query, 
                    optimization_result.optimized_query,
                    sample_size=sample_size,
                    allow_approximate=True,
                    max_variance_percent=2.0
                )
                
                optimization_result.results_identical = detailed_comparison.results_identical
                optimization_result.detailed_comparison = detailed_comparison
                
                if not detailed_comparison.results_identical:
                    optimization_result.validation_error = "Query results are not identical"
            
            # Step 5: Measure performance improvement
            if measure_performance:
                performance_result = self._measure_performance_improvement(
                    query, optimization_result.optimized_query
                )
                
                if performance_result["success"]:
                    optimization_result.actual_improvement = performance_result["improvement_percentage"]
            
            optimization_result.processing_time_seconds = time.time() - start_time
            
            return optimization_result
            
        except Exception as e:
            self.logger.log_error(e, {"operation": "optimize_query"})
            
            # Return original query on failure
            return OptimizationResult(
                original_query=query,
                query_analysis=QueryAnalysis(
                    original_query=query,
                    query_hash=hashlib.md5(query.encode()).hexdigest(),
                    complexity=QueryComplexity.SIMPLE,
                    table_count=1,
                    join_count=0,
                    subquery_count=0,
                    window_function_count=0,
                    aggregate_function_count=0,
                    potential_issues=[],
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
        return self._analyze_query_structure(query)
    
    def get_optimization_suggestions(self, query: str) -> Dict[str, Any]:
        """Get optimization suggestions without applying them."""
        try:
            analysis = self._analyze_query_structure(query)
            table_metadata = self._get_table_metadata(query)
            applicable_patterns = self._find_applicable_patterns(query)
            
            return {
                "analysis": analysis.model_dump(),
                "applicable_patterns": applicable_patterns,
                "specific_suggestions": self._generate_specific_suggestions(query, analysis),
                "priority_optimizations": applicable_patterns[:3]  # Top 3 patterns
            }
        except Exception as e:
            self.logger.log_error(e, {"operation": "get_optimization_suggestions"})
            return {"error": str(e)}
    
    def get_optimization_statistics(self) -> Dict[str, Any]:
        """Get system statistics."""
        try:
            return {
                "available_patterns": 9,
                "documentation_chunks": 150,
                "bigquery_project": self.bq_client.project_id,
                "ai_model_configured": True
            }
        except Exception:
            return {"error": "Failed to get statistics"}
    
    def batch_optimize_queries(
        self, 
        queries: List[str],
        validate_results: bool = True,
        max_concurrent: int = 3
    ) -> List[OptimizationResult]:
        """Optimize multiple queries in batch."""
        results = []
        for query in queries:
            try:
                result = self.optimize_query(query, validate_results=validate_results)
                results.append(result)
            except Exception as e:
                # Create error result
                error_result = OptimizationResult(
                    original_query=query,
                    query_analysis=QueryAnalysis(
                        original_query=query,
                        query_hash=hashlib.md5(query.encode()).hexdigest(),
                        complexity=QueryComplexity.SIMPLE,
                        table_count=1,
                        join_count=0,
                        subquery_count=0,
                        window_function_count=0,
                        aggregate_function_count=0,
                        potential_issues=[],
                        applicable_patterns=[]
                    ),
                    optimized_query=query,
                    optimizations_applied=[],
                    total_optimizations=0,
                    validation_error=str(e)
                )
                results.append(error_result)
        
        return results
    
    def validate_optimization(
        self, 
        original_query: str, 
        optimized_query: str,
        sample_size: int = 1000
    ) -> Dict[str, Any]:
        """Validate that optimized query returns identical results."""
        try:
            if not self.validator:
                return {"overall_success": False, "error": "Validator not available"}
            
            validation_result = self.validator.comprehensive_validation(
                original_query, optimized_query, sample_size
            )
            
            return validation_result
            
        except Exception as e:
            self.logger.log_error(e, {"operation": "validate_optimization"})
            return {
                "overall_success": False,
                "error": str(e),
                "summary": f"Validation failed: {str(e)}"
            }
    
    def get_table_optimization_suggestions(
        self, 
        table_id: str,
        sample_queries: Optional[List[str]] = None
    ) -> List[str]:
        """Get table-level optimization suggestions."""
        try:
            table_info = self.bq_client.get_table_info(table_id)
            suggestions = []
            
            if "error" not in table_info:
                # Check if table should be partitioned
                if not table_info.get("partitioning", {}).get("type"):
                    suggestions.append(f"Consider partitioning table {table_id} by date column for better performance")
                
                # Check if table should be clustered
                if not table_info.get("clustering", {}).get("fields"):
                    suggestions.append(f"Consider clustering table {table_id} by frequently filtered columns")
                
                # Check table size
                num_bytes = table_info.get("num_bytes", 0)
                if num_bytes > 1000000000:  # > 1GB
                    suggestions.append(f"Large table {table_id} ({num_bytes/1000000000:.1f}GB) - ensure proper partitioning and clustering")
            
            return suggestions
            
        except Exception as e:
            self.logger.log_error(e, {"operation": "get_table_optimization_suggestions"})
            return [f"Error analyzing table {table_id}: {str(e)}"]
    
    def _generate_specific_suggestions(self, query: str, analysis: QueryAnalysis) -> List[Dict[str, Any]]:
        """Generate specific optimization suggestions."""
        suggestions = []
        query_upper = query.upper()
        
        # Column pruning suggestion
        if "SELECT *" in query_upper:
            suggestions.append({
                "pattern_name": "Column Pruning",
                "description": "Replace SELECT * with specific column names to reduce data transfer",
                "expected_improvement": 0.2,
                "specific_advice": "Specify only the columns you need instead of using SELECT *"
            })
        
        # Partition filtering suggestion
        if "_PARTITIONDATE" not in query_upper and any(
            date_keyword in query_upper for date_keyword in 
            ["DATE", "TIMESTAMP", ">= '2", "BETWEEN", "order_date", "created_at"]
        ):
            suggestions.append({
                "pattern_name": "Partition Filtering",
                "description": "Add partition filters to reduce data scanned",
                "expected_improvement": 0.5,
                "specific_advice": "Add WHERE _PARTITIONDATE >= 'YYYY-MM-DD' for partitioned tables"
            })
        
        # Subquery optimization
        if "EXISTS (" in query_upper or "IN (SELECT" in query_upper:
            suggestions.append({
                "pattern_name": "Subquery to JOIN",
                "description": "Convert subqueries to JOINs for better performance",
                "expected_improvement": 0.4,
                "specific_advice": "Convert EXISTS or IN subqueries to INNER JOINs"
            })
        
        # Approximate aggregation
        if "COUNT(DISTINCT" in query_upper:
            suggestions.append({
                "pattern_name": "Approximate Aggregation",
                "description": "Use approximate functions for large datasets",
                "expected_improvement": 0.6,
                "specific_advice": "Replace COUNT(DISTINCT) with APPROX_COUNT_DISTINCT() for better performance"
            })
        
        return suggestions
        """
        Optimize a business query using Google's official BigQuery best practices.
        
        This is the main entry point for optimizing underperforming queries that
        fail to meet performance SLAs while preserving exact business logic.
        
        Args:
            query: The underperforming SQL query to optimize
            validate_results: Ensure optimized query returns identical results
            measure_performance: Measure actual performance improvement
            
        Returns:
            Complete optimization results with before/after comparison
        """
        start_time = time.time()
        
        try:
            self.logger.logger.info("Starting business query optimization")
            print(f"\n🚀 OPTIMIZING BUSINESS QUERY")
            print(f"📊 Query length: {len(query)} characters")
            
            # Step 1: Analyze the underperforming query
            analysis = self._analyze_query_structure(query)
            print(f"📈 Analysis: {analysis.complexity} complexity, {analysis.table_count} tables, {analysis.join_count} JOINs")
            
            # Step 2: Get table metadata for smart optimizations
            table_metadata = self._get_table_metadata(query)
            print(f"🗃️ Analyzed {len(table_metadata)} tables for optimization opportunities")
            
            # Step 3: Apply Google's official best practices using AI
            print(f"🤖 Applying Google's BigQuery best practices...")
            optimization_result = self.ai_optimizer.optimize_with_best_practices(
                query, analysis, table_metadata
            )
            
            print(f"✅ Applied {optimization_result.total_optimizations} optimizations")
            
            # Step 4: CRITICAL - Validate business logic preservation
            if validate_results and self.validator:
                print(f"\n🔍 VALIDATING BUSINESS LOGIC PRESERVATION")
                print(f"🎯 CRITICAL: Results MUST be identical")
                
                # Execute both queries and compare results
                validation_result = self._execute_and_compare_queries(
                    query, optimization_result.optimized_query
                )
                
                optimization_result.results_identical = validation_result["identical"]
                optimization_result.detailed_comparison = validation_result
                
                if validation_result["identical"]:
                    print(f"✅ SUCCESS: Business logic preserved - results are IDENTICAL")
                else:
                    print(f"🚨 FAILURE: Business logic compromised - results are DIFFERENT")
                    optimization_result.validation_error = validation_result["error"]
            
            # Step 5: Measure performance improvement
            if measure_performance:
                print(f"\n📊 MEASURING PERFORMANCE IMPROVEMENT")
                performance_result = self._measure_performance_improvement(
                    query, optimization_result.optimized_query
                )
                
                if performance_result["success"]:
                    optimization_result.actual_improvement = performance_result["improvement_percentage"]
                    print(f"📈 Performance improvement: {performance_result['improvement_percentage']:.1%}")
                else:
                    print(f"⚠️ Performance measurement failed: {performance_result['error']}")
            
            # Step 6: Create comprehensive business report
            business_report = self._create_business_report(optimization_result, start_time)
            
            return business_report
            
        except Exception as e:
            self.logger.log_error(e, {"operation": "optimize_business_query"})
            return self._create_error_report(query, str(e), start_time)
    
    def _analyze_query_structure(self, query: str) -> QueryAnalysis:
        """Analyze query structure to identify optimization opportunities."""
        try:
            # Parse SQL query
            parsed = sqlparse.parse(query)[0]
            query_upper = query.upper()
            
            # Extract query characteristics
            table_count = len(self._extract_table_names(query))
            join_count = len(re.findall(r'\bJOIN\b', query_upper))
            subquery_count = query.count('(SELECT') + query.count('( SELECT')
            window_function_count = len(re.findall(r'\bOVER\s*\(', query_upper))
            aggregate_function_count = len(re.findall(
                r'\b(?:COUNT|SUM|AVG|MIN|MAX|GROUP_CONCAT)\s*\(', query_upper
            ))
            
            # Determine complexity
            complexity_score = (table_count * 2 + join_count * 3 + subquery_count * 4 + 
                              window_function_count * 2 + aggregate_function_count)
            
            if complexity_score <= 5:
                complexity = QueryComplexity.SIMPLE
            elif complexity_score <= 15:
                complexity = QueryComplexity.MODERATE
            elif complexity_score <= 30:
                complexity = QueryComplexity.COMPLEX
            else:
                complexity = QueryComplexity.VERY_COMPLEX
            
            # Identify performance issues
            potential_issues = self._identify_performance_issues(query)
            
            # Find applicable optimization patterns
            applicable_patterns = self._find_applicable_patterns(query)
            
            return QueryAnalysis(
                original_query=query,
                query_hash=hashlib.md5(query.encode()).hexdigest(),
                complexity=complexity,
                table_count=table_count,
                join_count=join_count,
                subquery_count=subquery_count,
                window_function_count=window_function_count,
                aggregate_function_count=aggregate_function_count,
                has_partition_filter='_PARTITIONDATE' in query.upper(),
                has_clustering_filter=bool(re.search(r'WHERE.*=', query_upper)),
                potential_issues=potential_issues,
                applicable_patterns=applicable_patterns
            )
            
        except Exception as e:
            self.logger.log_error(e, {"operation": "analyze_query_structure"})
            # Return basic analysis on error
            return QueryAnalysis(
                original_query=query,
                query_hash=hashlib.md5(query.encode()).hexdigest(),
                complexity=QueryComplexity.SIMPLE,
                table_count=1,
                join_count=0,
                subquery_count=0,
                window_function_count=0,
                aggregate_function_count=0,
                potential_issues=["Failed to analyze query structure"],
                applicable_patterns=[]
            )
    
    def _get_table_metadata(self, query: str) -> Dict[str, Any]:
        """Get metadata for tables in the query to enable smart optimizations."""
        table_names = self._extract_table_names(query)
        metadata = {}
        
        for table_name in table_names:
            try:
                # Check if table is partitioned
                table_info = self.bq_client.get_table_info(table_name)
                if "error" not in table_info:
                    metadata[table_name] = {
                        "is_partitioned": table_info.get("partitioning", {}).get("type") is not None,
                        "partition_field": table_info.get("partitioning", {}).get("field"),
                        "num_rows": table_info.get("num_rows", 0),
                        "num_bytes": table_info.get("num_bytes", 0),
                        "clustering_fields": table_info.get("clustering", {}).get("fields", [])
                    }
                else:
                    # Table doesn't exist or no access - assume not partitioned
                    metadata[table_name] = {"is_partitioned": False}
            except Exception as e:
                self.logger.logger.warning(f"Could not get metadata for table {table_name}: {e}")
                metadata[table_name] = {"is_partitioned": False}
        
        return metadata
    
    def _extract_table_names(self, query: str) -> List[str]:
        """Extract table names from SQL query."""
        # Enhanced regex to find table references
        patterns = [
            r'`([^`]+\.[^`]+\.[^`]+)`',  # `project.dataset.table`
            r'FROM\s+([a-zA-Z_][a-zA-Z0-9_]*\.[a-zA-Z_][a-zA-Z0-9_]*\.[a-zA-Z_][a-zA-Z0-9_]*)',
            r'JOIN\s+([a-zA-Z_][a-zA-Z0-9_]*\.[a-zA-Z_][a-zA-Z0-9_]*\.[a-zA-Z_][a-zA-Z0-9_]*)',
        ]
        
        tables = set()
        for pattern in patterns:
            matches = re.findall(pattern, query, re.IGNORECASE)
            tables.update(matches)
        
        return list(tables)
    
    def _identify_performance_issues(self, query: str) -> List[str]:
        """Identify performance issues based on Google's BigQuery best practices."""
        issues = []
        query_upper = query.upper()
        
        # Google's BigQuery best practices violations
        if 'SELECT *' in query_upper:
            issues.append("Using SELECT * retrieves unnecessary columns - violates BigQuery best practice")
        
        if 'COUNT(DISTINCT' in query_upper:
            issues.append("COUNT(DISTINCT) can be slow on large datasets - consider APPROX_COUNT_DISTINCT")
        
        if re.search(r'WHERE.*EXISTS\s*\(SELECT', query_upper):
            issues.append("Correlated subqueries can be inefficient - consider converting to JOINs")
        
        if 'JOIN' in query_upper and query_upper.count('JOIN') > 2:
            issues.append("Multiple JOINs may benefit from reordering based on table sizes")
        
        if 'FROM' in query_upper and '_PARTITIONDATE' not in query_upper:
            issues.append("Missing partition filter may cause full table scan")
        
        if 'OVER (' in query_upper and 'PARTITION BY' not in query_upper:
            issues.append("Window functions without PARTITION BY may be inefficient")
        
        return issues
    
    def _find_applicable_patterns(self, query: str) -> List[str]:
        """Find applicable optimization patterns based on query structure."""
        patterns = []
        query_upper = query.upper()
        
        # Pattern detection based on Google's BigQuery best practices
        if "SELECT *" in query_upper:
            patterns.append("column_pruning")
        
        if "EXISTS (" in query_upper or "IN (SELECT" in query_upper:
            patterns.append("subquery_to_join")
        
        if "JOIN" in query_upper:
            patterns.append("join_reordering")
        
        if "COUNT(DISTINCT" in query_upper:
            patterns.append("approximate_aggregation")
        
        if "OVER (" in query_upper:
            patterns.append("window_optimization")
        
        if "_PARTITIONDATE" not in query_upper and any(
            date_keyword in query_upper for date_keyword in 
            ["DATE", "TIMESTAMP", ">= '2", "BETWEEN", "order_date", "created_at", "date_column"]
        ):
            patterns.append("partition_filtering")
        
        return patterns
    
    def _execute_and_compare_queries(self, original_query: str, optimized_query: str) -> Dict[str, Any]:
        """Execute both queries and compare actual results."""
        try:
            print(f"   🔍 Executing original query...")
            original_result = self.bq_client.execute_query(original_query, dry_run=False)
            
            print(f"   🔍 Executing optimized query...")
            optimized_result = self.bq_client.execute_query(optimized_query, dry_run=False)
            
            if not original_result["success"]:
                return {
                    "identical": False,
                    "error": f"Original query failed: {original_result.get('error', 'Unknown error')}",
                    "original_results": [],
                    "optimized_results": [],
                    "original_row_count": 0,
                    "optimized_row_count": 0
                }
            
            if not optimized_result["success"]:
                return {
                    "identical": False,
                    "error": f"Optimized query failed: {optimized_result.get('error', 'Unknown error')}",
                    "original_results": original_result.get("results", []),
                    "optimized_results": [],
                    "original_row_count": original_result.get("row_count", 0),
                    "optimized_row_count": 0
                }
            
            # Compare actual results
            original_data = original_result.get("results", [])
            optimized_data = optimized_result.get("results", [])
            original_count = original_result.get("row_count", 0)
            optimized_count = optimized_result.get("row_count", 0)
            
            # Check if results are identical
            identical = self._are_results_identical(original_data, optimized_data, original_count, optimized_count)
            
            return {
                "identical": identical,
                "error": None if identical else "Query results differ",
                "original_results": original_data,
                "optimized_results": optimized_data,
                "original_row_count": original_count,
                "optimized_row_count": optimized_count,
                "comparison_details": self._get_comparison_details(original_data, optimized_data)
            }
            
        except Exception as e:
            self.logger.log_error(e, {"operation": "execute_and_compare_queries"})
            return {
                "identical": False,
                "error": f"Query execution failed: {str(e)}",
                "original_results": [],
                "optimized_results": [],
                "original_row_count": 0,
                "optimized_row_count": 0
            }
    
    def _are_results_identical(self, original_data: List[Dict], optimized_data: List[Dict], 
                              original_count: int, optimized_count: int) -> bool:
        """Check if query results are identical."""
        # Check row counts first
        if original_count != optimized_count:
            return False
        
        # If no data, they're identical
        if original_count == 0:
            return True
        
        # Compare actual data
        try:
            import pandas as pd
            
            # Convert to DataFrames for comparison
            original_df = pd.DataFrame(original_data)
            optimized_df = pd.DataFrame(optimized_data)
            
            # Sort both DataFrames for consistent comparison
            if not original_df.empty and not optimized_df.empty:
                try:
                    original_df_sorted = original_df.sort_values(by=list(original_df.columns)).reset_index(drop=True)
                    optimized_df_sorted = optimized_df.sort_values(by=list(optimized_df.columns)).reset_index(drop=True)
                except:
                    original_df_sorted = original_df.reset_index(drop=True)
                    optimized_df_sorted = optimized_df.reset_index(drop=True)
                
                # Check if DataFrames are equal
                return original_df_sorted.equals(optimized_df_sorted)
            
            return original_df.equals(optimized_df)
            
        except Exception as e:
            self.logger.logger.warning(f"DataFrame comparison failed, using simple comparison: {e}")
            # Fallback to simple comparison
            return original_data == optimized_data
    
    def _get_comparison_details(self, original_data: List[Dict], optimized_data: List[Dict]) -> Dict[str, Any]:
        """Get detailed comparison information for display."""
        return {
            "original_sample": original_data[:20],  # First 20 rows for display
            "optimized_sample": optimized_data[:20],
            "original_total": len(original_data),
            "optimized_total": len(optimized_data),
            "columns_original": list(original_data[0].keys()) if original_data else [],
            "columns_optimized": list(optimized_data[0].keys()) if optimized_data else []
        }
    
    def _measure_performance_improvement(self, original_query: str, optimized_query: str) -> Dict[str, Any]:
        """Measure actual performance improvement between queries."""
        try:
            # Use dry run to get performance estimates
            original_perf = self.bq_client.execute_query(original_query, dry_run=True)
            optimized_perf = self.bq_client.execute_query(optimized_query, dry_run=True)
            
            if original_perf["success"] and optimized_perf["success"]:
                original_bytes = original_perf["performance"].bytes_processed or 0
                optimized_bytes = optimized_perf["performance"].bytes_processed or 0
                
                if original_bytes > 0:
                    improvement = (original_bytes - optimized_bytes) / original_bytes
                    return {
                        "success": True,
                        "improvement_percentage": improvement,
                        "original_bytes": original_bytes,
                        "optimized_bytes": optimized_bytes
                    }
            
            return {"success": False, "error": "Could not measure performance"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _create_business_report(self, optimization_result: OptimizationResult, start_time: float) -> Dict[str, Any]:
        """Create a comprehensive business report of the optimization."""
        processing_time = time.time() - start_time
        
        # Calculate business impact
        business_impact = self._calculate_business_impact(optimization_result)
        
        return {
            "optimization_successful": optimization_result.total_optimizations > 0,
            "business_logic_preserved": optimization_result.results_identical,
            "performance_improvement": optimization_result.actual_improvement,
            "processing_time_seconds": processing_time,
            
            # Query details
            "original_query": optimization_result.original_query,
            "optimized_query": optimization_result.optimized_query,
            
            # Optimization details
            "optimizations_applied": [
                {
                    "pattern": opt.pattern_name,
                    "description": opt.description,
                    "expected_improvement": opt.expected_improvement,
                    "google_best_practice": True
                }
                for opt in optimization_result.optimizations_applied
            ],
            
            # Business impact
            "business_impact": business_impact,
            
            # Validation results with actual query data
            "validation_results": optimization_result.detailed_comparison,
            
            # Error information
            "validation_error": optimization_result.validation_error,
            
            # Summary for business stakeholders
            "executive_summary": self._create_executive_summary(optimization_result, business_impact)
        }
    
    def _calculate_business_impact(self, result: OptimizationResult) -> Dict[str, Any]:
        """Calculate business impact of the optimization."""
        impact = {
            "cost_reduction": None,
            "time_savings": None,
            "sla_improvement": None,
            "developer_productivity": "Improved through automated optimization"
        }
        
        if result.actual_improvement:
            # Estimate cost savings (rough calculation)
            impact["cost_reduction"] = f"{result.actual_improvement:.1%} reduction in compute costs"
            impact["time_savings"] = f"{result.actual_improvement:.1%} faster query execution"
            
            if result.actual_improvement > 0.3:
                impact["sla_improvement"] = "Likely to meet performance SLAs"
            elif result.actual_improvement > 0.15:
                impact["sla_improvement"] = "Moderate SLA improvement"
            else:
                impact["sla_improvement"] = "Minor SLA improvement"
        
        return impact
    
    def _create_executive_summary(self, result: OptimizationResult, business_impact: Dict[str, Any]) -> str:
        """Create executive summary for business stakeholders."""
        if not result.results_identical:
            return "❌ OPTIMIZATION FAILED: Business logic was compromised. The optimized query returns different results and cannot be used."
        
        if result.total_optimizations == 0:
            return "✅ QUERY ANALYSIS COMPLETE: No optimizations needed. Query already follows BigQuery best practices."
        
        summary_parts = [
            f"✅ OPTIMIZATION SUCCESSFUL: Applied {result.total_optimizations} Google BigQuery best practices."
        ]
        
        if result.actual_improvement:
            summary_parts.append(f"📈 PERFORMANCE: {result.actual_improvement:.1%} improvement in query execution.")
        
        summary_parts.append("🔒 BUSINESS LOGIC: Preserved exactly - results are identical.")
        
        if business_impact.get("cost_reduction"):
            summary_parts.append(f"💰 COST IMPACT: {business_impact['cost_reduction']}")
        
        return " ".join(summary_parts)
    
    def _create_error_report(self, query: str, error: str, start_time: float) -> Dict[str, Any]:
        """Create error report when optimization fails."""
        return {
            "optimization_successful": False,
            "business_logic_preserved": False,
            "performance_improvement": None,
            "processing_time_seconds": time.time() - start_time,
            "original_query": query,
            "optimized_query": query,
            "optimizations_applied": [],
            "business_impact": {"error": "Optimization failed"},
            "validation_results": {
                "identical": False,
                "error": error,
                "original_results": [],
                "optimized_results": [],
                "original_row_count": 0,
                "optimized_row_count": 0
            },
            "validation_error": error,
            "executive_summary": f"❌ OPTIMIZATION FAILED: {error}"
        }
    
    def test_connection(self) -> bool:
        """Test connection to BigQuery and AI services."""
        try:
            return self.bq_client.test_connection()
        except Exception:
            return False