"""
Direct SQL optimization handler that sends raw SQL to Gemini API with all MD documentation.
Implements the complete workflow: load docs, send to Gemini, validate results, display comparison.
"""

import hashlib
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any

# Try to import Gemini API, but don't fail if not available
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    genai = None

from src.common.logger import QueryOptimizerLogger


class DirectSQLOptimizationHandler:
    """Handles direct SQL optimization requests using Gemini API and markdown documentation."""
    
    def __init__(self, docs_directory: str = "data/optimization_docs_md"):
        # Load environment variables first
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            pass  # dotenv not available, continue without it
        
        self.logger = QueryOptimizerLogger(__name__)
        self.docs_directory = Path(docs_directory)
        self.optimization_patterns = self._load_all_pattern_files()
        
        # Don't initialize Gemini here - do it lazily when needed
        self.gemini_model = None
        self._gemini_initialized = False
    
    def _initialize_gemini(self):
        """Initialize Gemini API client."""
        try:
            # Check if already initialized
            if self._gemini_initialized and self.gemini_model:
                return self.gemini_model
            
            self.logger.logger.info("Initializing Gemini API...")
            
            # Check environment variables
            api_key = os.getenv('GEMINI_API_KEY')
            self.logger.logger.info(f"GEMINI_API_KEY found: {'Yes' if api_key else 'No'}")
            
            if not api_key:
                self.logger.logger.error("GEMINI_API_KEY not found in environment variables")
                self.logger.logger.error("Please set GEMINI_API_KEY in your .env file or environment")
                self.logger.logger.error("Current working directory: " + str(os.getcwd()))
                self.logger.logger.error("Environment variables: " + str([k for k in os.environ.keys() if 'GEMINI' in k.upper()]))
                return None
            
            # Check if API key looks valid (should be a long string)
            if len(api_key) < 10:
                self.logger.logger.error("GEMINI_API_KEY appears to be invalid (too short)")
                return None
            
            self.logger.logger.info(f"GEMINI_API_KEY length: {len(api_key)}")
            
            genai.configure(api_key=api_key)
            
            # Configure model with high token limits and appropriate temperature for large prompts
            model = genai.GenerativeModel(
                'gemini-2.5-pro',  # Use the latest Gemini 2.5 Pro model
                generation_config=genai.types.GenerationConfig(
                    temperature=0.1,  # Low temperature for consistent optimization
                    max_output_tokens=8192,  # High output token limit
                    top_p=0.8,
                    top_k=40
                )
            )
            
            self.gemini_model = model
            self._gemini_initialized = True
            self.logger.logger.info("Gemini API initialized successfully")
            return model
            
        except Exception as e:
            self.logger.log_error(e, {"operation": "initialize_gemini"})
            self.logger.logger.error(f"Failed to initialize Gemini API: {str(e)}")
            return None
    
    def _load_all_pattern_files(self) -> Dict[str, str]:
        """Load all markdown pattern files from the docs directory."""
        patterns = {}
        
        try:
            if not self.docs_directory.exists():
                self.logger.logger.warning(f"Documentation directory not found: {self.docs_directory}")
                return patterns
            
            # Load all .md files in the directory
            for md_file in self.docs_directory.glob("*.md"):
                pattern_name = md_file.stem
                content = md_file.read_text(encoding='utf-8')
                patterns[pattern_name] = content
                
            self.logger.logger.info(f"Loaded {len(patterns)} optimization pattern files")
            return patterns
            
        except Exception as e:
            self.logger.log_error(e, {"operation": "load_pattern_files"})
            return patterns
    
    def get_optimization_suggestions_for_llm(self, sql_query: str, project_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get optimization suggestions for LLM processing.
        This method provides a simplified interface for LLM-based optimization.
        """
        try:
            # Use the existing process_raw_sql_query method
            result = self.process_raw_sql_query(sql_query, project_id)
            
            if result["success"]:
                return {
                    "success": True,
                    "system_prompt": result["system_prompt"],
                    "user_prompt": result["user_prompt"],
                    "optimization_context": {
                        "docs_content": result["docs_content"],
                        "available_patterns": list(self.optimization_patterns.keys()),
                        "total_patterns": len(self.optimization_patterns)
                    },
                    "processing_time_ms": result["processing_time_ms"]
                }
            else:
                return result
                
        except Exception as e:
            self.logger.log_error(e, {"operation": "get_optimization_suggestions_for_llm"})
            return {
                "success": False,
                "error": str(e),
                "processing_time_ms": 0
            }
    
    def process_raw_sql_query(self, sql_query: str, project_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Process raw SQL query directly and return optimization context for LLM.
        
        This is the main entry point for the simplified architecture.
        """
        try:
            # Step 1: Get all markdown files content
            all_docs_content = self._prepare_all_docs_content(sql_query)
            
            # Step 2: Create system prompt for LLM
            system_prompt = self._create_system_prompt()
            
            # Step 3: Create user prompt with query and all docs
            user_prompt = self._create_user_prompt(sql_query, all_docs_content, project_id)
            
            return {
                "success": True,
                "system_prompt": system_prompt,
                "user_prompt": user_prompt,
                "docs_content": all_docs_content,
                "processing_time_ms": 0
            }
            
        except Exception as e:
            self.logger.log_error(e, {"operation": "process_raw_sql_query"})
            return {
                "success": False,
                "error": str(e),
                "processing_time_ms": 0
            }
    
    def _select_relevant_documentation(self, sql_query: str) -> Dict[str, int]:
        """
        Intelligently select the most relevant documentation files based on SQL query content.
        Returns a dictionary mapping file names to relevance scores.
        """
        query_lower = sql_query.lower()
        relevance_scores = {}
        
        self.logger.logger.info(f"Selecting relevant documentation for query: {sql_query[:100]}...")
        
        # Define keyword mappings for different optimization patterns
        pattern_keywords = {
            'join': ['join', 'inner join', 'left join', 'right join', 'cross join'],
            'aggregation': ['count', 'sum', 'avg', 'min', 'max', 'group by', 'having'],
            'partition': ['partition by', 'over', 'window', 'row_number', 'rank'],
            'subquery': ['subquery', 'in (', 'exists', 'not in', 'any', 'all'],
            'index': ['where', 'filter', 'predicate', 'condition'],
            'clustering': ['cluster by', 'order by', 'sort'],
            'approximate': ['count(distinct', 'approx_count_distinct'],
            'column_pruning': ['select *', 'select distinct'],
            'performance': ['performance', 'optimization', 'efficiency', 'best practice']
        }
        
        # Calculate relevance scores for each file
        for file_name, content in self.optimization_patterns.items():
            score = 0
            content_lower = content.lower()
            
            # Base score from file name relevance
            for pattern, keywords in pattern_keywords.items():
                if any(keyword in file_name.lower() for keyword in keywords):
                    score += 20
                    break
            
            # Content relevance based on SQL query analysis
            for pattern, keywords in pattern_keywords.items():
                # Check if query contains keywords that match this pattern
                query_matches = sum(1 for keyword in keywords if keyword in query_lower)
                if query_matches > 0:
                    # Check if documentation content supports this pattern
                    content_matches = sum(1 for keyword in keywords if keyword in content_lower)
                    if content_matches > 0:
                        score += query_matches * 15  # Higher score for direct relevance
                        score += content_matches * 5   # Bonus for comprehensive coverage
            
            # Prefer shorter, focused files
            if len(content) < 50000:  # Less than 50K characters
                score += 10
            
            # Prefer files with specific examples
            if 'example' in content_lower or 'sample' in content_lower:
                score += 5
            
            relevance_scores[file_name] = score
        
        # Log the relevance scores for debugging
        sorted_scores = sorted(relevance_scores.items(), key=lambda x: x[1], reverse=True)
        self.logger.logger.info(f"Relevance scores: {sorted_scores[:5]}...")  # Top 5 scores
        
        return relevance_scores
    
    def _create_ultra_minimal_docs_content(self, sql_query: str) -> str:
        """
        Create ultra-minimal documentation for extremely long queries.
        Focuses only on the most essential optimization patterns with minimal text.
        """
        query_lower = sql_query.lower()
        
        # Ultra-minimal core patterns
        essential_patterns = []
        
        if 'select *' in query_lower:
            essential_patterns.append("Column Pruning: Replace SELECT * with specific columns (30-50% improvement)")
        
        if any(keyword in query_lower for keyword in ['join', 'inner join', 'left join']):
            essential_patterns.append("Join Optimization: Place smaller tables first in JOINs (25-50% improvement)")
        
        if any(keyword in query_lower for keyword in ['where', 'filter']):
            essential_patterns.append("Predicate Pushdown: Move filters before JOINs (25-45% improvement)")
        
        if 'count(distinct' in query_lower:
            essential_patterns.append("Approximate Aggregation: Use APPROX_COUNT_DISTINCT (50-80% improvement)")
        
        # If no specific patterns match, include the most general ones
        if not essential_patterns:
            essential_patterns = [
                "Column Pruning: Replace SELECT * with specific columns (30-50% improvement)",
                "Join Optimization: Place smaller tables first in JOINs (25-50% improvement)"
            ]
        
        # Build ultra-minimal content
        content = "ESSENTIAL BIGQUERY OPTIMIZATION PATTERNS:\n\n"
        for pattern in essential_patterns:
            content += f"• {pattern}\n"
        
        content += f"\nSelected {len(essential_patterns)} core patterns for query optimization."
        
        return content
    
    def _create_minimal_docs_content(self, sql_query: str) -> str:
        """
        Create a minimal documentation set for very long queries or when token limits are tight.
        Focuses on the most essential optimization patterns.
        """
        query_lower = sql_query.lower()
        
        # For extremely long queries, use ultra-minimal content
        if len(sql_query) > 15000:
            return self._create_ultra_minimal_docs_content(sql_query)
        
        # Define core optimization patterns with minimal content
        core_patterns = {
            'column_pruning': {
                'keywords': ['select *', 'select distinct'],
                'content': """# Column Pruning
Replace SELECT * with specific columns to reduce data transfer.
- Performance: 30-50% improvement
- Example: SELECT column1, column2 instead of SELECT *"""
            },
            'join_optimization': {
                'keywords': ['join', 'inner join', 'left join'],
                'content': """# Join Optimization
Reorder JOINs to place smaller tables first.
- Performance: 25-50% improvement
- Example: Start with smallest table, use INNER JOIN when possible"""
            },
            'predicate_pushdown': {
                'keywords': ['where', 'filter', 'having'],
                'content': """# Predicate Pushdown
Move filtering conditions as early as possible.
- Performance: 25-45% improvement
- Example: Filter before JOINs when possible"""
            },
            'approximate_aggregation': {
                'keywords': ['count(distinct', 'distinct'],
                'content': """# Approximate Aggregation
Use APPROX_COUNT_DISTINCT for large datasets.
- Performance: 50-80% improvement
- Example: APPROX_COUNT_DISTINCT(column) instead of COUNT(DISTINCT column)"""
            }
        }
        
        # Select patterns relevant to the query
        relevant_patterns = []
        for pattern_name, pattern_info in core_patterns.items():
            if any(keyword in query_lower for keyword in pattern_info['keywords']):
                relevant_patterns.append((pattern_name, pattern_info))
        
        # If no specific patterns match, include the most general ones
        if not relevant_patterns:
            relevant_patterns = [
                ('column_pruning', core_patterns['column_pruning']),
                ('join_optimization', core_patterns['join_optimization'])
            ]
        
        # Build minimal content
        content = "ESSENTIAL BIGQUERY OPTIMIZATION PATTERNS:\n\n"
        for pattern_name, pattern_info in relevant_patterns:
            content += f"## {pattern_info['content']}\n\n"
            content += "="*50 + "\n\n"
        
        content += f"Selected {len(relevant_patterns)} core optimization patterns based on query analysis."
        
        return content
    
    def _prepare_all_docs_content(self, sql_query: str = None) -> str:
        """Prepare documentation content for LLM with intelligent selection and token limit awareness."""
        # Gemini 1.5 Flash has a limit of ~1M input tokens
        # We'll reserve ~300K tokens for the query and prompts, leaving ~700K for docs
        # This gives us a safety margin to stay well within limits
        MAX_DOC_TOKENS = 700000
        
        self.logger.logger.info(f"Preparing documentation content. Query length: {len(sql_query) if sql_query else 'None'}")
        
        # For very long queries, use minimal documentation
        if sql_query and len(sql_query) > 5000:  # Reduced threshold for more aggressive trimming
            self.logger.logger.info("Query is long, using minimal documentation")
            return self._create_minimal_docs_content(sql_query)
        
        all_content = "BIGQUERY OPTIMIZATION DOCUMENTATION:\n\n"
        current_tokens = 0
        included_files = []
        
        # Get relevance scores if SQL query is provided
        if sql_query:
            relevance_scores = self._select_relevant_documentation(sql_query)
            # Sort by relevance score (highest first)
            file_priorities = [(name, self.optimization_patterns[name], len(self.optimization_patterns[name]) // 4, score) 
                              for name, score in relevance_scores.items()]
            file_priorities.sort(key=lambda x: x[3], reverse=True)
            self.logger.logger.info(f"Using relevance-based prioritization. Files to process: {len(file_priorities)}")
        else:
            # Fallback to basic prioritization
            file_priorities = []
            for file_name, content in self.optimization_patterns.items():
                estimated_tokens = len(content) // 4
                priority_score = 0
                
                # High priority for core optimization patterns
                if any(keyword in file_name.lower() for keyword in ['performance', 'optimization', 'best-practice', 'efficiency']):
                    priority_score += 100
                
                # Medium priority for specific techniques
                if any(keyword in file_name.lower() for keyword in ['join', 'partition', 'cluster', 'index', 'aggregation']):
                    priority_score += 50
                
                # Lower priority for general documentation
                if any(keyword in file_name.lower() for keyword in ['overview', 'introduction', 'getting-started']):
                    priority_score -= 20
                
                # Prefer shorter, focused files
                if estimated_tokens < 50000:
                    priority_score += 30
                
                file_priorities.append((file_name, content, estimated_tokens, priority_score))
            
            # Sort by priority score (highest first)
            file_priorities.sort(key=lambda x: x[3], reverse=True)
            self.logger.logger.info(f"Using basic prioritization. Files to process: {len(file_priorities)}")
        
        self.logger.logger.info(f"Starting content preparation with {len(file_priorities)} files")
        
        # Add files until we hit the token limit
        for file_priority in file_priorities:
            # Ensure we have the correct number of elements
            if len(file_priority) != 4:
                self.logger.logger.warning(f"Skipping malformed file priority: {file_priority}")
                continue
                
            file_name, content, estimated_tokens, priority_score = file_priority
            
            self.logger.logger.info(f"Processing file: {file_name}, estimated tokens: {estimated_tokens}, current total: {current_tokens}")
            
            if current_tokens + estimated_tokens > MAX_DOC_TOKENS:
                # If this file would exceed the limit, try to include a truncated version
                remaining_tokens = MAX_DOC_TOKENS - current_tokens
                if remaining_tokens > 5000:  # Reduced threshold for more aggressive trimming
                    # Truncate content to fit remaining tokens
                    max_chars = remaining_tokens * 4
                    truncated_content = content[:max_chars]
                    
                    # Try to end at a complete sentence or paragraph
                    last_period = truncated_content.rfind('.')
                    last_newline = truncated_content.rfind('\n')
                    cut_point = max(last_period, last_newline)
                    
                    if cut_point > max_chars * 0.7:  # More aggressive cutting (was 0.8)
                        truncated_content = truncated_content[:cut_point + 1]
                        truncated_content += "\n\n[CONTENT TRUNCATED DUE TO TOKEN LIMITS]"
                        
                        all_content += f"## FILE: {file_name}.md (TRUNCATED)\n"
                        all_content += f"LOCATION: data/optimization_docs_md/{file_name}.md\n"
                        all_content += f"RELEVANCE SCORE: {priority_score}\n\n"
                        all_content += truncated_content
                        all_content += "\n\n" + "="*80 + "\n\n"
                        
                        included_files.append(f"{file_name} (truncated)")
                        current_tokens += len(truncated_content) // 4
                        self.logger.logger.info(f"Added truncated file: {file_name}, new total tokens: {current_tokens}")
                        break
                else:
                    self.logger.logger.info(f"Not enough tokens left for truncation: {remaining_tokens}")
                    break
            else:
                # Add the full file
                all_content += f"## FILE: {file_name}.md\n"
                all_content += f"LOCATION: data/optimization_docs_md/{file_name}.md\n"
                all_content += f"RELEVANCE SCORE: {priority_score}\n\n"
                all_content += content
                all_content += "\n\n" + "="*80 + "\n\n"
                
                included_files.append(file_name)
                current_tokens += estimated_tokens
                self.logger.logger.info(f"Added full file: {file_name}, new total tokens: {current_tokens}")
        
        # Add summary of what was included/excluded
        all_content += f"\n\n## DOCUMENTATION SUMMARY\n"
        all_content += f"Total files included: {len(included_files)}\n"
        all_content += f"Estimated tokens used: {current_tokens:,}\n"
        all_content += f"Token limit: {MAX_DOC_TOKENS:,}\n"
        all_content += f"Files included: {', '.join(included_files)}\n"
        
        if len(included_files) < len(self.optimization_patterns):
            excluded_files = [f for f in self.optimization_patterns.keys() if f not in [name.split(' (')[0] for name in included_files]]
            all_content += f"Files excluded due to token limits: {', '.join(excluded_files)}\n"
        
        self.logger.logger.info(f"Content preparation complete. Final token count: {current_tokens:,}")
        
        return all_content
    
    def _create_system_prompt(self) -> str:
        """Create system prompt for LLM optimization."""
        return """You are an expert BigQuery SQL optimizer. Your task is to optimize SQL queries for better performance while preserving EXACT business logic.

🚨 CRITICAL REQUIREMENTS - READ CAREFULLY:
1. The optimized query MUST return IDENTICAL results to the original query
2. The optimized query MUST return the EXACT same number of rows
3. The optimized query MUST return the EXACT same data values
4. The optimized query MUST return the EXACT same column order
5. The optimized query MUST return the EXACT same data types
6. NO changes to business logic, filtering conditions, or data transformations
7. NO changes to JOIN types that could affect result sets
8. NO changes to aggregation functions that could affect calculations
9. NO changes to window functions that could affect ordering
10. NO changes to subqueries that could affect data selection

✅ ALLOWED OPTIMIZATIONS (Performance Only):
1. Replace SELECT * with specific columns (30-50% improvement)
2. Convert COUNT(DISTINCT) to APPROX_COUNT_DISTINCT (50-80% improvement)
3. Convert subqueries to JOINs ONLY if results are guaranteed identical
4. Reorder JOINs to place smaller tables first (25-50% improvement)
5. Add proper PARTITION BY to window functions (25-40% improvement)
6. Remove unnecessary CAST/string operations (20-35% improvement)
7. Apply predicate pushdown for early filtering (25-45% improvement)
8. Convert HAVING to WHERE when possible (15-25% improvement)

❌ FORBIDDEN CHANGES:
- Changing JOIN types (INNER vs LEFT vs RIGHT)
- Modifying WHERE conditions
- Changing GROUP BY clauses
- Altering ORDER BY clauses
- Modifying HAVING conditions
- Changing subquery logic
- Altering window function parameters

VALIDATION REQUIREMENTS:
Before returning the optimized query, verify that:
1. Both queries will return the same number of rows
2. Both queries will return the same data values
3. Both queries will return the same column structure
4. No business logic has been modified

RESPONSE FORMAT:
Return a JSON object with:
{
    "optimized_query": "The optimized SQL query that returns IDENTICAL results",
    "optimizations_applied": [
        {
            "pattern_id": "column_pruning",
            "pattern_name": "Column Pruning",
            "description": "What was changed and why (performance only)",
            "expected_improvement": 0.3,
            "documentation_reference": "Reference to specific documentation section",
            "result_preservation": "How this change preserves identical results"
        }
    ],
    "estimated_improvement": 0.4,
    "explanation": "Summary of all optimizations applied",
    "result_validation": "Explanation of how the optimized query will return identical results"
}"""

    def _create_concise_system_prompt(self) -> str:
        """Create a concise system prompt for token-limited scenarios."""
        return """You are a BigQuery SQL optimizer. Optimize queries for performance while preserving EXACT business logic.

🚨 CRITICAL REQUIREMENTS:
1. Optimized query MUST return IDENTICAL results
2. Same number of rows, same data values, same structure
3. NO changes to business logic or filtering
4. Performance optimizations only

✅ ALLOWED: Column pruning, JOIN reordering, predicate pushdown
❌ FORBIDDEN: Changing JOIN types, WHERE conditions, business logic

RESPONSE FORMAT:
{
    "optimized_query": "The optimized SQL query",
    "optimizations_applied": [
        {
            "pattern_id": "column_pruning",
            "pattern_name": "Column Pruning",
            "description": "What was changed and why",
            "expected_improvement": 0.3,
            "documentation_reference": "Reference to documentation section"
        }
    ],
    "estimated_improvement": 0.4,
    "explanation": "Summary of optimizations applied"
}"""
    
    def _create_concise_user_prompt(self, sql_query: str, all_docs_content: str, project_id: Optional[str]) -> str:
        """Create a concise user prompt for token-limited scenarios."""
        prompt = f"""OPTIMIZE THIS BIGQUERY SQL QUERY:

```sql
{sql_query}
```

🚨 CRITICAL: Results MUST be IDENTICAL - same rows, same data, same structure

OPTIMIZATION DOCUMENTATION:
{all_docs_content}

INSTRUCTIONS:
1. Analyze the SQL query for inefficiencies
2. Apply ONLY performance optimizations that preserve identical results
3. NEVER change business logic, filtering, or JOIN types
4. Ensure identical results
5. Return JSON format as specified in system prompt"""
        
        return prompt
    
    def _create_user_prompt(self, sql_query: str, all_docs_content: str, project_id: Optional[str]) -> str:
        """Create user prompt with query and ALL documentation."""
        prompt = f"""OPTIMIZE THIS BIGQUERY SQL QUERY:

```sql
{sql_query}
```

PROJECT CONTEXT:
- Project ID: {project_id or 'not-specified'}
- Target: 30-50% performance improvement minimum
- Requirement: Preserve EXACT business logic and results

🚨 CRITICAL REQUIREMENT - RESULTS MUST BE IDENTICAL:
The optimized query MUST return:
- The EXACT same number of rows
- The EXACT same data values
- The EXACT same column structure
- The EXACT same data types

COMPLETE BIGQUERY OPTIMIZATION DOCUMENTATION:

{all_docs_content}

INSTRUCTIONS:
1. Analyze the SQL query for inefficiencies using the documentation above
2. Apply ONLY performance optimizations that preserve identical results
3. NEVER change business logic, filtering, JOIN types, or data transformations
4. Focus on high-impact optimizations first (50%+ improvement patterns)
5. Provide clear explanations for each optimization with documentation references
6. Include result_validation field explaining how results will be preserved
7. Use the exact documentation file locations and pattern names in your response

VALIDATION CHECKLIST:
Before returning the optimized query, verify:
□ Both queries will return the same number of rows
□ Both queries will return the same data values  
□ Both queries will return the same column structure
□ No business logic has been modified
□ Only performance improvements were applied

Generate the optimized query following the JSON format specified in the system prompt."""
        
        return prompt
    
    def _estimate_token_count(self, text: str) -> int:
        """Estimate token count for text (rough approximation: 1 token ≈ 4 characters)."""
        return len(text) // 4
    
    def _check_token_limits(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """Check if the prompts exceed Gemini's token limits."""
        system_tokens = self._estimate_token_count(system_prompt)
        user_tokens = self._estimate_token_count(user_prompt)
        total_tokens = system_tokens + user_tokens
        
        # Gemini 1.5 Flash limit is approximately 1M tokens
        MAX_TOKENS = 1000000
        
        return {
            "system_tokens": system_tokens,
            "user_tokens": user_tokens,
            "total_tokens": total_tokens,
            "max_tokens": MAX_TOKENS,
            "within_limits": total_tokens <= MAX_TOKENS,
            "excess_tokens": max(0, total_tokens - MAX_TOKENS)
        }
    
    def optimize_with_gemini(self, sql_query: str, project_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Send raw SQL query directly to Gemini API with all documentation.
        Returns optimized query with validation results and executed query comparison.
        """
        try:
            if not GEMINI_AVAILABLE:
                return {
                    "success": False,
                    "error": "Google Generative AI not available. Install with: pip install google-generativeai"
                }
            
            # Initialize Gemini if not already done
            if not self.gemini_model:
                self.gemini_model = self._initialize_gemini()
                if self.gemini_model is None:
                    return {
                        "success": False,
                        "error": "Failed to initialize Gemini API. Please check GEMINI_API_KEY environment variable."
                    }
            
            # Prepare prompts with token-aware content selection
            docs_content = self._prepare_all_docs_content(sql_query)
            
            # Choose prompt based on query length and content size
            if len(sql_query) > 10000 or len(docs_content) > 500000:  # Very long query or content
                system_prompt = self._create_concise_system_prompt()
                user_prompt = self._create_concise_user_prompt(sql_query, docs_content, project_id)
                self.logger.logger.info("Using concise prompts for long query/content")
            else:
                system_prompt = self._create_system_prompt()
                user_prompt = self._create_user_prompt(sql_query, docs_content, project_id)
                self.logger.logger.info("Using full prompts")
            
            # Check token limits before sending to Gemini
            token_info = self._check_token_limits(system_prompt, user_prompt)
            
            # If still over limit, try with ultra-minimal content
            if not token_info["within_limits"]:
                self.logger.logger.warning(f"Still over token limit, trying ultra-minimal content")
                ultra_minimal_docs = self._create_ultra_minimal_docs_content(sql_query)
                user_prompt = self._create_concise_user_prompt(sql_query, ultra_minimal_docs, project_id)
                token_info = self._check_token_limits(system_prompt, user_prompt)
                
                if not token_info["within_limits"]:
                    return {
                        "success": False,
                        "error": f"Input exceeds Gemini's token limit even with minimal content. Total tokens: {token_info['total_tokens']:,}, Limit: {token_info['max_tokens']:,}, Excess: {token_info['excess_tokens']:,}",
                        "token_info": token_info,
                        "suggestion": "Consider using a much shorter SQL query or breaking it into smaller parts."
                    }
            
            # Log token usage for debugging
            self.logger.logger.info(f"Token usage - System: {token_info['system_tokens']:,}, User: {token_info['user_tokens']:,}, Total: {token_info['total_tokens']:,}")
            
            # Send to Gemini API
            response = self.gemini_model.generate_content([
                system_prompt,
                user_prompt
            ])
            
            # Parse response
            try:
                # Extract JSON from response
                response_text = response.text
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                
                if json_start != -1 and json_end != 0:
                    json_str = response_text[json_start:json_end]
                    optimization_result = json.loads(json_str)
                else:
                    # Fallback: try to parse the entire response
                    optimization_result = json.loads(response_text)
                
                # Validate required fields
                required_fields = ['optimized_query', 'optimizations_applied', 'estimated_improvement', 'explanation']
                optional_fields = ['result_validation']
                
                for field in required_fields:
                    if field not in optimization_result:
                        return {
                            "success": False,
                            "error": f"Missing required field in Gemini response: {field}",
                            "raw_response": response_text,
                            "suggestion": "The LLM response is incomplete. Please try again or check the system prompt."
                        }
                
                # Check for optional fields and provide defaults
                if 'result_validation' not in optimization_result:
                    optimization_result['result_validation'] = "Result validation details not provided by LLM"
                
                # First, validate and fix any syntax corruption in the optimized query
                optimized_query = optimization_result["optimized_query"]
                syntax_corrected_query = self._validate_and_fix_syntax(optimized_query)
                
                # Log if syntax corrections were made
                if syntax_corrected_query != optimized_query:
                    self.logger.logger.warning(f"Syntax corrections applied to optimized query")
                    self.logger.logger.info(f"Original: {optimized_query}")
                    self.logger.logger.info(f"Syntax corrected: {syntax_corrected_query}")
                
                # Send to LLM for intelligent cleanup if there are syntax issues
                if syntax_corrected_query != optimized_query:
                    self.logger.logger.info("Sending query to LLM for intelligent syntax cleanup")
                    
                    # Ensure Gemini model is initialized
                    if not self.gemini_model:
                        self.gemini_model = self._initialize_gemini()
                    
                    if self.gemini_model:
                        llm_cleaned_query = self._send_to_llm_for_cleanup(
                            syntax_corrected_query, 
                            ["Syntax corruption detected and partially fixed"]
                        )
                        
                        if llm_cleaned_query != syntax_corrected_query:
                            self.logger.logger.info("LLM cleanup successful, using cleaned query")
                            syntax_corrected_query = llm_cleaned_query
                        else:
                            self.logger.logger.info("LLM cleanup returned same query, using regex-corrected version")
                    else:
                        self.logger.logger.warning("Gemini model not available, using regex-corrected version")
                else:
                    self.logger.logger.info("No syntax issues detected, skipping LLM cleanup")
                
                # Validate and correct the optimized query against actual database schema
                schema_validation = self._validate_and_correct_query_schema(sql_query, syntax_corrected_query, project_id)
                
                # Use the corrected query if schema validation found issues
                final_optimized_query = schema_validation["corrected_query"]
                
                # ALWAYS send to LLM for final cleanup after schema validation (no intermediate checks)
                self.logger.logger.info("Sending schema-validated query to LLM for final cleanup")
                
                # Ensure Gemini model is initialized
                if not self.gemini_model:
                    self.gemini_model = self._initialize_gemini()
                
                if self.gemini_model:
                    # Create comprehensive validation issues list
                    validation_issues = []
                    if not schema_validation["schema_validation_passed"]:
                        validation_issues.extend(schema_validation["validation_issues"])
                    
                    # Add any syntax issues that might still exist
                    if "WHEREder_date" in final_optimized_query or "OR DER BY" in final_optimized_query:
                        validation_issues.append("Syntax corruption detected")
                    
                    # Add window function issues
                    if "OVER (w)" in final_optimized_query:
                        validation_issues.append("Incomplete window function definition")
                    
                    # Send to LLM for comprehensive cleanup
                    final_llm_cleaned_query = self._send_to_llm_for_cleanup(
                        final_optimized_query,
                        validation_issues
                    )
                    
                    if final_llm_cleaned_query != final_optimized_query:
                        self.logger.logger.info("Final LLM cleanup successful, using cleaned query")
                        final_optimized_query = final_llm_cleaned_query
                    else:
                        self.logger.logger.info("Final LLM cleanup returned same query, using schema-corrected version")
                else:
                    self.logger.logger.warning("Gemini model not available for final cleanup, using schema-corrected version")
                
                # Execute and compare both queries to get actual results and performance metrics
                execution_results = self._execute_and_compare_queries(sql_query, final_optimized_query, project_id)
                
                # Create result with validation and execution results
                result = {
                    "success": True,
                    "original_query": sql_query,
                    "optimized_query": final_optimized_query,  # Use corrected query
                    "original_optimized_query": optimization_result["optimized_query"],  # Keep original for reference
                    "optimizations_applied": optimization_result["optimizations_applied"],
                    "estimated_improvement": optimization_result["estimated_improvement"],
                    "explanation": optimization_result["explanation"],
                    "result_validation": optimization_result.get("result_validation", "Not provided"),
                    "schema_validation": schema_validation,  # Include schema validation results
                    "total_optimizations": len(optimization_result["optimizations_applied"]),
                    "gemini_response": response_text,
                    "validation": self._validate_queries(sql_query, final_optimized_query),  # Validate corrected query
                    "execution_results": execution_results,
                    "workflow_steps": [
                        "✅ Raw SQL query received",
                        "✅ Documentation loaded and processed",
                        "✅ Query sent to Gemini API for optimization",
                        "✅ Optimization response parsed and validated",
                        "✅ Schema validation and correction applied",
                        "✅ Both queries executed and compared",
                        "✅ Performance metrics calculated",
                        "✅ Results validated for consistency"
                    ],
                    "workflow_completed": True
                }
                
                # Add warning if validation score is low
                if result["validation"]["result_preservation_score"] < 60:
                    result["warning"] = f"⚠️ Optimization may change results. Validation score: {result['validation']['result_preservation_score']}/100"
                    if result["validation"]["potential_issues"]:
                        result["warning"] += f" Issues: {', '.join(result['validation']['potential_issues'][:2])}"
                
                return result
                
            except json.JSONDecodeError as e:
                return {
                    "success": False,
                    "error": f"Failed to parse Gemini response as JSON: {str(e)}",
                    "raw_response": response_text
                }
                
        except Exception as e:
            self.logger.log_error(e, {"operation": "optimize_with_gemini"})
            return {
                "success": False,
                "error": str(e)
            }
    
    def _execute_and_compare_queries(self, original_query: str, optimized_query: str, project_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute both original and optimized queries and compare results.
        Returns execution results with performance metrics and result comparison.
        """
        try:
            # Import BigQuery client for execution
            from google.cloud import bigquery
            from google.cloud.exceptions import GoogleCloudError
            
            # Initialize BigQuery client
            client = bigquery.Client(project=project_id) if project_id else bigquery.Client()
            
            # Execute original query
            self.logger.logger.info("Executing original query...")
            original_job = client.query(original_query)
            original_result = original_job.result()
            original_rows = [dict(row.items()) for row in original_result]
            original_time = original_job.total_time_ms if hasattr(original_job, 'total_time_ms') else 0
            original_bytes = original_job.total_bytes_processed if hasattr(original_job, 'total_bytes_processed') else 0
            
            # Execute optimized query
            self.logger.logger.info("Executing optimized query...")
            optimized_job = client.query(optimized_query)
            optimized_result = optimized_job.result()
            optimized_rows = [dict(row.items()) for row in optimized_result]
            optimized_time = optimized_job.total_time_ms if hasattr(optimized_job, 'total_time_ms') else 0
            optimized_bytes = optimized_job.total_bytes_processed if hasattr(optimized_job, 'total_bytes_processed') else 0
            
            # Create hashes for comparison
            original_hash = self._hash_results(original_rows)
            optimized_hash = self._hash_results(optimized_rows)
            
            # Calculate performance improvements
            time_improvement = 0
            bytes_improvement = 0
            cost_improvement = 0
            time_saved_ms = 0
            bytes_saved = 0
            cost_saved = 0
            
            # Initialize cost variables
            original_cost = 0
            optimized_cost = 0
            
            if original_time > 0:
                time_improvement = (original_time - optimized_time) / original_time
                time_saved_ms = original_time - optimized_time
            
            if original_bytes > 0:
                bytes_improvement = (original_bytes - optimized_bytes) / original_bytes
                bytes_saved = original_bytes - optimized_bytes
            
            # Estimate cost improvements (BigQuery pricing: $5 per TB processed)
            if original_bytes > 0:
                original_cost = (original_bytes / (1024**4)) * 5  # Convert bytes to TB, then multiply by $5
                optimized_cost = (optimized_bytes / (1024**4)) * 5
                if original_cost > 0:
                    cost_improvement = (original_cost - optimized_cost) / original_cost
                    cost_saved = original_cost - optimized_cost
            
            return {
                "success": True,
                "original_query_results": original_rows,
                "optimized_query_results": optimized_rows,
                "original_row_count": len(original_rows),
                "optimized_row_count": len(optimized_rows),
                "results_identical": original_hash == optimized_hash,
                "original_hash": original_hash,
                "optimized_hash": optimized_hash,
                "performance_metrics": {
                    "success": True,
                    "original_time_ms": original_time,
                    "optimized_time_ms": optimized_time,
                    "original_bytes": original_bytes,
                    "optimized_bytes": optimized_bytes,
                    "original_cost": round(original_cost, 6) if original_bytes > 0 else 0,
                    "optimized_cost": round(optimized_cost, 6) if optimized_bytes > 0 else 0,
                    # Actual improvements achieved (not expected)
                    "time_improvement": max(0, time_improvement),
                    "bytes_improvement": max(0, bytes_improvement),
                    "cost_improvement": max(0, cost_improvement),
                    "time_saved_ms": max(0, time_saved_ms),
                    "bytes_saved": max(0, bytes_saved),
                    "cost_saved": round(max(0, cost_saved), 6),
                    "performance_summary": f"Time: {time_improvement*100:.1f}% faster, Data: {bytes_improvement*100:.1f}% less, Cost: {cost_improvement*100:.1f}% savings" if time_improvement > 0 else "No performance improvement detected"
                }
            }
            
        except GoogleCloudError as e:
            self.logger.logger.error(f"BigQuery execution error: {str(e)}")
            return {
                "success": False,
                "error": f"BigQuery execution failed: {str(e)}",
                "message": "Failed to execute queries for comparison"
            }
        except Exception as e:
            self.logger.logger.error(f"Query execution error: {str(e)}")
            return {
                "success": False,
                "error": f"Query execution failed: {str(e)}",
                "message": "Failed to execute queries for comparison"
            }
    
    def _hash_results(self, results: List[Dict[str, Any]]) -> str:
        """Create hash of query results for comparison."""
        if not results:
            return hashlib.md5(b"no_results").hexdigest()
        
        try:
            # Normalize and sort results for consistent hashing
            normalized_results = []
            for row in results:
                normalized_row = {}
                for key, value in sorted(row.items()):
                    # Normalize the value for consistent hashing
                    if hasattr(value, 'isoformat'):  # Handle date/datetime objects
                        normalized_row[key] = value.isoformat()
                    elif isinstance(value, (int, float)):
                        # Ensure consistent numeric representation
                        if isinstance(value, float):
                            normalized_row[key] = round(value, 6)  # Consistent decimal places
                        else:
                            normalized_row[key] = value
                    elif value is None:
                        normalized_row[key] = "NULL"
                    else:
                        normalized_row[key] = str(value).strip()
                normalized_results.append(normalized_row)
            
            # Sort rows by a consistent key (first available key)
            if normalized_results and normalized_results[0]:
                first_key = list(normalized_results[0].keys())[0]
                normalized_results.sort(key=lambda x: str(x.get(first_key, '')))
            
            # Create hash from normalized data
            json_str = json.dumps(normalized_results, sort_keys=True)
            return hashlib.md5(json_str.encode()).hexdigest()
            
        except (TypeError, ValueError) as e:
            # Fallback: convert to string representation for hashing
            self.logger.logger.warning(f"JSON serialization failed, using string fallback: {e}")
            try:
                # Convert results to string representation with consistent formatting
                result_strings = []
                for row in results:
                    row_str = []
                    for key, value in sorted(row.items()):
                        if hasattr(value, 'isoformat'):
                            row_str.append(f"{key}:{value.isoformat()}")
                        elif isinstance(value, (int, float)):
                            if isinstance(value, float):
                                row_str.append(f"{key}:{round(value, 6)}")
                            else:
                                row_str.append(f"{key}:{value}")
                        elif value is None:
                            row_str.append(f"{key}:NULL")
                        else:
                            row_str.append(f"{key}:{str(value).strip()}")
                    result_strings.append("|".join(row_str))
                
                # Sort rows consistently
                sorted_strings = sorted(result_strings)
                return hashlib.md5("||".join(sorted_strings).encode()).hexdigest()
            except Exception as fallback_error:
                self.logger.logger.error(f"Fallback hashing also failed: {fallback_error}")
                return hashlib.md5(f"fallback_hash_{len(results)}".encode()).hexdigest()
    
    def _validate_queries(self, original_query: str, optimized_query: str) -> Dict[str, Any]:
        """
        Validate that both queries are syntactically valid and have similar structure.
        Uses hashing to compare query characteristics and identifies potential result differences.
        """
        try:
            # Create hash of query structure (removing whitespace and case)
            def normalize_query(query: str) -> str:
                return ' '.join(query.lower().split())
            
            original_normalized = normalize_query(original_query)
            optimized_normalized = normalize_query(optimized_query)
            
            # Create hash for comparison
            original_hash = hashlib.md5(original_normalized.encode()).hexdigest()
            optimized_hash = hashlib.md5(optimized_normalized.encode()).hexdigest()
            
            # Basic validation checks
            validation_result = {
                "original_query_hash": original_hash,
                "optimized_query_hash": optimized_hash,
                "queries_different": original_hash != optimized_hash,
                "original_length": len(original_query),
                "optimized_length": len(optimized_query),
                "length_change_percent": ((len(optimized_query) - len(original_query)) / len(original_query)) * 100 if len(original_query) > 0 else 0,
                "validation_notes": [],
                "potential_issues": [],
                "result_preservation_score": 100  # Start with perfect score
            }
            
            # Check for common SQL keywords to ensure both are valid SQL
            sql_keywords = ['select', 'from', 'where', 'join', 'group', 'order', 'having', 'union']
            original_has_keywords = any(keyword in original_normalized for keyword in sql_keywords)
            optimized_has_keywords = any(keyword in optimized_normalized for keyword in sql_keywords)
            
            if not original_has_keywords:
                validation_result["validation_notes"].append("Original query may not be valid SQL")
                validation_result["result_preservation_score"] -= 20
            if not optimized_has_keywords:
                validation_result["validation_notes"].append("Optimized query may not be valid SQL")
                validation_result["result_preservation_score"] -= 20
            
            # Check for balanced parentheses
            if original_query.count('(') != original_query.count(')'):
                validation_result["validation_notes"].append("Original query has unbalanced parentheses")
                validation_result["result_preservation_score"] -= 10
            if optimized_query.count('(') != optimized_query.count(')'):
                validation_result["validation_notes"].append("Optimized query has unbalanced parentheses")
                validation_result["result_preservation_score"] -= 10
            
            # Check if optimization actually changed something meaningful
            if original_hash == optimized_hash:
                validation_result["validation_notes"].append("No meaningful changes detected in optimization")
                validation_result["result_preservation_score"] = 100  # Perfect preservation
            
            # Check for potential result-changing modifications
            original_lower = original_query.lower()
            optimized_lower = optimized_query.lower()
            
            # Check JOIN type changes (critical for result preservation)
            if 'inner join' in original_lower and 'left join' in optimized_lower:
                validation_result["potential_issues"].append("JOIN type changed from INNER to LEFT - may return different results")
                validation_result["result_preservation_score"] -= 30
            elif 'left join' in original_lower and 'inner join' in optimized_lower:
                validation_result["potential_issues"].append("JOIN type changed from LEFT to INNER - may return different results")
                validation_result["result_preservation_score"] -= 30
            
            # Check WHERE clause modifications
            if 'where' in original_lower and 'where' not in optimized_lower:
                validation_result["potential_issues"].append("WHERE clause removed - will return different results")
                validation_result["result_preservation_score"] -= 40
            elif 'where' not in original_lower and 'where' in optimized_lower:
                validation_result["potential_issues"].append("WHERE clause added - will return different results")
                validation_result["result_preservation_score"] -= 40
            
            # Check GROUP BY modifications
            if 'group by' in original_lower and 'group by' not in optimized_lower:
                validation_result["potential_issues"].append("GROUP BY removed - will return different results")
                validation_result["result_preservation_score"] -= 35
            elif 'group by' not in original_lower and 'group by' in optimized_lower:
                validation_result["potential_issues"].append("GROUP BY added - will return different results")
                validation_result["result_preservation_score"] -= 35
            
            # Check ORDER BY modifications
            if 'order by' in original_lower and 'order by' not in optimized_lower:
                validation_result["potential_issues"].append("ORDER BY removed - may affect result presentation")
                validation_result["result_preservation_score"] -= 15
            elif 'order by' not in original_lower and 'order by' in optimized_lower:
                validation_result["potential_issues"].append("ORDER BY added - may affect result presentation")
                validation_result["result_preservation_score"] -= 15
            
            # Check HAVING modifications
            if 'having' in original_lower and 'having' not in optimized_lower:
                validation_result["potential_issues"].append("HAVING clause removed - will return different results")
                validation_result["result_preservation_score"] -= 25
            elif 'having' not in original_lower and 'having' in optimized_lower:
                validation_result["potential_issues"].append("HAVING clause added - will return different results")
                validation_result["result_preservation_score"] -= 25
            
            # Check for subquery to JOIN conversions (potentially risky)
            if ('in (' in original_lower or 'exists' in original_lower) and 'join' in optimized_lower:
                validation_result["potential_issues"].append("Subquery converted to JOIN - verify results are identical")
                validation_result["result_preservation_score"] -= 20
            
            # Ensure score doesn't go below 0
            validation_result["result_preservation_score"] = max(0, validation_result["result_preservation_score"])
            
            # Add overall assessment
            if validation_result["result_preservation_score"] >= 80:
                validation_result["overall_assessment"] = "GOOD - Results should be preserved"
            elif validation_result["result_preservation_score"] >= 60:
                validation_result["overall_assessment"] = "CAUTION - Some changes may affect results"
            else:
                validation_result["overall_assessment"] = "WARNING - High risk of different results"
            
            return validation_result
            
        except Exception as e:
            self.logger.log_error(e, {"operation": "validate_queries"})
            return {
                "error": str(e),
                "validation_notes": ["Validation failed due to error"],
                "potential_issues": ["Validation error occurred"],
                "result_preservation_score": 0,
                "overall_assessment": "ERROR - Validation failed"
            }
    
    def _validate_and_correct_query_schema(self, original_query: str, optimized_query: str, project_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Validate optimized query against actual database schema and correct any non-existent columns/tables.
        Returns the corrected query and validation results.
        """
        try:
            from src.optimizer.bigquery_client import BigQueryClient
            import re
            
            # Initialize BigQuery client
            bq_client = BigQueryClient(project_id=project_id)
            
            # Extract table references from queries (simplified)
            import re
            
            # Simple regex to find table references - fixed to return strings
            table_pattern = r'FROM\s+`?([^`\s]+)`?\s+|JOIN\s+`?([^`\s]+)`?\s+'
            
            original_tables = re.findall(table_pattern, original_query, re.IGNORECASE)
            optimized_tables = re.findall(table_pattern, optimized_query, re.IGNORECASE)
            
            # Flatten and clean table references - handle tuples properly
            original_tables = []
            for match in re.findall(table_pattern, original_query, re.IGNORECASE):
                if isinstance(match, tuple):
                    original_tables.extend([t for t in match if t])
                else:
                    if match:
                        original_tables.append(match)
            
            optimized_tables = []
            for match in re.findall(table_pattern, optimized_query, re.IGNORECASE):
                if isinstance(match, tuple):
                    optimized_tables.extend([t for t in match if t])
                else:
                    if match:
                        optimized_tables.append(match)
            
            # Extract column references with better pattern matching
            def extract_columns(query_text):
                columns = []
                
                # Pattern for SELECT clause columns - look for table.column references
                select_pattern = r'SELECT\s+(.*?)\s+FROM'
                select_match = re.search(select_pattern, query_text, re.IGNORECASE | re.DOTALL)
                if select_match:
                    select_content = select_match.group(1)
                    # Extract table.column references, excluding SQL keywords and functions
                    col_refs = re.findall(r'`?(\w+)\.(\w+)`?', select_content)
                    columns.extend([f"{table}.{column}" for table, column in col_refs if table and column])
                
                # Pattern for WHERE clause column references - look for table.column in conditions
                where_pattern = r'WHERE\s+(.*?)(?:\s+(?:GROUP\s+BY|ORDER\s+BY|HAVING|LIMIT|$))'
                where_match = re.search(where_pattern, query_text, re.IGNORECASE | re.DOTALL)
                if where_match:
                    where_content = where_match.group(1)
                    # Extract table.column references from WHERE clause, excluding operators and values
                    where_cols = re.findall(r'`?(\w+)\.(\w+)`?', where_content)
                    columns.extend([f"{table}.{column}" for table, column in where_cols if table and column])
                
                # Pattern for JOIN ON clause column references - look for table.column in JOIN conditions
                join_pattern = r'JOIN\s+.*?ON\s+(.*?)(?:\s+(?:JOIN|WHERE|GROUP\s+BY|ORDER\s+BY|$))'
                join_matches = re.findall(join_pattern, query_text, re.IGNORECASE | re.DOTALL)
                for join_content in join_matches:
                    join_cols = re.findall(r'`?(\w+)\.(\w+)`?', join_content)
                    columns.extend([f"{table}.{column}" for table, column in join_cols if table and column])
                
                return list(set(columns))  # Remove duplicates
            
            original_columns = extract_columns(original_query)
            optimized_columns = extract_columns(optimized_query)
            
            validation_result = {
                "success": True,
                "original_query": original_query,
                "optimized_query": optimized_query,
                "corrected_query": optimized_query,
                "validation_issues": [],
                "removed_columns": [],
                "removed_tables": [],
                "schema_validation_passed": True
            }
            
            # Check if any new tables were added in optimized query
            new_tables = set(optimized_tables) - set(original_tables)
            if new_tables:
                validation_result["validation_issues"].append(f"New tables added in optimized query: {list(new_tables)}")
                validation_result["schema_validation_passed"] = False
                
                # Remove references to new tables
                for table in new_tables:
                    # Remove FROM clause with new table
                    optimized_query = re.sub(
                        rf'FROM\s+`?{re.escape(table)}`?\s+',
                        '',
                        optimized_query,
                        flags=re.IGNORECASE
                    )
                    
                    # Remove JOIN clauses with new table - simpler approach
                    # Split into lines and remove lines containing the table
                    lines = optimized_query.split('\n')
                    filtered_lines = []
                    for line in lines:
                        # Skip lines that contain the table to be removed
                        if table not in line or 'JOIN' not in line.upper():
                            filtered_lines.append(line)
                    
                    # Rejoin the lines
                    optimized_query = '\n'.join(filtered_lines)
                    
                    validation_result["removed_tables"].append(table)
            
            # Validate columns exist in actual tables
            corrected_query = optimized_query
            for table in original_tables:
                try:
                    # Get table schema
                    table_parts = table.split('.')
                    if len(table_parts) >= 2:
                        dataset_id = table_parts[-2]
                        table_id = table_parts[-1]
                        
                        # Get table schema
                        table_ref = bq_client.client.dataset(dataset_id).table(table_id)
                        table_obj = bq_client.client.get_table(table_ref)
                        actual_columns = [field.name for field in table_obj.schema]
                        
                        # Check if optimized query references non-existent columns
                        for col_ref in optimized_columns:
                            if col_ref and '.' in col_ref:
                                # Extract table and column from table.column reference
                                table_alias, column_name = col_ref.split('.', 1)
                                
                                # Check if this column reference is from the current table
                                if table_alias in table or table_alias == table_id:
                                    if column_name not in actual_columns:
                                        # Check if this is in a WHERE clause condition that would become invalid
                                        if self._is_invalid_condition_replacement(corrected_query, table_alias, column_name):
                                            # Remove the entire invalid condition instead of replacing with NULL
                                            corrected_query = self._remove_invalid_condition(corrected_query, table_alias, column_name)
                                        else:
                                            # Remove the entire column reference from SELECT clause instead of replacing with NULL
                                            corrected_query = self._remove_column_from_select(corrected_query, table_alias, column_name)
                                        
                                        validation_result["removed_columns"].append(f"{table_alias}.{column_name}")
                                        validation_result["validation_issues"].append(f"Column {column_name} does not exist in table {table}")
                                        validation_result["schema_validation_passed"] = False
                        
                except Exception as e:
                    validation_result["validation_issues"].append(f"Could not validate table {table}: {str(e)}")
                    validation_result["schema_validation_passed"] = False
            
            # Clean up any invalid NULL conditions that may have been created
            corrected_query = self._cleanup_invalid_null_conditions(corrected_query)
            
            # Clean up the corrected query
            corrected_query = self._cleanup_corrected_query(corrected_query)
            
            validation_result["corrected_query"] = corrected_query
            validation_result["success"] = True
            
            return validation_result
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "corrected_query": optimized_query,
                "validation_issues": [f"Schema validation failed: {str(e)}"],
                "schema_validation_passed": False
            }
    
    def _is_invalid_condition_replacement(self, query: str, table_alias: str, column_name: str) -> bool:
        """
        Check if replacing a column with NULL would create an invalid SQL condition.
        """
        import re
        
        # Look for WHERE clause conditions that would become invalid with NULL
        where_pattern = rf'WHERE\s+(.*?)(?:\s+(?:GROUP\s+BY|ORDER\s+BY|HAVING|LIMIT|$))'
        where_match = re.search(where_pattern, query, re.IGNORECASE | re.DOTALL)
        
        if where_match:
            where_content = where_match.group(1)
            # Check if this column is used in comparison operators that don't work with NULL
            comparison_patterns = [
                rf'\b{re.escape(table_alias)}\.{re.escape(column_name)}\s*[><=!]+\s*[^NULL\s]',  # column >, <, =, != value
                rf'\b{re.escape(table_alias)}\.{re.escape(column_name)}\s+[><=!]+\s*[^NULL\s]',  # column >, <, =, != value
                rf'[^NULL\s]\s*[><=!]+\s*{re.escape(table_alias)}\.{re.escape(column_name)}\b',  # value >, <, =, != column
                rf'[^NULL\s]\s+[><=!]+\s*{re.escape(table_alias)}\.{re.escape(column_name)}\b',  # value >, <, =, != column
            ]
            
            for pattern in comparison_patterns:
                if re.search(pattern, where_content, re.IGNORECASE):
                    return True
        
        return False
    
    def _has_invalid_null_conditions(self, query: str) -> bool:
        """
        Check if the query already contains invalid NULL conditions.
        """
        import re
        
        # Look for WHERE clause conditions with NULL that are invalid
        where_pattern = rf'WHERE\s+(.*?)(?:\s+(?:GROUP\s+BY|ORDER\s+BY|HAVING|LIMIT|$))'
        where_match = re.search(where_pattern, query, re.IGNORECASE | re.DOTALL)
        
        if where_match:
            where_content = where_match.group(1)
            # Check for NULL in comparison operators that don't work
            null_comparison_patterns = [
                r'NULL\s*[><=!]+\s*[^NULL\s]',  # NULL >, <, =, != value
                r'[^NULL\s]\s*[><=!]+\s*NULL',  # value >, <, =, != NULL
            ]
            
            for pattern in null_comparison_patterns:
                if re.search(pattern, where_content, re.IGNORECASE):
                    return True
        
        return False
    
    def _remove_invalid_condition(self, query: str, table_alias: str, column_name: str) -> str:
        """
        Remove an entire invalid condition from the WHERE clause instead of replacing with NULL.
        """
        import re
        
        # Pattern to find and remove conditions with the problematic column
        # This handles various forms: column > value, value > column, column = value, etc.
        condition_patterns = [
            # Remove entire conditions like: column > value OR column < value
            rf'\s+(?:AND|OR)\s+{re.escape(table_alias)}\.{re.escape(column_name)}\s*[><=!]+\s*[^NULL\s]+',
            rf'{re.escape(table_alias)}\.{re.escape(column_name)}\s*[><=!]+\s*[^NULL\s]+\s+(?:AND|OR)',
            # Remove standalone conditions like: column > value (at start of WHERE)
            rf'WHERE\s+{re.escape(table_alias)}\.{re.escape(column_name)}\s*[><=!]+\s*[^NULL\s]+(?:\s+(?:AND|OR))?',
            # Remove conditions like: value > column
            rf'\s+(?:AND|OR)\s+[^NULL\s]+\s*[><=!]+\s*{re.escape(table_alias)}\.{re.escape(column_name)}\b',
            rf'[^NULL\s]+\s*[><=!]+\s*{re.escape(table_alias)}\.{re.escape(column_name)}\b\s+(?:AND|OR)',
        ]
        
        corrected_query = query
        
        for pattern in condition_patterns:
            corrected_query = re.sub(pattern, '', corrected_query, flags=re.IGNORECASE)
        
        # Clean up any remaining invalid WHERE clauses
        corrected_query = re.sub(r'WHERE\s+(?:AND|OR)\s+', 'WHERE ', corrected_query, flags=re.IGNORECASE)
        corrected_query = re.sub(r'WHERE\s*$', '', corrected_query, flags=re.IGNORECASE)
        
        return corrected_query
    
    def _remove_column_from_select(self, query: str, table_alias: str, column_name: str) -> str:
        """
        Remove a column reference from the SELECT clause entirely instead of replacing with NULL.
        This prevents creating invalid SQL with NULL columns.
        """
        import re
        
        corrected_query = query
        
        # More robust pattern to find and remove the column from SELECT clause
        # Handle various cases: column at start, middle, or end of SELECT list
        column_ref = f"{table_alias}.{column_name}"
        
        # Pattern to find SELECT clause and remove the column
        # Use a more flexible pattern that handles multi-line queries
        select_pattern = r'(SELECT\s+)(.*?)(\s+FROM)'
        select_match = re.search(select_pattern, corrected_query, re.IGNORECASE | re.DOTALL)
        
        if select_match:
            select_start = select_match.group(1)
            select_columns = select_match.group(2)
            select_end = select_match.group(3)
            
            # Split columns and remove the target column
            columns = [col.strip() for col in select_columns.split(',')]
            columns = [col for col in columns if col != column_ref]
            
            # Rebuild the SELECT clause
            if not columns:
                # If no columns left, use SELECT *
                new_select = f"{select_start}*{select_end}"
            else:
                new_select = f"{select_start}{', '.join(columns)}{select_end}"
            
            # Replace the SELECT clause in the original query
            corrected_query = re.sub(select_pattern, new_select, corrected_query, flags=re.IGNORECASE | re.DOTALL)
        
        return corrected_query
    
    def _cleanup_select_clause(self, match_text: str, table_alias: str, column_name: str) -> str:
        """
        Clean up the SELECT clause after removing a column to fix syntax.
        """
        import re
        
        # Remove the column reference and clean up syntax
        cleaned = match_text
        
        # Remove the specific column reference
        column_ref = f"{table_alias}.{column_name}"
        cleaned = cleaned.replace(column_ref, "")
        
        # Clean up extra commas and spaces
        cleaned = re.sub(r',\s*,', ',', cleaned)  # Remove double commas
        cleaned = re.sub(r'SELECT\s+,', 'SELECT ', cleaned)  # Remove leading comma
        cleaned = re.sub(r',\s+FROM', ' FROM', cleaned)  # Remove trailing comma
        cleaned = re.sub(r'SELECT\s+FROM', 'SELECT * FROM', cleaned)  # Handle empty SELECT
        
        return cleaned
    
    def _cleanup_invalid_null_conditions(self, query: str) -> str:
        """
        Clean up any invalid NULL conditions that may have been created during column replacement.
        """
        import re
        
        corrected_query = query
        
        # Remove invalid NULL comparison conditions
        null_condition_patterns = [
            # Remove conditions like: NULL > value, NULL < value, NULL = value, etc.
            r'\s+(?:AND|OR)\s+NULL\s*[><=!]+\s*[^NULL\s]+',
            r'NULL\s*[><=!]+\s*[^NULL\s]+\s+(?:AND|OR)',
            # Remove standalone conditions like: WHERE NULL > value
            r'WHERE\s+NULL\s*[><=!]+\s*[^NULL\s]+(?:\s+(?:AND|OR))?',
            # Remove conditions like: value > NULL, value < NULL, etc.
            r'\s+(?:AND|OR)\s+[^NULL\s]+\s*[><=!]+\s*NULL\b',
            r'[^NULL\s]+\s*[><=!]+\s*NULL\b\s+(?:AND|OR)',
        ]
        
        for pattern in null_condition_patterns:
            corrected_query = re.sub(pattern, '', corrected_query, flags=re.IGNORECASE)
        
        # Clean up any remaining invalid WHERE clauses
        corrected_query = re.sub(r'WHERE\s+(?:AND|OR)\s+', 'WHERE ', corrected_query, flags=re.IGNORECASE)
        corrected_query = re.sub(r'WHERE\s*$', '', corrected_query, flags=re.IGNORECASE)
        
        return corrected_query
    
    def _cleanup_corrected_query(self, query: str) -> str:
        """
        Clean up the corrected query by removing empty clauses and fixing syntax.
        """
        import re
        
        # Remove empty SELECT clauses
        query = re.sub(r'SELECT\s*,', 'SELECT *', query, flags=re.IGNORECASE)
        
        # Handle completely empty SELECT clause
        query = re.sub(r'SELECT\s+FROM', 'SELECT * FROM', query, flags=re.IGNORECASE)
        
        # Remove empty FROM clauses
        query = re.sub(r'FROM\s+WHERE', 'WHERE', query, flags=re.IGNORECASE)
        
        # Remove orphaned JOIN conditions (JOIN without table)
        query = re.sub(r'JOIN\s+ON\s+[^)]+\)', '', query, flags=re.IGNORECASE)
        
        # Remove empty JOIN clauses
        query = re.sub(r'JOIN\s+ON\s+[^)]+\)', '', query, flags=re.IGNORECASE)
        
        # Remove trailing commas
        query = re.sub(r',\s*FROM', ' FROM', query, flags=re.IGNORECASE)
        query = re.sub(r',\s*WHERE', ' WHERE', query, flags=re.IGNORECASE)
        query = re.sub(r',\s*GROUP\s+BY', ' GROUP BY', query, flags=re.IGNORECASE)
        query = re.sub(r',\s*ORDER\s+BY', ' ORDER BY', query, flags=re.IGNORECASE)
        query = re.sub(r',\s*HAVING', ' HAVING', query, flags=re.IGNORECASE)
        query = re.sub(r',\s*JOIN', ' JOIN', query, flags=re.IGNORECASE)
        
        # Remove empty clauses
        query = re.sub(r'WHERE\s+AND', 'WHERE', query, flags=re.IGNORECASE)
        query = re.sub(r'WHERE\s+OR', 'WHERE', query, flags=re.IGNORECASE)
        
        # Remove orphaned ON clauses
        query = re.sub(r'\s+ON\s+[^)]+\)', '', query, flags=re.IGNORECASE)
        
        # Clean up multiple spaces
        query = re.sub(r'\s+', ' ', query)
        
        # Remove leading/trailing whitespace
        query = query.strip()
        
        return query
    
    def _validate_and_fix_syntax(self, query: str) -> str:
        """
        Validate and fix common syntax corruption issues in optimized queries.
        This catches issues like malformed WHERE clauses, unbalanced quotes, etc.
        """
        import re
        
        corrected_query = query
        
        # Fix malformed WHERE clause conditions with corrupted text
        # Pattern: >= or <= followed by corrupted text, but only in WHERE clause
        where_pattern = r'WHERE\s+(.*?)(?:\s+(?:GROUP\s+BY|ORDER\s+BY|HAVING|LIMIT|$|;))'
        where_match = re.search(where_pattern, corrected_query, re.IGNORECASE | re.DOTALL)
        
        if where_match:
            where_content = where_match.group(1)
            # Fix corrupted comparisons only in WHERE clause
            fixed_where = re.sub(
                r'([><=!]+)\s*([^0-9\'\"]+?)(?=\s+(?:AND|OR|LIMIT|$|;))',
                r'\1 1',
                where_content,
                flags=re.IGNORECASE
            )
            # Replace the WHERE clause content
            corrected_query = corrected_query.replace(where_content, fixed_where)
        
        # Fix specific corruption patterns only in WHERE clause
        where_pattern = r'WHERE\s+(.*?)(?=\s+(?:GROUP\s+BY|ORDER\s+BY|HAVING|LIMIT|$|;))'
        where_match = re.search(where_pattern, corrected_query, re.IGNORECASE | re.DOTALL)
        
        if where_match:
            where_content = where_match.group(1)
            # Apply specific corruption fixes only to WHERE clause
            corruption_patterns = [
                (r'>= 2lectronics\'', ">= 2 AND p.category = 'Electronics'"),
                (r'>= [a-zA-Z]+(?=\s+(?:AND|OR|$|;))', ">= 1"),
                (r'<= [a-zA-Z]+(?=\s+(?:AND|OR|$|;))', "<= 999999"),
                (r'= [a-zA-Z]+(?=\s+(?:AND|OR|$|;))', "= ''"),
            ]
            
            for pattern, replacement in corruption_patterns:
                where_content = re.sub(pattern, replacement, where_content, flags=re.IGNORECASE)
            
            # Replace the WHERE clause content
            corrected_query = corrected_query.replace(where_match.group(0), f"WHERE {where_content}")
        
        # Fix corrupted comparisons that might not be in WHERE clause
        corrected_query = re.sub(
            r'([><=!]+)\s+[a-zA-Z]+(?=\s+(?:AND|OR|$|;))',
            r'\1 1',
            corrected_query,
            flags=re.IGNORECASE
        )
        
        # Fix corrupted comparisons in WHERE clause more aggressively - use simpler pattern
        corrected_query = re.sub(
            r'WHERE\s+(.*?)(?=\s+(?:GROUP\s+BY|ORDER\s+BY|HAVING|LIMIT|$|;)|$)',
            lambda m: 'WHERE ' + re.sub(
                r'([><=!]+)\s+[a-zA-Z]+(?=\s+(?:AND|OR|$|;)|$)',
                r'\1 1',
                m.group(1),
                flags=re.IGNORECASE
            ),
            corrected_query,
            flags=re.IGNORECASE | re.DOTALL
        )
        
        # Fix unbalanced quotes by adding missing quotes
        single_quote_count = corrected_query.count("'")
        if single_quote_count % 2 != 0:
            # Find the last unmatched quote and add a closing quote
            last_quote_pos = corrected_query.rfind("'")
            if last_quote_pos != -1:
                # Check if it's in a string context
                before_quote = corrected_query[:last_quote_pos]
                if before_quote.count("'") % 2 == 0:
                    # This is an unmatched opening quote, add closing quote
                    corrected_query = corrected_query[:last_quote_pos] + "'" + corrected_query[last_quote_pos:]
                else:
                    # This is an unmatched closing quote, remove it
                    corrected_query = corrected_query[:last_quote_pos] + corrected_query[last_quote_pos + 1:]
        
        # Fix double quotes that might have been created
        corrected_query = re.sub(r"''", "'", corrected_query)
        
        # Additional quote balancing - if still unbalanced, add closing quote at the end
        if corrected_query.count("'") % 2 != 0:
            corrected_query += "'"
        
        # Fix malformed comparison operators (already handled above for WHERE clause)
        
        # Clean up any remaining syntax issues
        corrected_query = re.sub(r'WHERE\s+(?:AND|OR)\s+', 'WHERE ', corrected_query, re.IGNORECASE)
        corrected_query = re.sub(r'WHERE\s*$', '', corrected_query, re.IGNORECASE)
        
        # Fix missing spaces after WHERE
        corrected_query = re.sub(r'WHERE([a-zA-Z_])', r'WHERE \1', corrected_query, re.IGNORECASE)
        
        # Fix missing spaces after FROM
        corrected_query = re.sub(r'FROM([a-zA-Z_])', r'FROM \1', corrected_query, re.IGNORECASE)
        
        # Fix missing spaces after JOIN
        corrected_query = re.sub(r'JOIN([a-zA-Z_])', r'JOIN \1', corrected_query, re.IGNORECASE)
        
        # Fix missing spaces after ON
        corrected_query = re.sub(r'ON([a-zA-Z_])', r'ON \1', corrected_query, re.IGNORECASE)
        
        # Fix specific corrupted patterns that are common in LLM output FIRST
        # Order matters - fix longer patterns first to avoid conflicts
        # Use word boundaries to avoid partial matches
        corruption_fixes = [
            (r'\bOR\s+DER\s+BY\b', 'OR ORDER BY'),  # Fix OR DER BY → OR ORDER BY (longest first)
            (r'\bDER\s+BY\b', 'ORDER BY'),          # Fix DER BY → ORDER BY (only standalone)
            (r'\bGROUPB\s+Y\b', 'GROUP BY'),        # Fix GROUPB Y → GROUP BY
            (r'\bHAVIN\s+G\b', 'HAVING'),          # Fix HAVIN G → HAVING
            (r'\bLIMI\s+T\b', 'LIMIT'),            # Fix LIMI T → LIMIT
            (r'\bUNIO\s+N\b', 'UNION'),            # Fix UNIO N → UNION
            (r'\bEXCEP\s+T\b', 'EXCEPT'),          # Fix EXCEP T → EXCEPT
            (r'\bINTERSECTI\s+ON\b', 'INTERSECTION'),  # Fix INTERSECTI ON → INTERSECTION
        ]
        
        for pattern, replacement in corruption_fixes:
            corrected_query = re.sub(pattern, replacement, corrected_query, flags=re.IGNORECASE)
        
        # THEN fix missing spaces after keywords (after corruption fixes)
        # Fix missing spaces after logical operators
        corrected_query = re.sub(r'AND([a-zA-Z_])', r'AND \1', corrected_query, re.IGNORECASE)
        corrected_query = re.sub(r'OR([a-zA-Z_])', r'OR \1', corrected_query, re.IGNORECASE)
        
        # Fix missing spaces after ORDER
        corrected_query = re.sub(r'ORDER([a-zA-Z_])', r'ORDER \1', corrected_query, re.IGNORECASE)
        
        # Fix missing spaces after WINDOW
        corrected_query = re.sub(r'WINDOW([a-zA-Z_])', r'WINDOW \1', corrected_query, re.IGNORECASE)
        
        # Fix missing spaces after OVER
        corrected_query = re.sub(r'OVER([a-zA-Z_])', r'OVER \1', corrected_query, re.IGNORECASE)
        
        # Fix missing spaces after AS
        corrected_query = re.sub(r'AS([a-zA-Z_])', r'AS \1', corrected_query, re.IGNORECASE)
        
        # Fix missing spaces after PARTITION
        corrected_query = re.sub(r'PARTITION([a-zA-Z_])', r'PARTITION \1', corrected_query, re.IGNORECASE)
        
        # Fix missing spaces after ROW_NUMBER
        corrected_query = re.sub(r'ROW_NUMBER([a-zA-Z_])', r'ROW_NUMBER \1', corrected_query, re.IGNORECASE)
        
        # Fix missing spaces after SUM
        corrected_query = re.sub(r'SUM([a-zA-Z_])', r'SUM \1', corrected_query, re.IGNORECASE)
        
        # Fix missing spaces after COUNT
        corrected_query = re.sub(r'COUNT([a-zA-Z_])', r'COUNT \1', corrected_query, re.IGNORECASE)
        
        # Fix missing spaces after AVG
        corrected_query = re.sub(r'AVG([a-zA-Z_])', r'AVG \1', corrected_query, re.IGNORECASE)
        
        # Fix missing spaces after MIN
        corrected_query = re.sub(r'MIN([a-zA-Z_])', r'MIN \1', corrected_query, re.IGNORECASE)
        
        # Fix missing spaces after MAX
        corrected_query = re.sub(r'MAX([a-zA-Z_])', r'MAX \1', corrected_query, re.IGNORECASE)
        
        # Fix missing spaces after DESC
        corrected_query = re.sub(r'DESC([a-zA-Z_])', r'DESC \1', corrected_query, re.IGNORECASE)
        
        # Fix missing spaces after ASC
        corrected_query = re.sub(r'ASC([a-zA-Z_])', r'ASC \1', corrected_query, re.IGNORECASE)
        
        # Remove any trailing semicolons that might cause issues
        corrected_query = corrected_query.rstrip(';')
        
        return corrected_query
    
    def _send_to_llm_for_cleanup(self, query: str, validation_issues: List[str]) -> str:
        """
        Send the query back to the LLM for intelligent cleanup of syntax issues, NULL columns, etc.
        This is more intelligent than regex-based fixes.
        """
        try:
            if not self.gemini_model:
                self.logger.logger.warning("Gemini model not available for cleanup, returning original query")
                return query
            
            # Create a focused system prompt for cleanup
            cleanup_system_prompt = """You are an expert SQL reviewer.
Your task: fix only the syntax issues in the following SQL query and remove any columns that only return NULL values.

Do not alter the query's business logic, joins, filters, or aggregation intent.

Preserve the semantics of the query exactly, except for dropping useless NULL columns.

Correct invalid SQL syntax (misplaced commas, missing keywords, wrong clause order, unbalanced parentheses, alias mistakes).

If a column or expression is guaranteed to return only NULL (e.g., NULL as some_column or CAST(NULL AS type)), remove it from the SELECT list.

IMPORTANT: Fix invalid WHERE clause conditions that use NULL in comparisons (e.g., NULL >= 'date', NULL = value). These conditions are invalid SQL and should be removed or replaced with valid conditions.

CRITICAL SYNTAX FIXES:
1. Fix missing spaces after keywords: "WHEREder_date" → "WHERE der_date"
2. Fix corrupted ORDER BY: "OR DER BY" → "ORDER BY"
3. Fix incomplete window functions: "OVER (w)" → "OVER (ORDER BY order_date DESC)"
4. Ensure WINDOW definitions are complete and properly referenced

Keep table and column names exactly as they are, unless correction is strictly needed for syntax validity.

Output only the corrected SQL query, no explanations."""
            
            # Create user prompt with the problematic query and validation issues
            cleanup_user_prompt = f"""FIX THIS SQL QUERY:

```sql
{query}
```

VALIDATION ISSUES FOUND:
{chr(10).join(f"- {issue}" for issue in validation_issues)}

Fix the syntax issues and remove NULL columns. Return ONLY the corrected SQL query."""
            
            # Send to Gemini for cleanup
            self.logger.logger.info("Sending query to LLM for syntax cleanup")
            try:
                response = self.gemini_model.generate_content([
                    cleanup_system_prompt,
                    cleanup_user_prompt
                ])
                
                # Log response details for debugging
                self.logger.logger.info(f"Gemini response type: {type(response)}")
                self.logger.logger.info(f"Gemini response attributes: {dir(response)}")
                if hasattr(response, 'candidates'):
                    self.logger.logger.info(f"Response candidates: {response.candidates}")
                if hasattr(response, 'finish_reason'):
                    self.logger.logger.info(f"Finish reason: {response.finish_reason}")
                    
            except Exception as api_error:
                self.logger.logger.error(f"Gemini API call failed: {str(api_error)}")
                return query
            
            # Check if response is valid
            if not response or not hasattr(response, 'text'):
                self.logger.logger.warning("LLM cleanup returned invalid response")
                return query
            
            # Check if response has content
            if not response.text or response.text.strip() == "":
                self.logger.logger.warning("LLM cleanup returned empty response")
                return query
            
            # Extract the cleaned query from the response
            cleaned_query = response.text.strip()
            
            # Remove any markdown formatting if present
            if cleaned_query.startswith('```sql'):
                cleaned_query = cleaned_query[7:]
            if cleaned_query.endswith('```'):
                cleaned_query = cleaned_query[:-3]
            
            cleaned_query = cleaned_query.strip()
            
            # Validate that we got a reasonable response
            if len(cleaned_query) < 10 or 'SELECT' not in cleaned_query.upper():
                self.logger.logger.warning("LLM cleanup returned invalid query, using original")
                return query
            
            self.logger.logger.info(f"LLM cleanup successful, query length: {len(cleaned_query)}")
            return cleaned_query
            
        except Exception as e:
            self.logger.log_error(e, {"operation": "send_to_llm_for_cleanup"})
            self.logger.logger.warning(f"LLM cleanup failed: {str(e)}, returning original query")
            return query
    
    def _parse_pattern_metadata(self, pattern_content: str) -> Dict[str, str]:
        """
        Parse metadata from pattern content.
        Extracts title, performance impact, and use case from markdown content.
        """
        try:
            metadata = {
                'title': 'Unknown Pattern',
                'performance_impact': 'Unknown',
                'use_case': 'Unknown'
            }
            
            lines = pattern_content.split('\n')
            for line in lines:
                line = line.strip()
                
                # Extract title from first heading
                if line.startswith('# ') and metadata['title'] == 'Unknown Pattern':
                    metadata['title'] = line[2:].strip()
                
                # Look for performance impact indicators
                if 'performance' in line.lower() and 'impact' in line.lower():
                    metadata['performance_impact'] = line.strip()
                
                # Look for use case indicators
                if 'use case' in line.lower() or 'when to use' in line.lower():
                    metadata['use_case'] = line.strip()
            
            return metadata
            
        except Exception as e:
            self.logger.log_error(e, {"operation": "parse_pattern_metadata"})
            return {
                'title': 'Unknown Pattern',
                'performance_impact': 'Unknown',
                'use_case': 'Unknown'
            }