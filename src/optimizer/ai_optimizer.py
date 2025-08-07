"""AI-powered query optimizer using Gemini API."""

import json
import time
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
        # self.model = genai.GenerativeModel(self.settings.gemini_model)
        # self.model = genai.GenerativeModel(model_name=self.settings.gemini_model_name)
        self.model = genai.GenerativeModel(
    model_name=self.settings.gemini_model_name,  # should be "gemini-pro"
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
        documentation_context: Optional[List[Dict]] = None
    ) -> OptimizationResult:
        """Optimize a SQL query using AI."""
        start_time = time.time()
        
        try:
            # Build the optimization prompt
            prompt = self._build_optimization_prompt(
                query, analysis, applicable_patterns, documentation_context
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
You are an expert BigQuery SQL optimizer. Your task is to optimize SQL queries for better performance while maintaining identical results.

🚨 CRITICAL REQUIREMENT: NEVER CHANGE BUSINESS LOGIC OR QUERY RESULTS 🚨
- The optimized query MUST return exactly the same data as the original
- Same number of rows, same column values, same ordering (unless ORDER BY is added for consistency)
- Only performance optimizations are allowed, never logic changes
- Results will be validated by executing both queries and comparing outputs
- ANY difference in results means the optimization FAILED

🎯 OPTIMIZATION PRINCIPLES:
1. BUSINESS LOGIC PRESERVATION IS MANDATORY - results must be 100% identical
2. Focus on performance improvements that reduce execution time and cost
3. Apply BigQuery-specific optimizations
4. Provide clear explanations for each change
5. Reference official BigQuery documentation when possible
6. ALWAYS add partition filters using _PARTITIONDATE >= 'YYYY-MM-DD' for ALL tables
7. Results will be executed and compared - they MUST be identical

🔧 MANDATORY OPTIMIZATION PATTERNS:
- Partition filtering: Add partition filters ONLY for tables that are actually partitioned by date/timestamp
- JOIN reordering: Place smaller tables first, more selective conditions early
- Subquery conversion: Convert correlated subqueries to JOINs
- Column pruning: Replace SELECT * with specific columns
- Approximate aggregation: Use APPROX_COUNT_DISTINCT instead of COUNT(DISTINCT)
- Window function optimization: Improve PARTITION BY and ORDER BY clauses
- Predicate pushdown: Move filters closer to data sources
- Clustering optimization: Use clustering keys in WHERE clauses

🎯 PARTITION FILTERING RULES (CRITICAL):
- NEVER add _PARTITIONDATE unless you are 100% certain the table is partitioned by date
- _PARTITIONDATE only exists for tables with date/timestamp partitioning
- Adding _PARTITIONDATE to non-partitioned tables will cause "Unrecognized name" errors
- Instead, focus on optimizing existing date filters and other performance improvements
- Only suggest partition filtering in comments, do not automatically add _PARTITIONDATE
- Prioritize other optimizations like JOIN reordering, column pruning, and subquery conversion

📋 RESPONSE FORMAT:
Return a JSON object with this exact structure:
{
    "optimized_query": "The optimized SQL query",
    "optimizations_applied": [
        {
            "pattern_id": "optimization_pattern_id",
            "pattern_name": "Human readable name",
            "description": "What was changed and why",
            "before_snippet": "Original SQL snippet",
            "after_snippet": "Optimized SQL snippet",
            "expected_improvement": 0.3,
            "confidence_score": 0.9
        }
    ],
    "estimated_improvement": 0.25,
    "explanation": "Overall explanation of optimizations"
}

⚠️ IMPORTANT: Only return the JSON object, no other text. Results will be validated for identity.
"""
        return context
    
    def _build_optimization_prompt(
        self,
        query: str,
        analysis: QueryAnalysis,
        patterns: List[OptimizationPattern],
        documentation_context: Optional[List[Dict]] = None
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
        
        # Add applicable patterns
        if patterns:
            prompt_parts.append("APPLICABLE OPTIMIZATION PATTERNS:")
            for pattern in patterns:
                prompt_parts.append(f"""
- {pattern.name} ({pattern.pattern_id}):
  Description: {pattern.description}
  Expected improvement: {pattern.expected_improvement or 'Unknown'}
  Documentation: {pattern.documentation_url or 'N/A'}
""")
        
        # Add documentation context if available
        if documentation_context:
            prompt_parts.append("RELEVANT DOCUMENTATION:")
            for doc in documentation_context[:3]:  # Limit to top 3 results
                prompt_parts.append(f"""
- {doc.get('title', 'Unknown')}:
  {doc.get('content', '')[:500]}...
""")
        
        # Add the query to optimize
        prompt_parts.append(f"""
QUERY TO OPTIMIZE:
```sql
{query}
```

IMPORTANT REMINDERS:
1. Results must be IDENTICAL - same rows, same values, same meaning
2. Add _PARTITIONDATE filters for better performance
3. Only optimize performance, never change business logic
4. Provide clear explanations for each optimization

Please optimize this query following the principles above and return the result in the specified JSON format.
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
Explain the following BigQuery SQL optimizations in simple terms for a developer:

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

Please provide a clear, concise explanation of:
1. What changes were made
2. Why these changes improve performance
3. Expected impact on query execution

Keep the explanation under 500 words and use technical but accessible language.
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

Return suggestions as a JSON array of strings, each being a specific actionable recommendation.
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