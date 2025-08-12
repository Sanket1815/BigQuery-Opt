"""Data models for BigQuery Query Optimizer."""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class OptimizationType(str, Enum):
    """Types of optimizations that can be applied."""
    JOIN_REORDERING = "join_reordering"
    PARTITION_FILTERING = "partition_filtering"
    SUBQUERY_CONVERSION = "subquery_conversion"
    WINDOW_OPTIMIZATION = "window_optimization"
    AGGREGATION_OPTIMIZATION = "aggregation_optimization"
    COLUMN_PRUNING = "column_pruning"
    CLUSTERING_RECOMMENDATION = "clustering_recommendation"
    PREDICATE_PUSHDOWN = "predicate_pushdown"
    APPROXIMATE_AGGREGATION = "approximate_aggregation"
    MATERIALIZED_VIEW_SUGGESTION = "materialized_view_suggestion"


class QueryComplexity(str, Enum):
    """Query complexity levels."""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    VERY_COMPLEX = "very_complex"


class OptimizationPattern(BaseModel):
    """Represents a specific optimization pattern."""
    
    pattern_id: str = Field(description="Unique identifier for the pattern")
    name: str = Field(description="Human-readable name of the pattern")
    description: str = Field(description="Description of what this pattern does")
    optimization_type: OptimizationType = Field(description="Type of optimization")
    documentation_url: Optional[str] = Field(
        default=None, 
        description="URL to BigQuery documentation"
    )
    expected_improvement: Optional[float] = Field(
        default=None,
        description="Expected performance improvement (0.0 to 1.0)"
    )
    applicability_conditions: List[str] = Field(
        default_factory=list,
        description="Conditions when this pattern applies"
    )
    sql_pattern: Optional[str] = Field(
        default=None,
        description="SQL pattern that triggers this optimization"
    )
    replacement_pattern: Optional[str] = Field(
        default=None,
        description="SQL replacement pattern"
    )


class QueryAnalysis(BaseModel):
    """Analysis results for a BigQuery SQL query."""
    
    original_query: str = Field(description="Original SQL query")
    query_hash: str = Field(description="Hash of the original query")
    complexity: QueryComplexity = Field(description="Query complexity level")
    
    # Query structure analysis
    table_count: int = Field(description="Number of tables referenced")
    join_count: int = Field(description="Number of JOIN operations")
    subquery_count: int = Field(description="Number of subqueries")
    window_function_count: int = Field(description="Number of window functions")
    aggregate_function_count: int = Field(description="Number of aggregate functions")
    
    # Performance indicators
    estimated_bytes_processed: Optional[int] = Field(
        default=None,
        description="Estimated bytes to be processed"
    )
    estimated_slots: Optional[int] = Field(
        default=None,
        description="Estimated slots required"
    )
    has_partition_filter: bool = Field(
        default=False,
        description="Whether query includes partition filtering"
    )
    has_clustering_filter: bool = Field(
        default=False,
        description="Whether query includes clustering filtering"
    )
    
    # Identified issues
    potential_issues: List[str] = Field(
        default_factory=list,
        description="List of potential performance issues"
    )
    applicable_patterns: List[str] = Field(
        default_factory=list,
        description="List of applicable optimization pattern IDs"
    )
    
    # Metadata
    analyzed_at: datetime = Field(default_factory=datetime.utcnow)


class AppliedOptimization(BaseModel):
    """Details of an optimization that was applied."""
    
    pattern_id: str = Field(description="ID of the optimization pattern applied")
    pattern_name: str = Field(description="Name of the optimization pattern")
    description: str = Field(description="Description of what was changed")
    before_snippet: str = Field(description="SQL snippet before optimization")
    after_snippet: str = Field(description="SQL snippet after optimization")
    documentation_reference: Optional[str] = Field(
        default=None,
        description="Reference to BigQuery documentation"
    )
    expected_improvement: Optional[float] = Field(
        default=None,
        description="Expected performance improvement"
    )
    confidence_score: float = Field(
        default=1.0,
        description="Confidence in this optimization (0.0 to 1.0)"
    )


class PerformanceMetrics(BaseModel):
    """Performance metrics for query execution."""
    
    execution_time_ms: Optional[int] = Field(
        default=None,
        description="Query execution time in milliseconds"
    )
    bytes_processed: Optional[int] = Field(
        default=None,
        description="Actual bytes processed"
    )
    bytes_billed: Optional[int] = Field(
        default=None,
        description="Bytes billed for the query"
    )
    slot_time_ms: Optional[int] = Field(
        default=None,
        description="Total slot time in milliseconds"
    )
    total_slots: Optional[int] = Field(
        default=None,
        description="Total slots used"
    )
    cache_hit: Optional[bool] = Field(
        default=None,
        description="Whether query result was served from cache"
    )
    creation_time: datetime = Field(default_factory=datetime.utcnow)


