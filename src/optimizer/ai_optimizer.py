"""
AI-powered query optimizer using Gemini API to apply Google's BigQuery best practices.

This module implements the core AI optimization logic that transforms underperforming
BigQuery queries into optimized versions while preserving exact business logic.
"""

import json
import time
import re
from typing import Dict, List, Optional, Any
import google.generativeai as genai

from config.settings import get_settings
from src.common.exceptions import OptimizationError
from src.common.logger import QueryOptimizerLogger
from src.common.models import OptimizationResult, QueryAnalysis, AppliedOptimization


class GeminiQueryOptimizer:
    """
    AI-powered BigQuery query optimizer that applies Google's official best practices
    to underperforming queries while preserving exact business logic.
    
    SUCCESS METRICS:
    1. Functional Accuracy: 100% - Optimized queries must return identical results
    2. Performance Improvement: Target 30-50% reduction in query execution time
    3. Documentation Coverage: References 20+ distinct BigQuery optimization patterns
    """
    
    def __init__(self):
        self.settings = get_settings()
        self.logger = QueryOptimizerLogger(__name__)
        
        # Configure Gemini
        if not self.settings.gemini_api_key:
            raise OptimizationError("Gemini API key not configured")
        
        genai.configure(api_key=self.settings.gemini_api_key)
        self.model = genai.GenerativeModel(
            model_name=self.settings.gemini_model_name,
            safety_settings=[
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"}
            ]
        )
    
    def optimize_with_best_practices(
        self, 
        query: str, 
        analysis: QueryAnalysis,
        table_metadata: Dict[str, Any],
        optimization_suggestions: Optional[str] = None  # NEW parameter
    ) -> OptimizationResult:
        """
        Apply Google's official BigQuery best practices to underperforming queries.
        
        CRITICAL BUSINESS REQUIREMENT: The optimized query MUST return IDENTICAL results.
        This is non-negotiable for business logic preservation.
        
        Now enhanced with direct optimization suggestions from markdown documentation.
        """
        start_time = time.time()
        
        try:
            # Build optimization prompt with Google's best practices
            prompt = self._build_comprehensive_optimization_prompt(
                query, analysis, table_metadata, optimization_suggestions
            )
            
            # Generate optimization using Gemini
            response = self.model.generate_content(prompt)
            
            # Parse the AI response
            optimization_data = self._parse_ai_response(response.text)
            
            # Log optimization details
            optimizations_count = len(optimization_data.get('optimizations_applied', []))
            self.logger.logger.info(f"AI generated {optimizations_count} optimizations")
            
            # Create optimization result
            result = self._create_optimization_result(query, analysis, optimization_data, start_time)
            
            self.logger.logger.info(
                "Query optimization completed using Google best practices",
                optimizations_applied=result.total_optimizations,
                processing_time=result.processing_time_seconds
            )
            
            return result
            
        except Exception as e:
            self.logger.log_error(e, {"operation": "optimize_with_best_practices"})
            
            # Return original query on failure (preserve business logic)
            return OptimizationResult(
                original_query=query,
                query_analysis=analysis,
                optimized_query=query,
                optimizations_applied=[],
                total_optimizations=0,
                processing_time_seconds=time.time() - start_time,
                validation_error=str(e)
            )
    
    def _build_comprehensive_optimization_prompt(
        self, 
        query: str, 
        analysis: QueryAnalysis,
        table_metadata: Dict[str, Any],
        optimization_suggestions: Optional[str] = None
    ) -> str:
        """Build comprehensive optimization prompt based on Google's BigQuery best practices."""
        
        # Create detailed table metadata summary
        table_info = ""
        for table_name, metadata in table_metadata.items():
            is_partitioned = metadata.get('is_partitioned', False)
            partition_field = metadata.get('partition_field', 'N/A')
            row_count = metadata.get('num_rows', 0)
            size_gb = metadata.get('num_bytes', 0) / (1024**3) if metadata.get('num_bytes') else 0
            clustering_fields = metadata.get('clustering_fields', [])
            schema_columns = metadata.get('schema_columns', [])
            table_name_simple = metadata.get('table_name_simple', table_name.split('.')[-1])
            
            table_info += f"""
- {table_name}:
  Table name: {table_name_simple}
  Partitioned: {is_partitioned}
  Partition field: {partition_field}
  Row count: {row_count:,}
  Size: {size_gb:.2f} GB
  Clustering fields: {clustering_fields}
  Available columns: {schema_columns}
  🚨 CRITICAL: ONLY add _PARTITIONDATE if Partitioned=True!
"""
        
        # Add optimization suggestions from documentation if available
        suggestions_context = ""
        if optimization_suggestions:
            suggestions_context = f"""

📚 BIGQUERY OPTIMIZATION DOCUMENTATION:

{optimization_suggestions}
"""
        
        # Build comprehensive prompt
        prompt = f"""
You are an expert BigQuery SQL optimizer implementing Google's official best practices to solve real business problems.

🚨 BUSINESS PROBLEM 🚨
Organizations have underperforming BigQuery queries that:
- Fail to meet performance SLAs
- Cost money through inefficient compute usage  
- Delay business insights
- Frustrate end users

🎯 YOUR MISSION 🎯
Transform this underperforming query into an optimized version that:
- Returns EXACTLY THE SAME RESULTS (100% functional accuracy)
- Improves performance by 30-50%
- Applies Google's official BigQuery best practices
- Includes clear explanations with documentation references

🚨 CRITICAL BUSINESS REQUIREMENT 🚨
The optimized query MUST return EXACTLY THE SAME RESULTS as the original query.
- Same number of rows
- Same column values  
- Same data types
- ZERO differences allowed
- Business logic must be preserved 100%

🚨 CRITICAL PROJECT ID REQUIREMENT 🚨
- ALWAYS use the ACTUAL project ID from table metadata
- NEVER use placeholder project IDs like "your-project" or "project"
- Replace ANY placeholder project IDs with the REAL project ID
- Ensure ALL table references use the correct project ID

🚨 CRITICAL COLUMN VALIDATION REQUIREMENT 🚨
- ONLY use columns that ACTUALLY exist in the table schema
- NEVER generate non-existent column names
- When replacing SELECT *, use ONLY the columns listed in "Available columns"
- If unsure about column names, keep the original SELECT clause
- Example: If Available columns: [order_id, customer_id, total_amount], use these EXACT names

📋 GOOGLE'S BIGQUERY BEST PRACTICES (20+ PATTERNS):

1. **PARTITION FILTERING** (High Impact - 50-80% improvement)
   - 🚨 CRITICAL: Only add _PARTITIONDATE >= 'YYYY-MM-DD' if table shows Partitioned=True
   - NEVER add _PARTITIONDATE if Partitioned=False - this causes BigQuery errors!
   - 🚨 IMPORTANT: Use table alias when adding _PARTITIONDATE (e.g., o._PARTITIONDATE, not just _PARTITIONDATE)
   - Check table metadata carefully before adding partition filters
   - Documentation: https://cloud.google.com/bigquery/docs/partitioned-tables

2. **COLUMN PRUNING** (Medium Impact - 20-40% improvement)
   - Replace SELECT * with specific column names
   - 🚨 CRITICAL: ONLY use columns that exist in the table schema
   - Use the exact column names from "Available columns" in table metadata
   - Reduces data transfer and processing costs
   - Documentation: https://cloud.google.com/bigquery/docs/best-practices-performance-input

3. **SUBQUERY TO JOIN CONVERSION** (High Impact - 30-60% improvement)
   - Convert EXISTS subqueries to INNER JOINs
   - Convert IN subqueries to INNER JOINs  
   - Convert NOT EXISTS to LEFT JOIN with IS NULL
   - Documentation: https://cloud.google.com/bigquery/docs/best-practices-performance-compute

4. **JOIN REORDERING** (Medium Impact - 20-40% improvement)
   - Place smaller tables first in JOIN order
   - Apply more selective filters early
   - Use table size metadata for optimization
   - Documentation: https://cloud.google.com/bigquery/docs/best-practices-performance-compute

5. **APPROXIMATE AGGREGATION** (High Impact - 40-70% improvement)
   - Replace COUNT(DISTINCT column) with APPROX_COUNT_DISTINCT(column)
   - Use for large datasets where exact counts aren't critical
   - Documentation: https://cloud.google.com/bigquery/docs/reference/standard-sql/approximate_aggregate_functions

6. **WINDOW FUNCTION OPTIMIZATION** (Medium Impact - 15-30% improvement)
   - Convert correlated subqueries to window functions
   - Optimize PARTITION BY clauses
   - Improve ORDER BY specifications
   - Documentation: https://cloud.google.com/bigquery/docs/reference/standard-sql/analytic-functions

7. **PREDICATE PUSHDOWN** (Medium Impact - 25-45% improvement)
   - Move WHERE conditions closer to data sources
   - Apply filters before JOINs where possible
   - Reduce intermediate result sizes
   - Documentation: https://cloud.google.com/bigquery/docs/best-practices-performance-compute

8. **CLUSTERING OPTIMIZATION** (Medium Impact - 20-35% improvement)
   - Use clustering keys in WHERE clauses
   - Leverage existing clustering for better performance
   - Documentation: https://cloud.google.com/bigquery/docs/clustered-tables

9. **MATERIALIZED VIEW SUGGESTIONS** (High Impact - 60-90% improvement)
   - Identify frequently used aggregations
   - Suggest materialized views for common patterns
   - Documentation: https://cloud.google.com/bigquery/docs/materialized-views-intro

10. **LIMIT OPTIMIZATION** (Variable Impact)
    - Add LIMIT when appropriate to reduce result size
    - Optimize ORDER BY with LIMIT
    - Documentation: https://cloud.google.com/bigquery/docs/best-practices-performance-output

TABLE METADATA:
{table_info}

QUERY ANALYSIS:
- Complexity: {analysis.complexity}
- Tables: {analysis.table_count}
- JOINs: {analysis.join_count}
- Subqueries: {analysis.subquery_count}
- Window functions: {analysis.window_function_count}
- Aggregations: {analysis.aggregate_function_count}
- Performance issues: {', '.join(analysis.potential_issues)}
- Applicable patterns: {', '.join(analysis.applicable_patterns)}

UNDERPERFORMING QUERY TO OPTIMIZE:
```sql
{query}
```
{suggestions_context}

🚨 CRITICAL PARTITION FILTERING RULES:
1. ONLY add _PARTITIONDATE if table metadata shows Partitioned=True
2. NEVER add _PARTITIONDATE to non-partitioned tables - this causes BigQuery errors!
3. If table is partitioned, use the date column filter instead of _PARTITIONDATE
4. Example: WHERE order_date >= '2024-01-01' (NOT _PARTITIONDATE)
5. Focus on other optimizations like column pruning, JOIN reordering, approximate aggregation

🚨 PARTITION FILTERING IS DISABLED - DO NOT USE _PARTITIONDATE
Instead of partition filtering, focus on these high-impact optimizations:
- Column Pruning (SELECT specific columns instead of *)
- JOIN Reordering (smaller tables first)
- Approximate Aggregation (APPROX_COUNT_DISTINCT)
- Subquery to JOIN conversion
- Window function optimization

🎯 OPTIMIZATION REQUIREMENTS:
1. Apply at least 1-3 relevant optimizations from Google's best practices
2. ENSURE the optimized query returns IDENTICAL results
3. CRITICAL: Replace ALL placeholder project IDs with the ACTUAL project ID
4. CRITICAL: Check table metadata - only add table_alias._PARTITIONDATE if Partitioned=True
5. Focus on performance without changing business logic
6. Include documentation references for each optimization
7. Target 30-50% performance improvement

RESPONSE FORMAT (JSON ONLY):
{{
    "optimized_query": "The optimized SQL query with CORRECT project ID that returns IDENTICAL results",
    "optimizations_applied": [
        {{
            "pattern_id": "partition_filtering",
            "pattern_name": "Partition Filtering",
            "description": "Added _PARTITIONDATE filter to reduce data scanned by 60%",
            "before_snippet": "WHERE o.order_date >= '2024-01-01'",
            "after_snippet": "WHERE o._PARTITIONDATE >= '2024-01-01' AND o.order_date >= '2024-01-01'",
            "expected_improvement": 0.6,
            "confidence_score": 0.95,
            "documentation_reference": "https://cloud.google.com/bigquery/docs/partitioned-tables"
        }},
        {{
            "pattern_id": "column_pruning",
            "pattern_name": "Column Pruning",
            "description": "Replaced SELECT * with specific columns to reduce data transfer",
            "before_snippet": "SELECT *",
            "after_snippet": "SELECT customer_id, order_date, total_amount",
            "expected_improvement": 0.3,
            "confidence_score": 0.9,
            "documentation_reference": "https://cloud.google.com/bigquery/docs/best-practices-performance-input"
        }}
    ],
    "estimated_improvement": 0.72,
    "explanation": "Applied Google's BigQuery best practices: partition filtering and column pruning for significant performance improvement while preserving exact business logic"
}}

🚨 CRITICAL REMINDERS:
- ALWAYS replace placeholder project IDs with the actual project ID from table metadata
- NEVER add _PARTITIONDATE to non-partitioned tables
- ALWAYS use table alias with _PARTITIONDATE (e.g., o._PARTITIONDATE)
- ONLY use column names that exist in the table schema (see "Available columns")
- When doing column pruning, use EXACT column names from table metadata
- Results must be 100% identical
- Apply multiple optimizations when possible
- Include documentation references
- Target 30-50% performance improvement

Return only the JSON object. The optimized query will be executed and validated for identical results.
"""
        return prompt
    
    def _parse_ai_response(self, response_text: str) -> Dict[str, Any]:
        """Parse the AI response and extract optimization data."""
        try:
            # Clean the response text
            cleaned_response = response_text.strip()
            
            # Log the raw response for debugging
            self.logger.logger.debug(f"Raw AI response: {response_text[:500]}...")
            
            # Remove markdown code blocks if present
            if cleaned_response.startswith('```json'):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.startswith('```'):
                cleaned_response = cleaned_response[3:]
            if cleaned_response.endswith('```'):
                cleaned_response = cleaned_response[:-3]
            
            cleaned_response = cleaned_response.strip()
            
            # Parse JSON
            optimization_data = json.loads(cleaned_response)
            
            # Validate required fields
            required_fields = ['optimized_query', 'optimizations_applied']
            for field in required_fields:
                if field not in optimization_data:
                    raise ValueError(f"Missing required field: {field}")
            
            # Log what optimizations were found
            optimizations = optimization_data.get('optimizations_applied', [])
            self.logger.logger.info(f"Parsed {len(optimizations)} optimizations from AI response")
            
            # Log each optimization for debugging
            for i, opt in enumerate(optimizations, 1):
                pattern_name = opt.get('pattern_name', 'Unknown')
                expected_improvement = opt.get('expected_improvement', 0)
                self.logger.logger.info(f"  {i}. {pattern_name} (expected: {expected_improvement:.1%})")
            
            return optimization_data
            
        except json.JSONDecodeError as e:
            self.logger.logger.error(f"Failed to parse AI response as JSON: {e}")
            self.logger.logger.debug(f"Response text: {response_text}")
            raise OptimizationError(f"Invalid AI response format: {e}")
        except Exception as e:
            self.logger.logger.error(f"Error parsing AI response: {e}")
            raise OptimizationError(f"Failed to parse AI response: {e}")
    
    def _create_optimization_result(
        self,
        original_query: str,
        analysis: QueryAnalysis,
        optimization_data: Dict[str, Any],
        start_time: float
    ) -> OptimizationResult:
        """Create an OptimizationResult from the AI response."""
        
        # Get the actual project ID from settings
        actual_project_id = self.settings.google_cloud_project
        
        # Parse applied optimizations
        applied_optimizations = []
        for opt_data in optimization_data.get('optimizations_applied', []):
            optimization = AppliedOptimization(
                pattern_id=opt_data.get('pattern_id', 'unknown'),
                pattern_name=opt_data.get('pattern_name', 'Unknown Optimization'),
                description=opt_data.get('description', 'No description provided'),
                before_snippet=opt_data.get('before_snippet', ''),
                after_snippet=opt_data.get('after_snippet', ''),
                documentation_reference=opt_data.get('documentation_reference', ''),
                expected_improvement=opt_data.get('expected_improvement'),
                confidence_score=opt_data.get('confidence_score', 1.0)
            )
            applied_optimizations.append(optimization)
        
        # Fix project ID in optimized query
        optimized_query = optimization_data.get('optimized_query', original_query)
        if actual_project_id and 'your-project' in optimized_query:
            optimized_query = optimized_query.replace('your-project', actual_project_id)
            self.logger.logger.info(f"Replaced placeholder project ID with actual: {actual_project_id}")
        
        # Create the result
        result = OptimizationResult(
            original_query=original_query,
            query_analysis=analysis,
            optimized_query=optimized_query,
            optimizations_applied=applied_optimizations,
            total_optimizations=len(applied_optimizations),
            estimated_improvement=optimization_data.get('estimated_improvement'),
            processing_time_seconds=time.time() - start_time
        )
        
        return result