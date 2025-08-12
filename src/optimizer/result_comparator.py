"""Enhanced result comparator that shows both original and optimized query results."""

import json
import pandas as pd
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from src.common.logger import QueryOptimizerLogger
from src.optimizer.bigquery_client import BigQueryClient


@dataclass
class QueryResultComparison:
    """Detailed comparison of query results."""
    original_results: List[Dict[str, Any]]
    optimized_results: List[Dict[str, Any]]
    original_row_count: int
    optimized_row_count: int
    results_identical: bool
    differences_found: List[str]
    sample_original: List[Dict[str, Any]]
    sample_optimized: List[Dict[str, Any]]
    comparison_summary: str
    variance_percentage: Optional[float] = None
    approximate_functions_used: bool = False


class EnhancedResultComparator:
    """Enhanced result comparator with detailed result display."""
    
    def __init__(self, bigquery_client: BigQueryClient):
        self.bq_client = bigquery_client
        self.logger = QueryOptimizerLogger(__name__)
    
    def compare_query_results_detailed(
        self,
        original_query: str,
        optimized_query: str,
        sample_size: int = 1000,
        allow_approximate: bool = False,
        max_variance_percent: float = 2.0
    ) -> QueryResultComparison:
        """Compare query results with detailed analysis and display."""
        
        self.logger.logger.info("Starting detailed query result comparison")
        print(f"🔍 Executing original query...")
        
        # Execute both queries
        original_result = self._execute_with_sample(original_query, sample_size)
        print(f"✅ Original query executed: {original_result['success']}")
        if original_result["success"]:
            print(f"   📊 Original query returned {original_result['row_count']} rows")
        
        if not original_result["success"]:
            print(f"❌ Original query error: {original_result.get('error', 'Unknown')}")
        
        print(f"🔍 Executing optimized query...")
        optimized_result = self._execute_with_sample(optimized_query, sample_size)
        print(f"✅ Optimized query executed: {optimized_result['success']}")
        if optimized_result["success"]:
            print(f"   📊 Optimized query returned {optimized_result['row_count']} rows")
        
        if not optimized_result["success"]:
            print(f"❌ Optimized query error: {optimized_result.get('error', 'Unknown')}")
        
        if not original_result["success"] or not optimized_result["success"]:
            return QueryResultComparison(
                original_results=[],
                optimized_results=[],
                original_row_count=0,
                optimized_row_count=0,
                results_identical=False,
                differences_found=[
                    f"Query execution failed: Original: {original_result.get('error', 'Unknown')}, "
                    f"Optimized: {optimized_result.get('error', 'Unknown')}"
                ],
                sample_original=[],
                sample_optimized=[],
                comparison_summary="Query execution failed"
            )
        
        original_data = original_result["results"]
        optimized_data = optimized_result["results"]
        original_count = original_result["row_count"]
        optimized_count = optimized_result["row_count"]
        
        # Perform detailed comparison
        comparison_result = self._perform_detailed_comparison(
            original_data, optimized_data, original_count, optimized_count,
            allow_approximate, max_variance_percent
        )
        
        # Log comparison results
        self.logger.logger.info(
            "Query result comparison completed",
            original_rows=original_count,
            optimized_rows=optimized_count,
            results_identical=comparison_result.results_identical,
            differences_count=len(comparison_result.differences_found)
        )
        
        return comparison_result
    
    def _execute_with_sample(self, query: str, sample_size: int) -> Dict[str, Any]:
        """Execute query with sampling for comparison."""
        # Execute the full query without artificial limits
        # Only add LIMIT if the original query is very large (>10000 rows expected)
        sampled_query = query
        
        return self.bq_client.execute_query(sampled_query, dry_run=False)
    
    def _perform_detailed_comparison(
        self,
        original_data: List[Dict],
        optimized_data: List[Dict],
        original_count: int,
        optimized_count: int,
        allow_approximate: bool,
        max_variance_percent: float
    ) -> QueryResultComparison:
        """Perform detailed comparison of query results."""
        
        differences = []
        results_identical = True
        variance_percentage = None
        approximate_functions_used = False
        
        # Check row counts
        if original_count != optimized_count:
            differences.append(f"Row count mismatch: original={original_count}, optimized={optimized_count}")
            results_identical = False
        
        # If no data, return early
        if original_count == 0 and optimized_count == 0:
            return QueryResultComparison(
                original_results=original_data,
                optimized_results=optimized_data,
                original_row_count=original_count,
                optimized_row_count=optimized_count,
                results_identical=True,
                differences_found=[],
                sample_original=[],
                sample_optimized=[],
                comparison_summary="Both queries returned no results - identical"
            )
        
        # Convert to DataFrames for easier comparison
        try:
            if original_data and optimized_data:
                original_df = pd.DataFrame(original_data)
                optimized_df = pd.DataFrame(optimized_data)
                
                # Check column structure
                if list(original_df.columns) != list(optimized_df.columns):
                    differences.append(f"Column structure differs: original={list(original_df.columns)}, optimized={list(optimized_df.columns)}")
                    results_identical = False
                
                # Detailed value comparison
                if original_df.shape == optimized_df.shape and list(original_df.columns) == list(optimized_df.columns):
                    value_differences = self._compare_dataframe_values(
                        original_df, optimized_df, allow_approximate, max_variance_percent
                    )
                    differences.extend(value_differences["differences"])
                    if value_differences["differences"]:
                        results_identical = False
                    variance_percentage = value_differences.get("variance_percentage")
                    approximate_functions_used = value_differences.get("approximate_detected", False)
        
        except Exception as e:
            differences.append(f"Comparison error: {str(e)}")
            results_identical = False
        
        # Create samples for display
        # Show ALL results, not just a sample
        sample_original = original_data if original_data else []
        sample_optimized = optimized_data if optimized_data else []
        
        # Generate summary
        if results_identical:
            summary = f"✅ Results are identical ({original_count} rows)"
        elif allow_approximate and variance_percentage and variance_percentage <= max_variance_percent:
            summary = f"✅ Results are approximately identical (variance: {variance_percentage:.2f}%)"
            results_identical = True  # Accept as identical for approximate functions
        else:
            summary = f"❌ Results differ ({len(differences)} differences found)"
        
        return QueryResultComparison(
            original_results=original_data,
            optimized_results=optimized_data,
            original_row_count=original_count,
            optimized_row_count=optimized_count,
            results_identical=results_identical,
            differences_found=differences,
            sample_original=sample_original,
            sample_optimized=sample_optimized,
            comparison_summary=summary,
            variance_percentage=variance_percentage,
            approximate_functions_used=approximate_functions_used
        )
    
    def _compare_dataframe_values(
        self,
        df1: pd.DataFrame,
        df2: pd.DataFrame,
        allow_approximate: bool,
        max_variance_percent: float
    ) -> Dict[str, Any]:
        """Compare DataFrame values with support for approximate functions."""
        
        differences = []
        variance_percentage = None
        approximate_detected = False
        
        # Sort both DataFrames for consistent comparison
        try:
            # Try to sort by all columns
            df1_sorted = df1.sort_values(by=list(df1.columns)).reset_index(drop=True)
            df2_sorted = df2.sort_values(by=list(df2.columns)).reset_index(drop=True)
        except (TypeError, ValueError):
            # If sorting fails, use original order
            df1_sorted = df1.reset_index(drop=True)
            df2_sorted = df2.reset_index(drop=True)
        
        # Compare each column
        for col in df1_sorted.columns:
            if col not in df2_sorted.columns:
                differences.append(f"Column '{col}' missing in optimized results")
                continue
            
            col1_data = df1_sorted[col]
            col2_data = df2_sorted[col]
            
            # Check for numeric columns that might use approximate functions
            if pd.api.types.is_numeric_dtype(col1_data) and pd.api.types.is_numeric_dtype(col2_data):
                if allow_approximate:
                    # Calculate percentage difference for numeric columns
                    non_zero_mask = col1_data != 0
                    if non_zero_mask.any():
                        percentage_diff = abs((col1_data[non_zero_mask] - col2_data[non_zero_mask]) / col1_data[non_zero_mask] * 100)
                        max_diff = percentage_diff.max()
                        
                        if max_diff > max_variance_percent:
                            differences.append(f"Column '{col}' variance {max_diff:.2f}% exceeds threshold {max_variance_percent}%")
                        else:
                            approximate_detected = True
                            variance_percentage = max_diff
                    else:
                        # Handle zero values
                        if not col1_data.equals(col2_data):
                            differences.append(f"Column '{col}' values differ (zero values)")
                else:
                    # Exact comparison for numeric data
                    if not col1_data.equals(col2_data):
                        differences.append(f"Column '{col}' numeric values differ")
            else:
                # Exact comparison for non-numeric data
                if not col1_data.equals(col2_data):
                    differences.append(f"Column '{col}' values differ")
        
        return {
            "differences": differences,
            "variance_percentage": variance_percentage,
            "approximate_detected": approximate_detected
        }
    
    def display_comparison_results(self, comparison: QueryResultComparison) -> str:
        """Generate a formatted display of comparison results."""
        
        output = []
        output.append("\n" + "=" * 100)
        output.append("🔍 ACTUAL QUERY EXECUTION RESULTS - BUSINESS LOGIC VALIDATION")
        output.append("=" * 100)
        
        # Summary
        if comparison.results_identical:
            output.append(f"\n✅ SUCCESS: BUSINESS LOGIC PRESERVED!")
            output.append(f"   {comparison.comparison_summary}")
            output.append(f"   🎯 Both queries return IDENTICAL results!")
            output.append(f"   ✅ Optimization is VALID and APPROVED!")
        else:
            output.append(f"\n🚨 CRITICAL FAILURE: BUSINESS LOGIC COMPROMISED!")
            output.append(f"   {comparison.comparison_summary}")
            output.append("   ⚠️  THE OPTIMIZED QUERY RETURNS DIFFERENT RESULTS!")
            output.append("   ⚠️  THIS OPTIMIZATION IS INVALID AND MUST BE REJECTED!")
            
        output.append(f"   Original rows: {comparison.original_row_count:,}")
        output.append(f"   Optimized rows: {comparison.optimized_row_count:,}")
        
        if comparison.variance_percentage is not None:
            output.append(f"   Variance: {comparison.variance_percentage:.3f}%")
        
        if comparison.approximate_functions_used:
            output.append("   ⚠️  Approximate functions detected - slight variance expected")
        
        # Differences
        if comparison.differences_found:
            output.append(f"\n🚨 CRITICAL DIFFERENCES FOUND ({len(comparison.differences_found)}):")
            for i, diff in enumerate(comparison.differences_found, 1):
                output.append(f"   🔴 {i}. {diff}")
        else:
            output.append("\n✅ NO DIFFERENCES FOUND")
        
        # ALWAYS show both query results side by side with actual data
        output.append(f"\n📊 COMPLETE QUERY RESULTS COMPARISON (showing ALL {comparison.original_row_count} rows):")
        output.append("-" * 100)
        
        # Show original results
        output.append("\n🔵 ORIGINAL QUERY RESULTS:")
        if comparison.sample_original:
            output.append(self._format_sample_data_detailed(comparison.sample_original, max_rows=comparison.original_row_count))
        else:
            output.append("   No data returned")
        
        # Show optimized results  
        output.append("\n🟢 OPTIMIZED QUERY RESULTS:")
        if comparison.sample_optimized:
            output.append(self._format_sample_data_detailed(comparison.sample_optimized, max_rows=comparison.optimized_row_count))
        else:
            output.append("   No data returned")
        
        # Add explicit comparison verification
        if comparison.results_identical:
            output.append("\n✅ VERIFICATION: Both queries return IDENTICAL results!")
            output.append("   ✅ Business logic is PRESERVED - optimization is VALID!")
            output.append("   ✅ The optimization improves performance without changing results!")
        else:
            output.append("\n🚨 VERIFICATION: Queries return DIFFERENT results!")
            output.append("   🚨 Business logic has been CHANGED - optimization is INVALID!")
            output.append("   🚨 This optimization MUST BE REJECTED!")
        
        output.append("\n" + "=" * 100)
        
        return "\n".join(output)
    
    def _format_sample_data_detailed(self, data: List[Dict[str, Any]], max_rows: int = 20) -> str:
        """Format sample data with detailed table structure."""
        if not data:
            return "   No data"
        
        # Show all data, not just a sample
        actual_max_rows = min(max_rows, len(data)) if max_rows > 0 else len(data)
        
        try:
            # Get headers
            headers = list(data[0].keys())
            
            # Calculate column widths
            col_widths = {}
            for header in headers:
                col_widths[header] = max(
                    len(header),
                    max(len(str(row.get(header, ''))) for row in data[:actual_max_rows])
                )
                col_widths[header] = min(col_widths[header], 25)  # Max width
            
            # Create table header
            output = []
            header_line = "   " + " | ".join(header.ljust(col_widths[header]) for header in headers)
            output.append(header_line)
            
            # Create separator
            separator = "   " + "-+-".join("-" * col_widths[header] for header in headers)
            output.append(separator)
            
            # Add data rows
            for i, row in enumerate(data[:actual_max_rows]):
                values = []
                for header in headers:
                    value = row.get(header)
                    if value is None:
                        display_value = "NULL"
                    elif isinstance(value, (int, float)):
                        display_value = str(value)
                    else:
                        display_value = str(value)
                    
                    # Truncate if too long
                    if len(display_value) > col_widths[header]:
                        display_value = display_value[:col_widths[header]-3] + "..."
                    
                    values.append(display_value.ljust(col_widths[header]))
                
                row_line = "   " + " | ".join(values)
                output.append(row_line)
            
            if len(data) > actual_max_rows:
                output.append(f"   ... and {len(data) - actual_max_rows} more rows")
            
            return '\n'.join(output)
            
        except Exception as e:
            # Fallback to simple format
            output = []
            for i, row in enumerate(data[:actual_max_rows]):
                output.append(f"   Row {i+1}: {row}")
            if len(data) > actual_max_rows:
                output.append(f"   ... and {len(data) - actual_max_rows} more rows")
            return '\n'.join(output)
    
    def _format_sample_data(self, data: List[Dict[str, Any]], max_rows: int = 5) -> str:
        """Format sample data for display (legacy method)."""
        return self._format_sample_data_detailed(data, max_rows)
    
    def save_comparison_report(
        self, 
        comparison: QueryResultComparison,
        original_query: str,
        optimized_query: str,
        output_file: str
    ) -> None:
        """Save detailed comparison report to file."""
        
        report = {
            "timestamp": pd.Timestamp.now().isoformat(),
            "queries": {
                "original": original_query,
                "optimized": optimized_query
            },
            "comparison_results": {
                "results_identical": comparison.results_identical,
                "original_row_count": comparison.original_row_count,
                "optimized_row_count": comparison.optimized_row_count,
                "differences_found": comparison.differences_found,
                "variance_percentage": comparison.variance_percentage,
                "approximate_functions_used": comparison.approximate_functions_used,
                "summary": comparison.comparison_summary
            },
            "sample_data": {
                "original": comparison.sample_original,
                "optimized": comparison.sample_optimized
            }
        }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        self.logger.logger.info(f"Comparison report saved to {output_file}")