class OptimizationResult(BaseModel):
    """Complete result of query optimization process."""
    
    # Input
    original_query: str = Field(description="Original SQL query")
    query_analysis: QueryAnalysis = Field(description="Analysis of original query")
    
    # Output
    optimized_query: str = Field(description="Optimized SQL query")
    optimizations_applied: List[AppliedOptimization] = Field(
        description="List of optimizations that were applied"
    )
    
    # Performance comparison
    original_performance: Optional[PerformanceMetrics] = Field(
        default=None,
        description="Performance metrics of original query"
    )
    optimized_performance: Optional[PerformanceMetrics] = Field(
        default=None,
        description="Performance metrics of optimized query"
    )
    
    # Summary
    total_optimizations: int = Field(description="Number of optimizations applied")
    estimated_improvement: Optional[float] = Field(
        default=None,
        description="Estimated overall performance improvement"
    )
    actual_improvement: Optional[float] = Field(
        default=None,
        description="Actual measured performance improvement"
    )
    
    # Validation
    results_identical: Optional[bool] = Field(
        default=None,
        description="Whether original and optimized queries return identical results"
    )
    validation_error: Optional[str] = Field(
        default=None,
        description="Error message if validation failed"
    )
    
    # Metadata
    optimization_timestamp: datetime = Field(default_factory=datetime.utcnow)
    processing_time_seconds: Optional[float] = Field(
        default=None,
        description="Time taken to perform optimization"
    )
    
    # Enhanced result comparison
    detailed_comparison: Optional[Any] = Field(
        default=None,
        description="Detailed comparison results (QueryResultComparison object)"
    )
    
    # Query execution results for display
    original_query_results: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="Results from executing the original query"
    )
    optimized_query_results: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="Results from executing the optimized query"
    )
    original_row_count: Optional[int] = Field(
        default=None,
        description="Number of rows returned by original query"
    )
    optimized_row_count: Optional[int] = Field(
        default=None,
        description="Number of rows returned by optimized query"
    )
    query_execution_error: Optional[str] = Field(
        default=None,
        description="Error message if query execution failed"
    )
    
    # Performance comparison metrics
    original_execution_time_ms: Optional[int] = Field(
        default=None,
        description="Execution time of original query in milliseconds"
    )
    optimized_execution_time_ms: Optional[int] = Field(
        default=None,
        description="Execution time of optimized query in milliseconds"
    )
    original_bytes_processed: Optional[int] = Field(
        default=None,
        description="Bytes processed by original query"
    )
    optimized_bytes_processed: Optional[int] = Field(
        default=None,
        description="Bytes processed by optimized query"
    )
    performance_improvement_ms: Optional[int] = Field(
        default=None,
        description="Time saved in milliseconds"
    )
    bytes_saved: Optional[int] = Field(
        default=None,
        description="Bytes saved by optimization"
    )
    cost_savings_usd: Optional[float] = Field(
        default=None,
        description="Estimated cost savings in USD"
    )
    
    def get_summary(self) -> str:
        """Get a human-readable summary of the optimization."""
        if not self.optimizations_applied:
            return "No optimizations were applied to this query."
        
        summary_parts = [
            f"Applied {self.total_optimizations} optimization(s):",
        ]
        
        for opt in self.optimizations_applied:
            improvement = ""
            if opt.expected_improvement:
                improvement = f" (expected {opt.expected_improvement:.1%} improvement)"
            summary_parts.append(f"• {opt.pattern_name}: {opt.description}{improvement}")
        
        if self.estimated_improvement:
            summary_parts.append(
                f"\nEstimated overall improvement: {self.estimated_improvement:.1%}"
            )
        
        if self.actual_improvement:
            summary_parts.append(
                f"Actual measured improvement: {self.actual_improvement:.1%}"
            )
        
        return "\n".join(summary_parts)


class DocumentationSection(BaseModel):
    """Represents a section of BigQuery documentation."""
    
    title: str = Field(description="Section title")
    url: str = Field(description="URL of the documentation page")
    content: str = Field(description="Text content of the section")
    optimization_patterns: List[str] = Field(
        default_factory=list,
        description="Optimization patterns mentioned in this section"
    )
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    
    
class MCPRequest(BaseModel):
    """Request to MCP server."""
    
    query: str = Field(description="SQL query to analyze")
    request_type: str = Field(description="Type of request (analyze, optimize, etc.)")
    options: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional options for the request"
    )


class MCPResponse(BaseModel):
    """Response from MCP server."""
    
    success: bool = Field(description="Whether the request was successful")
    data: Dict[str, Any] = Field(description="Response data")
    error_message: Optional[str] = Field(
        default=None,
        description="Error message if request failed"
    )
    processing_time_ms: int = Field(description="Processing time in milliseconds")