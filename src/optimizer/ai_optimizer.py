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
        
        # Add optimization suggestions from documentation if available (truncated)
        suggestions_context = ""
        if optimization_suggestions:
            # Truncate suggestions to prevent API limits
            truncated_suggestions = optimization_suggestions[:2000] + "..." if len(optimization_suggestions) > 2000 else optimization_suggestions
            suggestions_context = f"""

📚 BIGQUERY OPTIMIZATION DOCUMENTATION:

{truncated_suggestions}
"""
        
        # Build comprehensive prompt
        prompt = f"""
2. Use only existing columns from table schema
3. Apply Google's BigQuery best practices
4. Include documentation references

UNDERPERFORMING QUERY TO OPTIMIZE:
```sql
{query}
```
{suggestions_context}

Apply optimizations based on the documentation suggestions above.
Focus on: Column Pruning, JOIN Reordering, Approximate Aggregation, Subquery Conversion.
DO NOT use _PARTITIONDATE filters.

RESPONSE FORMAT (JSON ONLY):
{{
    "optimized_query": "The optimized SQL query that returns IDENTICAL results",
    "optimizations_applied": [
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
    "estimated_improvement": 0.3,
    "explanation": "Applied BigQuery best practices for performance improvement while preserving exact business logic"
}}
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