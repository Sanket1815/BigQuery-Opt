"""Request handlers for the MCP server."""

import hashlib
import re
from typing import Dict, List, Optional, Any
import sqlparse
from sqlparse.sql import Statement, Token
from sqlparse.tokens import Keyword, Name

from src.common.logger import QueryOptimizerLogger
from src.common.models import QueryAnalysis, QueryComplexity, OptimizationPattern
from src.crawler.documentation_processor import DocumentationProcessor


class DocumentationHandler:
    """Handler for documentation search requests."""
    
    def __init__(self, documentation_processor: DocumentationProcessor):
        self.processor = documentation_processor
        self.logger = QueryOptimizerLogger(__name__)
    
    async def search_documentation(
        self, 
        query: str, 
        n_results: int = 5,
        filter_patterns: Optional[List[str]] = None
    ) -> List[Dict]:
        """Search documentation for relevant information."""
        try:
            results = self.processor.search_documentation(
                query, n_results, filter_patterns
            )
            
            # Enhance results with additional context
            enhanced_results = []
            for result in results:
                enhanced_result = {
                    **result,
                    "relevance_score": result.get("similarity_score", 0),
                    "context_type": "documentation",
                    "applicable_patterns": result.get("optimization_patterns", [])
                }
                enhanced_results.append(enhanced_result)
            
            return enhanced_results
            
        except Exception as e:
            self.logger.log_error(e, {"operation": "search_documentation"})
            return []


