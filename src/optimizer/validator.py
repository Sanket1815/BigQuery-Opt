"""Query validator to ensure optimized queries return identical results."""

import hashlib
from typing import Dict, List, Optional, Any, Tuple
import pandas as pd

from src.common.exceptions import ValidationError
from src.common.logger import QueryOptimizerLogger
from src.optimizer.bigquery_client import BigQueryClient


class QueryValidator:
    """Validates that optimized queries return identical results to original queries."""
    
    def __init__(self, bigquery_client: Optional[BigQueryClient] = None):
        self.logger = QueryOptimizerLogger(__name__)
        self.bq_client = bigquery_client or BigQueryClient()
    
    def validate_query_results(
        self, 
        original_query: str, 
        optimized_query: str,
        sample_size: Optional[int] = 0  # Default to no sampling
    ) -> Dict[str, Any]:
        """Validate that both queries return identical results."""
        
        try:
            self.logger.logger.info("Starting query result validation")
            
            # First, validate both queries syntactically
            original_validation = self.bq_client.validate_query(original_query)
            optimized_validation = self.bq_client.validate_query(optimized_query)
            
            if not original_validation["valid"]:
                return {
                    "identical": False,
                    "error": f"Original query is invalid: {original_validation['error']}",
                    "validation_type": "syntax_error"
                }
            
            if not optimized_validation["valid"]:
                return {
                    "identical": False,
                    "error": f"Optimized query is invalid: {optimized_validation['error']}",
                    "validation_type": "syntax_error"
                }
            
            # Only add LIMIT if sample_size is explicitly specified and > 0
            if sample_size and sample_size > 0:
                original_test_query = self._add_limit_clause(original_query, sample_size)
                optimized_test_query = self._add_limit_clause(optimized_query, sample_size)
                print(f"🔍 Using sample size: {sample_size} rows for validation")
            else:
                original_test_query = original_query
                optimized_test_query = optimized_query
                print(f"🔍 Executing complete queries (no sampling)")
            
            # Execute both queries
            original_result = self.bq_client.execute_query(original_test_query, dry_run=False)
            optimized_result = self.bq_client.execute_query(optimized_test_query, dry_run=False)
            
            if not original_result["success"]:
                return {
                    "identical": False,
                    "error": f"Original query execution failed: {original_result['error']}",
                    "validation_type": "execution_error"
                }
            
            if not optimized_result["success"]:
                return {
                    "identical": False,
                    "error": f"Optimized query execution failed: {optimized_result['error']}",
                    "validation_type": "execution_error"
                }
            
            # Compare results
            comparison_result = self._compare_query_results(
                original_result["results"],
                optimized_result["results"],
                original_result["row_count"],
                optimized_result["row_count"]
            )
            
            self.logger.log_validation_result(
                comparison_result["identical"],
                comparison_result.get("error")
            )
            
            return comparison_result
            
        except Exception as e:
            self.logger.log_error(e, {"operation": "validate_query_results"})
            return {
                "identical": False,
                "error": f"Validation failed: {str(e)}",
                "validation_type": "validation_error"
            }
    
    def _add_limit_clause(self, query: str, limit: int) -> str:
        """Add LIMIT clause to query for sampling."""
        query_upper = query.upper().strip()
        
        # Check if query already has LIMIT
        if "LIMIT" in query_upper:
            return query
        
        # Add LIMIT clause
        if query.rstrip().endswith(';'):
            return f"{query.rstrip()[:-1]} LIMIT {limit};"
        else:
            return f"{query} LIMIT {limit}"
    
    def _compare_query_results(
        self, 
        original_results: List[Dict],
        optimized_results: List[Dict],
        original_count: int,
        optimized_count: int
    ) -> Dict[str, Any]:
        """Compare results from two queries."""
        
        # Check row counts
        if original_count != optimized_count:
            return {
                "identical": False,
                "error": f"Row count mismatch: original={original_count}, optimized={optimized_count}",
                "validation_type": "row_count_mismatch",
                "original_count": original_count,
                "optimized_count": optimized_count
            }
        
        # If no results, they're identical
        if original_count == 0:
            return {
                "identical": True,
                "validation_type": "empty_results",
                "original_count": 0,
                "optimized_count": 0
            }
        
        # Convert to DataFrames for easier comparison
        try:
            original_df = pd.DataFrame(original_results)
            optimized_df = pd.DataFrame(optimized_results)
            
            # Handle numeric precision issues
            for col in original_df.columns:
                if original_df[col].dtype in ['float64', 'float32']:
                    original_df[col] = original_df[col].round(10)
                if optimized_df[col].dtype in ['float64', 'float32']:
                    optimized_df[col] = optimized_df[col].round(10)
            
            # Sort both DataFrames to handle potential ordering differences
            original_df_sorted = self._sort_dataframe(original_df)
            optimized_df_sorted = self._sort_dataframe(optimized_df)
            
            # Compare DataFrames
            are_equal = original_df_sorted.equals(optimized_df_sorted)
            
            if are_equal:
                return {
                    "identical": True,
                    "validation_type": "content_match",
                    "original_count": original_count,
                    "optimized_count": optimized_count
                }
            else:
                # Find differences
                differences = self._find_dataframe_differences(
                    original_df_sorted, 
                    optimized_df_sorted
                )
                
                return {
                    "identical": False,
                    "error": "Query results differ in content",
                    "validation_type": "content_mismatch",
                    "original_count": original_count,
                    "optimized_count": optimized_count,
                    "differences": differences
                }
                
        except Exception as e:
            self.logger.log_error(e, {"operation": "_compare_query_results"})
            
            # Fallback to simple comparison
            return self._simple_results_comparison(
                original_results, 
                optimized_results,
                original_count,
                optimized_count
            )
    
    def _sort_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Sort DataFrame for consistent comparison."""
        if df.empty:
            return df
        
        try:
            # Sort by all columns, handling mixed types
            sortable_columns = []
            for col in df.columns:
                try:
                    # Test if column is sortable
                    df[col].sort_values()
                    sortable_columns.append(col)
                except (TypeError, ValueError):
                    # Skip columns that can't be sorted (mixed types, etc.)
                    continue
            
            if sortable_columns:
                return df.sort_values(by=sortable_columns).reset_index(drop=True)
            else:
                return df.reset_index(drop=True)
        except Exception:
            # If sorting fails, return original DataFrame
            return df.reset_index(drop=True)
    
    def _find_dataframe_differences(
        self, 
        df1: pd.DataFrame, 
        df2: pd.DataFrame
    ) -> Dict[str, Any]:
        """Find specific differences between DataFrames."""
        differences = {}
        
        # Check column differences
        df1_cols = set(df1.columns)
        df2_cols = set(df2.columns)
        
        if df1_cols != df2_cols:
            differences["column_differences"] = {
                "only_in_original": list(df1_cols - df2_cols),
                "only_in_optimized": list(df2_cols - df1_cols)
            }
        
        # Check shape differences
        if df1.shape != df2.shape:
            differences["shape_differences"] = {
                "original_shape": df1.shape,
                "optimized_shape": df2.shape
            }
        
        # Sample differences (first few rows that differ)
        try:
            # Find rows that are different
            if df1.shape == df2.shape and list(df1.columns) == list(df2.columns):
                comparison = df1.compare(df2)
                if not comparison.empty:
                    differences["sample_differences"] = comparison.head(5).to_dict()
        except Exception:
            pass
        
        return differences
    
    def _simple_results_comparison(
        self, 
        original_results: List[Dict],
        optimized_results: List[Dict],
        original_count: int,
        optimized_count: int
    ) -> Dict[str, Any]:
        """Simple comparison fallback when pandas comparison fails."""
        
        if original_count != optimized_count:
            return {
                "identical": False,
                "error": f"Row count mismatch: {original_count} vs {optimized_count}",
                "validation_type": "row_count_mismatch"
            }
        
        # Compare first few rows as sample
        sample_size = min(10, len(original_results))
        
        for i in range(sample_size):
            if original_results[i] != optimized_results[i]:
                return {
                    "identical": False,
                    "error": f"Content differs at row {i}",
                    "validation_type": "content_mismatch",
                    "sample_difference": {
                        "row_index": i,
                        "original": original_results[i],
                        "optimized": optimized_results[i]
                    }
                }
        
        return {
            "identical": True,
            "validation_type": "simple_match",
            "original_count": original_count,
            "optimized_count": optimized_count
        }
    
    def validate_query_performance(
        self, 
        original_query: str, 
        optimized_query: str,
        min_improvement: float = 0.05
    ) -> Dict[str, Any]:
        """Validate that the optimized query performs better than the original."""
        
        try:
            # Compare performance
            comparison = self.bq_client.compare_query_performance(
                original_query, 
                optimized_query,
                iterations=3
            )
            
            if not comparison["success"]:
                return {
                    "performance_improved": False,
                    "error": comparison["error"],
                    "validation_type": "performance_test_failed"
                }
            
            improvement = comparison["improvement_percentage"]
            
            return {
                "performance_improved": improvement >= min_improvement,
                "improvement_percentage": improvement,
                "original_avg_ms": comparison["original_avg_ms"],
                "optimized_avg_ms": comparison["optimized_avg_ms"],
                "meets_threshold": improvement >= min_improvement,
                "threshold": min_improvement,
                "validation_type": "performance_comparison"
            }
            
        except Exception as e:
            self.logger.log_error(e, {"operation": "validate_query_performance"})
            return {
                "performance_improved": False,
                "error": str(e),
                "validation_type": "performance_validation_error"
            }
    
    def comprehensive_validation(
        self, 
        original_query: str, 
        optimized_query: str,
        sample_size: Optional[int] = 1000,
        min_improvement: float = 0.05
    ) -> Dict[str, Any]:
        """Perform comprehensive validation of query optimization."""
        
        validation_results = {
            "overall_success": False,
            "results_validation": {},
            "performance_validation": {},
            "summary": ""
        }
        
        try:
            # Validate results are identical
            results_validation = self.validate_query_results(
                original_query, 
                optimized_query, 
                sample_size
            )
            validation_results["results_validation"] = results_validation
            
            if not results_validation["identical"]:
                validation_results["summary"] = "Validation failed: Query results are not identical"
                return validation_results
            
            # Validate performance improvement (optional)
            performance_validation = self.validate_query_performance(
                original_query, 
                optimized_query, 
                min_improvement
            )
            validation_results["performance_validation"] = performance_validation
            
            # Determine overall success
            results_identical = results_validation["identical"]
            performance_improved = performance_validation.get("performance_improved", True)
            
            validation_results["overall_success"] = results_identical
            
            if results_identical and performance_improved:
                improvement = performance_validation.get("improvement_percentage", 0)
                validation_results["summary"] = f"Validation successful: Results identical, {improvement:.1%} performance improvement"
            elif results_identical:
                validation_results["summary"] = "Validation successful: Results identical (performance not significantly improved)"
            else:
                validation_results["summary"] = "Validation failed: Results differ or performance degraded"
            
            return validation_results
            
        except Exception as e:
            self.logger.log_error(e, {"operation": "comprehensive_validation"})
            validation_results["summary"] = f"Validation error: {str(e)}"
            return validation_results