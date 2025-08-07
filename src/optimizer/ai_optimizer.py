"""
AI-powered query optimizer using Gemini API to apply Google's BigQuery best practices.
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
        table_metadata: Dict[str, Any]
    ) -> OptimizationResult:
        """
        Optimize query using Google's official BigQuery best practices.
        
        CRITICAL REQUIREMENT: The optimized query MUST return IDENTICAL results.
        """
        start_time = time.time()
        
        try:
            # Build optimization prompt with Google's best practices
            prompt = self._build_best_practices_prompt(query, analysis, table_metadata)
            
            # Generate optimization using Gemini
            response = self.model.generate_content(prompt)
            
            # Parse the AI response
            optimization_data = self._parse_ai_response(response.text)
            
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
            
            # Return original query on failure
            return OptimizationResult(
                original_query=query,
                query_analysis=analysis,
                optimized_query=query,
                optimizations_applied=[],
                total_optimizations=0,
                processing_time_seconds=time.time() - start_time,
                validation_error=str(e)
            )
    
    def _build_best_practices_prompt(
        self, 
        query: str, 
        analysis: QueryAnalysis,
        table_metadata: Dict[str, Any]
    ) -> str:
        """Build optimization prompt based on Google's BigQuery best practices."""
        
        # Create table metadata summary
        table_info = ""
        for table_name, metadata in table_metadata.items():
            is_partitioned = metadata.get('is_partitioned', False)
            partition_field = metadata.get('partition_field', 'N/A')
            table_info += f"""
- {table_name}:
  Partitioned: {is_partitioned}
  Partition field: {partition_field}
  CRITICAL: Only add _PARTITIONDATE if Partitioned=True
"""
        
        prompt = f"""
You are an expert BigQuery SQL optimizer implementing Google's official best practices.

🚨 CRITICAL BUSINESS REQUIREMENT 🚨
The optimized query MUST return EXACTLY THE SAME RESULTS as the original query.
- Same number of rows
- Same column values  
- Same data types
- ZERO differences allowed
- Business logic must be preserved 100%

🎯 GOOGLE'S BIGQUERY BEST PRACTICES TO APPLY:

1. **PARTITION FILTERING** (High Impact - 50-80% improvement)
   - Add _PARTITIONDATE >= 'YYYY-MM-DD' ONLY for partitioned tables
   - NEVER add _PARTITIONDATE to non-partitioned tables (causes errors)
   - Reduces data scanned significantly

2. **COLUMN PRUNING** (Medium Impact - 20-40% improvement)
   - Replace SELECT * with specific column names
   - Reduces data transfer and processing
   - Improves query performance

3. **SUBQUERY TO JOIN CONVERSION** (High Impact - 30-60% improvement)
   - Convert EXISTS subqueries to INNER JOINs
   - Convert IN subqueries to INNER JOINs
   - Convert NOT EXISTS to LEFT JOIN with IS NULL
   - Much more efficient execution

4. **JOIN REORDERING** (Medium Impact - 20-40% improvement)
   - Place smaller tables first in JOIN order
   - Apply more selective filters early
   - Optimize JOIN execution plan

5. **APPROXIMATE AGGREGATION** (High Impact - 40-70% improvement)
   - Replace COUNT(DISTINCT column) with APPROX_COUNT_DISTINCT(column)
   - Use for large datasets where exact counts aren't critical
   - Significant performance improvement

6. **WINDOW FUNCTION OPTIMIZATION** (Medium Impact - 15-30% improvement)
   - Convert correlated subqueries to window functions
   - Optimize PARTITION BY clauses
   - Improve ORDER BY specifications

7. **PREDICATE PUSHDOWN** (Medium Impact - 25-45% improvement)
   - Move WHERE conditions closer to data sources
   - Apply filters before JOINs where possible
   - Reduce intermediate result sizes

TABLE METADATA:
{table_info}

QUERY ANALYSIS:
- Complexity: {analysis.complexity}
- Tables: {analysis.table_count}
- JOINs: {analysis.join_count}
- Subqueries: {analysis.subquery_count}
- Window functions: {analysis.window_function_count}
- Aggregations: {analysis.aggregate_function_count}
- Issues found: {', '.join(analysis.potential_issues)}

ORIGINAL QUERY TO OPTIMIZE:
```sql
{query}
```

OPTIMIZATION INSTRUCTIONS:
1. Apply Google's BigQuery best practices from the list above
2. ENSURE the optimized query returns IDENTICAL results
3. Only add _PARTITIONDATE for tables that are actually partitioned
4. Focus on performance without changing business logic
5. Provide clear explanations for each optimization

RESPONSE FORMAT (JSON ONLY):
{{
    "optimized_query": "The optimized SQL query that returns IDENTICAL results",
    "optimizations_applied": [
        {{
            "pattern_id": "partition_filtering",
            "pattern_name": "Partition Filtering",
            "description": "Added _PARTITIONDATE filter to reduce data scanned",
            "before_snippet": "WHERE order_date >= '2024-01-01'",
            "after_snippet": "WHERE _PARTITIONDATE >= '2024-01-01' AND order_date >= '2024-01-01'",
            "expected_improvement": 0.6,
            "confidence_score": 0.95,
            "google_best_practice": "Partition filtering reduces data scanned"
        }}
    ],
    "estimated_improvement": 0.45,
    "explanation": "Applied Google's BigQuery best practices for performance optimization"
}}

CRITICAL: Return only the JSON object. Results will be executed and validated for identity.
"""
        return prompt
    
    def _parse_ai_response(self, response_text: str) -> Dict[str, Any]:
        """Parse the AI response and extract optimization data."""
        try:
            # Clean the response text
            cleaned_response = response_text.strip()
            
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
        
        # Parse applied optimizations
        applied_optimizations = []
        for opt_data in optimization_data.get('optimizations_applied', []):
            optimization = AppliedOptimization(
                pattern_id=opt_data.get('pattern_id', 'unknown'),
                pattern_name=opt_data.get('pattern_name', 'Unknown Optimization'),
                description=opt_data.get('description', 'No description provided'),
                before_snippet=opt_data.get('before_snippet', ''),
                after_snippet=opt_data.get('after_snippet', ''),
                expected_improvement=opt_data.get('expected_improvement'),
                confidence_score=opt_data.get('confidence_score', 1.0)
            )
            applied_optimizations.append(optimization)
        
        # Create the result
        result = OptimizationResult(
            original_query=original_query,
            query_analysis=analysis,
            optimized_query=optimization_data.get('optimized_query', original_query),
            optimizations_applied=applied_optimizations,
            total_optimizations=len(applied_optimizations),
            estimated_improvement=optimization_data.get('estimated_improvement'),
            processing_time_seconds=time.time() - start_time
        )
        
        return result