class OptimizationHandler:
    """Handler for query optimization requests."""
    
    def __init__(self, documentation_processor: DocumentationProcessor):
        self.processor = documentation_processor
        self.logger = QueryOptimizerLogger(__name__)
    
    async def analyze_query(self, query: str) -> QueryAnalysis:
        """Analyze a SQL query for optimization opportunities."""
        try:
            # Parse the query
            parsed = sqlparse.parse(query)[0]
            
            # Extract query characteristics
            analysis_data = self._extract_query_characteristics(query, parsed)
            
            # Determine complexity
            complexity = self._determine_complexity(analysis_data)
            
            # Identify potential issues
            potential_issues = self._identify_potential_issues(query, parsed)
            
            # Find applicable patterns
            applicable_patterns = self._find_applicable_patterns(query)
            
            # Create query hash
            query_hash = hashlib.md5(query.encode()).hexdigest()
            
            analysis = QueryAnalysis(
                original_query=query,
                query_hash=query_hash,
                complexity=complexity,
                table_count=analysis_data["table_count"],
                join_count=analysis_data["join_count"],
                subquery_count=analysis_data["subquery_count"],
                window_function_count=analysis_data["window_function_count"],
                aggregate_function_count=analysis_data["aggregate_function_count"],
                has_partition_filter=analysis_data["has_partition_filter"],
                has_clustering_filter=analysis_data["has_clustering_filter"],
                potential_issues=potential_issues,
                applicable_patterns=applicable_patterns
            )
            
            self.logger.log_query_analysis(query, analysis.model_dump())
            return analysis
            
        except Exception as e:
            self.logger.log_error(e, {"operation": "analyze_query"})
            # Return a basic analysis on error
            return QueryAnalysis(
                original_query=query,
                query_hash=hashlib.md5(query.encode()).hexdigest(),
                complexity=QueryComplexity.SIMPLE,
                table_count=0,
                join_count=0,
                subquery_count=0,
                window_function_count=0,
                aggregate_function_count=0,
                potential_issues=["Failed to analyze query"],
                applicable_patterns=[]
            )
    
    async def get_patterns_for_query(self, query: str) -> List[OptimizationPattern]:
        """Get optimization patterns applicable to a SQL query."""
        try:
            patterns = self.processor.get_optimization_patterns_for_query(query)
            return patterns
        except Exception as e:
            self.logger.log_error(e, {"operation": "get_patterns_for_query"})
            return []
    
    async def get_optimization_suggestions(self, query: str) -> Dict[str, Any]:
        """Get detailed optimization suggestions for a SQL query."""
        try:
            # Analyze the query
            analysis = await self.analyze_query(query)
            
            # Get applicable patterns
            patterns = await self.get_patterns_for_query(query)
            
            # Search for relevant documentation
            doc_results = await DocumentationHandler(self.processor).search_documentation(
                query, n_results=5
            )
            
            # Generate specific suggestions
            suggestions = self._generate_specific_suggestions(query, analysis, patterns)
            
            return {
                "analysis": analysis.model_dump(),
                "applicable_patterns": [p.model_dump() for p in patterns],
                "specific_suggestions": suggestions,
                "documentation_references": doc_results,
                "priority_optimizations": self._prioritize_optimizations(patterns, analysis)
            }
            
        except Exception as e:
            self.logger.log_error(e, {"operation": "get_optimization_suggestions"})
            return {"error": str(e)}
    
    def _extract_query_characteristics(self, query: str, parsed: Statement) -> Dict:
        """Extract characteristics from parsed SQL query."""
        query_upper = query.upper()
        
        # Count different elements
        table_count = len(re.findall(r'\bFROM\s+[\w.]+|\bJOIN\s+[\w.]+', query_upper))
        join_count = len(re.findall(r'\b(?:INNER|LEFT|RIGHT|FULL|CROSS)\s+JOIN\b|\bJOIN\b', query_upper))
        subquery_count = query.count('(') - query.count(')')  # Rough estimate
        window_function_count = len(re.findall(r'\bOVER\s*\(', query_upper))
        aggregate_function_count = len(re.findall(
            r'\b(?:COUNT|SUM|AVG|MIN|MAX|GROUP_CONCAT)\s*\(', query_upper
        ))
        
        # Check for partition/clustering filters
        has_partition_filter = bool(re.search(
            r'_PARTITION(?:TIME|DATE)', query_upper
        ))
        has_clustering_filter = bool(re.search(
            r'WHERE.*=.*', query_upper
        ))
        
        return {
            "table_count": max(table_count, 1),  # At least 1 table
            "join_count": join_count,
            "subquery_count": max(subquery_count, 0),
            "window_function_count": window_function_count,
            "aggregate_function_count": aggregate_function_count,
            "has_partition_filter": has_partition_filter,
            "has_clustering_filter": has_clustering_filter
        }
    
    def _determine_complexity(self, analysis_data: Dict) -> QueryComplexity:
        """Determine query complexity based on characteristics."""
        complexity_score = 0
        
        # Add points for different characteristics
        complexity_score += analysis_data["table_count"] * 2
        complexity_score += analysis_data["join_count"] * 3
        complexity_score += analysis_data["subquery_count"] * 4
        complexity_score += analysis_data["window_function_count"] * 2
        complexity_score += analysis_data["aggregate_function_count"] * 1
        
        if complexity_score <= 5:
            return QueryComplexity.SIMPLE
        elif complexity_score <= 15:
            return QueryComplexity.MODERATE
        elif complexity_score <= 30:
            return QueryComplexity.COMPLEX
        else:
            return QueryComplexity.VERY_COMPLEX
    
    def _identify_potential_issues(self, query: str, parsed: Statement) -> List[str]:
        """Identify potential performance issues in the query."""
        issues = []
        query_upper = query.upper()
        
        # Check for SELECT *
        if 'SELECT *' in query_upper:
            issues.append("Using SELECT * may retrieve unnecessary columns")
        
        # Check for missing partition filters
        if 'FROM' in query_upper and '_PARTITIONDATE' not in query_upper:
            issues.append("Consider adding partition filter if table is partitioned by date")
        
        # Check for missing WHERE clause
        if 'WHERE' not in query_upper and 'FROM' in query_upper:
            issues.append("Query may scan entire table without filtering - consider adding WHERE clause")
        
        # Check for correlated subqueries
        if re.search(r'WHERE.*EXISTS\s*\(SELECT.*\)', query_upper):
            issues.append("Correlated subqueries may impact performance")
        
        # Check for COUNT(DISTINCT) on large datasets
        if 'COUNT(DISTINCT' in query_upper:
            issues.append("COUNT(DISTINCT) can be slow on large datasets - consider APPROX_COUNT_DISTINCT (results may vary slightly)")
        
        # Check for complex JOINs without proper ordering
        join_count = len(re.findall(r'\bJOIN\b', query_upper))
        if join_count > 2:
            issues.append("Multiple JOINs may benefit from reordering by table size")
        
        # Check for window functions without proper partitioning
        if 'OVER (' in query_upper and 'PARTITION BY' not in query_upper:
            issues.append("Window functions without PARTITION BY may be inefficient")
        
        return issues
    
    def _find_applicable_patterns(self, query: str) -> List[str]:
        """Find optimization pattern IDs applicable to the query."""
        applicable = []
        query_upper = query.upper()
        
        patterns_map = {
            "partition_filtering": ["FROM", "WHERE", "date"],  # Suggest partition filtering for date queries
            "join_reordering": ["JOIN"],
            "subquery_to_join": ["EXISTS", "IN (SELECT"],
            "window_optimization": ["OVER ("],
            "approximate_aggregation": ["COUNT(DISTINCT"],
            "column_pruning": ["SELECT *"],
            "predicate_pushdown": ["WHERE", "HAVING"],
            "clustering_optimization": ["WHERE", "ORDER BY"],
            "materialized_view": ["GROUP BY", "AGGREGATE"]
        }
        
        # Suggest partition filtering for queries with date filters (likely partitioned tables)
        if ("FROM" in query_upper and "_PARTITIONDATE" not in query_upper and 
            any(date_keyword in query_upper for date_keyword in ["DATE", "TIMESTAMP", ">= '2", "BETWEEN"])):
            applicable.append("partition_filtering")
        
        for pattern_id, keywords in patterns_map.items():
            if pattern_id == "partition_filtering":
                continue  # Already handled above
            if any(keyword in query_upper for keyword in keywords):
                applicable.append(pattern_id)
        
        return applicable
    
    def _generate_specific_suggestions(
        self, 
        query: str, 
        analysis: QueryAnalysis, 
        patterns: List[OptimizationPattern]
    ) -> List[Dict]:
        """Generate specific optimization suggestions."""
        suggestions = []
        
        for pattern in patterns:
            suggestion = {
                "pattern_id": pattern.pattern_id,
                "pattern_name": pattern.name,
                "description": pattern.description,
                "expected_improvement": pattern.expected_improvement,
                "documentation_url": pattern.documentation_url,
                "specific_advice": self._generate_specific_advice(query, pattern),
                "priority": self._calculate_priority(pattern, analysis)
            }
            suggestions.append(suggestion)
        
        # Sort by priority (higher is better)
        suggestions.sort(key=lambda x: x["priority"], reverse=True)
        
        return suggestions
    
    def _generate_specific_advice(self, query: str, pattern: OptimizationPattern) -> str:
        """Generate specific advice for a pattern and query."""
        query_upper = query.upper()
        
        if pattern.pattern_id == "join_reordering":
            return "Consider reordering JOINs to place smaller tables first and more selective conditions early in the JOIN chain."
        
        elif pattern.pattern_id == "partition_filtering":
            return "Add partition filters like WHERE _PARTITIONDATE >= '2024-01-01' to reduce data scanned."
        
        elif pattern.pattern_id == "subquery_to_join":
            return "Convert EXISTS or IN subqueries to INNER JOINs or LEFT JOINs for better performance."
        
        elif pattern.pattern_id == "window_optimization":
            return "Optimize window functions by using appropriate PARTITION BY clauses and avoiding unnecessary ORDER BY."
        
        elif pattern.pattern_id == "approximate_aggregation":
            return "Replace COUNT(DISTINCT column) with APPROX_COUNT_DISTINCT(column) for better performance on large datasets."
        
        elif pattern.pattern_id == "column_pruning":
            return "Replace SELECT * with specific column names to reduce data transfer and improve performance."
        
        elif pattern.pattern_id == "predicate_pushdown":
            return "Move WHERE conditions as close to the data source as possible to filter data early."
        
        elif pattern.pattern_id == "clustering_optimization":
            return "Ensure WHERE clauses use clustering keys and consider clustering tables by frequently filtered columns."
        
        elif pattern.pattern_id == "materialized_view":
            return "Consider creating a materialized view for this aggregation if it's run frequently."
        
        return pattern.description
    
    def _calculate_priority(self, pattern: OptimizationPattern, analysis: QueryAnalysis) -> int:
        """Calculate priority score for an optimization pattern."""
        priority = 0
        
        # Base priority from expected improvement
        if pattern.expected_improvement:
            priority += int(pattern.expected_improvement * 100)
        
        # Adjust based on query complexity
        if analysis.complexity == QueryComplexity.VERY_COMPLEX:
            priority += 20
        elif analysis.complexity == QueryComplexity.COMPLEX:
            priority += 10
        
        # Boost priority for common high-impact patterns
        high_impact_patterns = ["partition_filtering", "approximate_aggregation", "column_pruning"]
        if pattern.pattern_id in high_impact_patterns:
            priority += 15
        
        return priority
    
    def _prioritize_optimizations(
        self, 
        patterns: List[OptimizationPattern], 
        analysis: QueryAnalysis
    ) -> List[str]:
        """Return a prioritized list of optimization pattern IDs."""
        pattern_priorities = []
        
        for pattern in patterns:
            priority = self._calculate_priority(pattern, analysis)
            pattern_priorities.append((pattern.pattern_id, priority))
        
        # Sort by priority (higher first)
        pattern_priorities.sort(key=lambda x: x[1], reverse=True)
        
        return [pattern_id for pattern_id, _ in pattern_priorities]