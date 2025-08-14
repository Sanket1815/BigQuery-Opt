"""
LLM-based query optimizer that uses direct prompts with documentation context.
Simplified architecture that sends raw SQL and docs directly to LLM.
"""

import json
import time
from typing import Dict, List, Optional, Any
import google.generativeai as genai

from config.settings import get_settings
from src.common.exceptions import OptimizationError
from src.common.logger import QueryOptimizerLogger
from src.common.models import OptimizationResult, QueryAnalysis, AppliedOptimization


class LLMQueryOptimizer:
    """Direct LLM-based query optimizer using system and user prompts."""
    
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
    
    def optimize_with_llm(
        self, 
        sql_query: str,
        system_prompt: str,
        user_prompt: str,
        project_id: Optional[str] = None
    ) -> OptimizationResult:
        """
        Optimize SQL query using LLM with system and user prompts.
        
        Args:
            sql_query: Original SQL query to optimize
            system_prompt: System prompt with optimization instructions
            user_prompt: User prompt with query and documentation context
            project_id: Google Cloud project ID for table validation
        """
        start_time = time.time()
        
        try:
            self.logger.logger.info(f"Starting LLM optimization for query of length {len(sql_query)}")
            
            # Create chat with system prompt
            chat = self.model.start_chat(history=[])
            
            # Send system prompt first
            chat.send_message(system_prompt)
            
            # Send user prompt with query and docs
            response = chat.send_message(user_prompt)
            
            # Parse the LLM response
            optimization_data = self._parse_llm_response(response.text)
            
            # Validate the optimized query
            validated_query = self._validate_optimized_query(
                optimization_data.get("optimized_query", sql_query),
                project_id
            )
            
            # Create optimization result
            result = self._create_optimization_result(
                sql_query, optimization_data, validated_query, start_time
            )
            
            self.logger.logger.info(
                f"LLM optimization completed: {result.total_optimizations} optimizations applied"
            )
            
            return result
            
        except Exception as e:
            self.logger.log_error(e, {"operation": "optimize_with_llm"})
            
            # Return original query on failure
            return OptimizationResult(
                original_query=sql_query,
                query_analysis=self._create_basic_analysis(sql_query),
                optimized_query=sql_query,
                optimizations_applied=[],
                total_optimizations=0,
                processing_time_seconds=time.time() - start_time,
                validation_error=str(e)
            )
    
    def _parse_llm_response(self, response_text: str) -> Dict[str, Any]:
        """Parse LLM response and extract optimization data."""
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
            self.logger.logger.error(f"Failed to parse LLM response as JSON: {e}")
            raise OptimizationError(f"Invalid LLM response format: {e}")
        except Exception as e:
            self.logger.logger.error(f"Error parsing LLM response: {e}")
            raise OptimizationError(f"Failed to parse LLM response: {e}")
    
    def _validate_optimized_query(self, optimized_query: str, project_id: Optional[str]) -> str:
        """Validate and fix the optimized query."""
        # Fix project ID placeholders
        if project_id and 'your-project' in optimized_query:
            optimized_query = optimized_query.replace('your-project', project_id)
        
        # Basic SQL validation
        query_upper = optimized_query.upper().strip()
        if not query_upper.startswith('SELECT'):
            raise OptimizationError("Optimized query must start with SELECT")
        
        if 'FROM' not in query_upper:
            raise OptimizationError("Optimized query must include FROM clause")
        
        return optimized_query
    
    def _create_optimization_result(
        self,
        original_query: str,
        optimization_data: Dict[str, Any],
        validated_query: str,
        start_time: float
    ) -> OptimizationResult:
        """Create optimization result from LLM response."""
        
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
        
        # Create basic query analysis
        query_analysis = self._create_basic_analysis(original_query)
        
        return OptimizationResult(
            original_query=original_query,
            query_analysis=query_analysis,
            optimized_query=validated_query,
            optimizations_applied=applied_optimizations,
            total_optimizations=len(applied_optimizations),
            estimated_improvement=optimization_data.get('estimated_improvement'),
            processing_time_seconds=time.time() - start_time
        )
    
    def _create_basic_analysis(self, sql_query: str) -> QueryAnalysis:
        """Create basic query analysis."""
        import hashlib
        
        query_upper = sql_query.upper()
        
        return QueryAnalysis(
            original_query=sql_query,
            query_hash=hashlib.md5(sql_query.encode()).hexdigest(),
            complexity="moderate",
            table_count=len(re.findall(r'\bFROM\b|\bJOIN\b', query_upper)),
            join_count=len(re.findall(r'\bJOIN\b', query_upper)),
            subquery_count=sql_query.count('(SELECT'),
            window_function_count=len(re.findall(r'\bOVER\s*\(', query_upper)),
            aggregate_function_count=len(re.findall(r'\b(?:COUNT|SUM|AVG|MIN|MAX)\s*\(', query_upper)),
            potential_issues=[],
            applicable_patterns=[]
        )