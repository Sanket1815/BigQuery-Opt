"""AI-powered query optimizer using Gemini API."""

import json
import time
import re
from typing import Dict, List, Optional, Any
import google.generativeai as genai

from config.settings import get_settings
from src.common.exceptions import OptimizationError
from src.common.logger import QueryOptimizerLogger
from src.common.models import (
    OptimizationResult, 
    QueryAnalysis, 
    AppliedOptimization,
    OptimizationPattern
)


class GeminiQueryOptimizer:
    """AI-powered BigQuery query optimizer using Gemini."""
    
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
        
        # Load optimization context
        self.optimization_context = self._build_optimization_context()
    
    def optimize_query(
        self, 
        query: str, 
        analysis: QueryAnalysis,
        applicable_patterns: List[OptimizationPattern],
        documentation_context: Optional[List[Dict]] = None,
        table_metadata: Optional[Dict[str, Any]] = None
    ) -> OptimizationResult:
        """Optimize a SQL query using AI with dynamic optimization patterns."""
        start_time = time.time()
        
        try:
            # Build the optimization prompt with table metadata
            prompt = self._build_optimization_prompt(
                query, analysis, applicable_patterns, documentation_context, table_metadata
            )
            
            # Generate optimization using Gemini
            response = self.model.generate_content(prompt)
            
            # Parse the AI response
            optimization_data = self._parse_ai_response(response.text)
            
            # Create optimization result
            result = self._create_optimization_result(
                query, analysis, optimization_data, start_time
            )
            
            self.logger.logger.info(
                "Query optimization completed",
                original_length=len(query),
                optimized_length=len(result.optimized_query),
                optimizations_applied=result.total_optimizations,
                processing_time=result.processing_time_seconds
            )
            
            return result
            
        except Exception as e:
            self.logger.log_error(e, {"operation": "optimize_query"})
            
            # Return a result indicating failure
            return OptimizationResult(
                original_query=query,
                query_analysis=analysis,
                optimized_query=query,  # Return original on failure
                optimizations_applied=[],
                total_optimizations=0,
                processing_time_seconds=time.time() - start_time,
                validation_error=str(e)
            )
    
    def _build_optimization_context(self) -> str:
        """Build the optimization context for the AI model."""
        context = """
You are an expert BigQuery SQL optimizer. Your task is to optimize SQL queries for better performance while maintaining IDENTICAL results.

🚨 CRITICAL REQUIREMENT: RESULTS MUST BE 100% IDENTICAL 🚨
- The optimized query MUST return exactly the same data as the original
- Same number of rows, same column values, same data types
- Only performance optimizations are allowed, NEVER change business logic
- Results will be executed and compared - they MUST match exactly
- ANY difference in results means the optimization FAILED

🎯 DYNAMIC OPTIMIZATION PATTERNS TO APPLY:

1. **SUBQUERY TO JOIN CONVERSION**
   - Convert EXISTS subqueries to INNER JOINs
   - Convert IN subqueries to INNER JOINs  
   - Convert NOT EXISTS to LEFT JOIN with IS NULL
   - Convert correlated subqueries to window functions where appropriate
   
2. **PARTITION FILTERING** (ONLY for partitioned tables)
   - Add _PARTITIONDATE >= 'YYYY-MM-DD' filters for date-partitioned tables
   - NEVER add _PARTITIONDATE to non-partitioned tables
   - Check table metadata before adding partition filters
   
3. **JOIN OPTIMIZATION**
   - Reorder JOINs to place smaller tables first
   - Move more selective conditions earlier in JOIN chain
   - Convert implicit JOINs to explicit JOINs
   
4. **APPROXIMATE AGGREGATION**
   - Replace COUNT(DISTINCT column) with APPROX_COUNT_DISTINCT(column)
   - Use HLL_COUNT.MERGE for very large datasets
   - Only when exact counts aren't critical for business logic
   
5. **COLUMN PRUNING**
   - Replace SELECT * with specific column names
   - Remove unused columns from intermediate results
   - Reduce data transfer and processing
   
6. **WINDOW FUNCTION OPTIMIZATION**
   - Convert correlated subqueries to window functions
   - Optimize PARTITION BY clauses
   - Improve ORDER BY specifications in window functions
   
7. **CLUSTERING RECOMMENDATIONS**
   - Use clustering keys in WHERE clauses
   - Optimize filter conditions to leverage clustering
   
8. **PREDICATE PUSHDOWN**
   - Move WHERE conditions closer to data sources
   - Apply filters before JOINs where possible
   - Push filters into subqueries

🔧 OPTIMIZATION RULES:
- ALWAYS preserve exact business logic and results
- Focus on reducing bytes scanned and execution time
- Use BigQuery-specific optimizations
- Provide clear explanations for each change
- Reference official BigQuery best practices

📋 RESPONSE FORMAT (JSON ONLY):
{
    "optimized_query": "The optimized SQL query that returns IDENTICAL results",
    "optimizations_applied": [
        {
            "pattern_id": "subquery_to_join",
            "pattern_name": "Subquery to JOIN Conversion",
            "description": "Converted EXISTS subquery to INNER JOIN for better performance",
            "before_snippet": "WHERE EXISTS (SELECT 1 FROM table2 WHERE...)",
            "after_snippet": "INNER JOIN table2 ON ...",
            "expected_improvement": 0.3,
            "confidence_score": 0.9
        }
    ],
    "estimated_improvement": 0.25,
    "explanation": "Overall explanation of optimizations applied"
}

⚠️ CRITICAL: Only return the JSON object. Results will be validated for identity.
"""
        return context
    
    def _build_optimization_prompt(
        self,
        query: str,
        analysis: QueryAnalysis,
        patterns: List[OptimizationPattern],
        documentation_context: Optional[List[Dict]] = None,
        table_metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Build the complete optimization prompt for Gemini."""
        
        # Start with the base context
        prompt_parts = [self.optimization_context]
        
        # Add query analysis
        prompt_parts.append(f"""
QUERY ANALYSIS:
- Complexity: {analysis.complexity}
- Tables: {analysis.table_count}
- JOINs: {analysis.join_count}
- Subqueries: {analysis.subquery_count}
- Window functions: {analysis.window_function_count}
- Aggregations: {analysis.aggregate_function_count}
- Has partition filter: {analysis.has_partition_filter}
- Potential issues: {', '.join(analysis.potential_issues)}
""")
        
        # Add table metadata if available
        if table_metadata:
            prompt_parts.append("TABLE METADATA:")
            for table_name, metadata in table_metadata.items():
                is_partitioned = metadata.get('is_partitioned', False)
                partition_field = metadata.get('partition_field', 'N/A')
                prompt_parts.append(f"""
- {table_name}:
  Partitioned: {is_partitioned}
  Partition field: {partition_field}
  Use _PARTITIONDATE: {is_partitioned}
""")
        
        # Add applicable patterns
        if patterns:
            prompt_parts.append("APPLICABLE OPTIMIZATION PATTERNS:")
            for pattern in patterns:
                prompt_parts.append(f"""
- {pattern.name} ({pattern.pattern_id}):
  Description: {pattern.description}
  Expected improvement: {pattern.expected_improvement or 'Unknown'}
""")
        
        # Add documentation context if available
        if documentation_context:
            prompt_parts.append("RELEVANT DOCUMENTATION:")
            for doc in documentation_context[:3]:
                prompt_parts.append(f"""
- {doc.get('title', 'Unknown')}:
  {doc.get('content', '')[:300]}...
""")
        
        # Add the query to optimize
        prompt_parts.append(f"""
QUERY TO OPTIMIZE:
```sql
{query}
```

OPTIMIZATION INSTRUCTIONS:
1. Analyze the query for optimization opportunities
2. Apply appropriate optimizations from the patterns above
3. ENSURE results remain IDENTICAL - same rows, same values
4. Only add _PARTITIONDATE for tables that are actually partitioned
5. Focus on performance improvements without changing business logic
6. Return optimized query in the JSON format specified

Please optimize this query and return the result in JSON format.
""")
        
        return "\n".join(prompt_parts)
    
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
    
    def generate_explanation(
        self, 
        original_query: str, 
        optimized_query: str,
        optimizations: List[AppliedOptimization]
    ) -> str:
        """Generate a detailed explanation of the optimizations."""
        
        prompt = f"""
Explain the following BigQuery SQL optimizations in simple terms:

Original Query:
```sql
{original_query}
```

Optimized Query:
```sql
{optimized_query}
```

Optimizations Applied:
{json.dumps([opt.model_dump() for opt in optimizations], indent=2)}

Provide a clear explanation of what changed and why it improves performance.
Keep it under 300 words.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            self.logger.log_error(e, {"operation": "generate_explanation"})
            return "Unable to generate detailed explanation due to an error."
    
    def suggest_table_optimizations(
        self, 
        query: str, 
        table_info: Dict[str, Any]
    ) -> List[str]:
        """Suggest table-level optimizations based on query patterns."""
        
        prompt = f"""
Based on this BigQuery SQL query and table information, suggest table-level optimizations:

Query:
```sql
{query}
```

Table Information:
{json.dumps(table_info, indent=2)}

Suggest specific optimizations such as:
- Partitioning strategies
- Clustering key recommendations
- Schema optimizations
- Materialized view opportunities

Return suggestions as a JSON array of strings.
"""
        
        try:
            response = self.model.generate_content(prompt)
            suggestions_data = json.loads(response.text)
            
            if isinstance(suggestions_data, list):
                return suggestions_data
            else:
                return ["Unable to parse table optimization suggestions"]
                
        except Exception as e:
            self.logger.log_error(e, {"operation": "suggest_table_optimizations"})
            return ["Error generating table optimization suggestions"]