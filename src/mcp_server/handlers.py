"""
Direct SQL optimization handler that reads markdown files and sends to LLM.
Simplified architecture that processes raw SQL queries directly.
"""

import re
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from src.common.logger import QueryOptimizerLogger


class DirectSQLOptimizationHandler:
    """Handles direct SQL optimization requests using markdown documentation."""
    
    def __init__(self, docs_directory: str = "data/optimization_docs_md"):
        self.logger = QueryOptimizerLogger(__name__)
        self.docs_directory = Path(docs_directory)
        self.optimization_patterns = self._load_all_pattern_files()
    
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
    
    def process_raw_sql_query(self, sql_query: str, project_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Process raw SQL query directly and return optimization context for LLM.
        
        This is the main entry point for the simplified architecture.
        """
        try:
            start_time = time.time()
            
            # Step 1: Get all markdown files content
            all_docs_content = self._prepare_all_docs_content()
            
            # Step 2: Create system prompt for LLM
            system_prompt = self._create_system_prompt()
            
            # Step 3: Create user prompt with query and all docs
            user_prompt = self._create_user_prompt(sql_query, all_docs_content, project_id)
            
            processing_time = int((time.time() - start_time) * 1000)
            
            return {
                "success": True,
                "system_prompt": system_prompt,
                "user_prompt": user_prompt,
                "docs_content": all_docs_content,
                "processing_time_ms": processing_time
            }
            
        except Exception as e:
            self.logger.log_error(e, {"operation": "process_raw_sql_query"})
            return {
                "success": False,
                "error": str(e),
                "processing_time_ms": int((time.time() - start_time) * 1000)
            }
    
    def _prepare_all_docs_content(self) -> str:
        """Prepare ALL documentation content for LLM."""
        all_content = "BIGQUERY OPTIMIZATION DOCUMENTATION:\n\n"
        
        for file_name, content in self.optimization_patterns.items():
            all_content += f"## FILE: {file_name}.md\n"
            all_content += f"LOCATION: data/optimization_docs_md/{file_name}.md\n\n"
            all_content += content
            all_content += "\n\n" + "="*80 + "\n\n"
        
        return all_content
    
    def _create_system_prompt(self) -> str:
        """Create system prompt for LLM optimization."""
        return """You are an expert BigQuery SQL optimizer. Your task is to optimize SQL queries for better performance while preserving exact business logic.

CRITICAL REQUIREMENTS:
1. The optimized query MUST return identical results to the original query
2. Apply Google's official BigQuery best practices from the provided documentation
3. Target 30-50% performance improvement minimum
4. Use only existing table columns (no made-up column names)
5. Preserve all business logic exactly

OPTIMIZATION PRIORITIES (from documentation):
1. Replace SELECT * with specific columns (30-50% improvement)
2. Convert COUNT(DISTINCT) to APPROX_COUNT_DISTINCT (50-80% improvement)
3. Convert subqueries to JOINs (40-70% improvement)
4. Reorder JOINs to place smaller tables first (25-50% improvement)
5. Add proper PARTITION BY to window functions (25-40% improvement)
6. Remove unnecessary CAST/string operations (20-35% improvement)
7. Apply predicate pushdown for early filtering (25-45% improvement)
8. Convert HAVING to WHERE when possible (15-25% improvement)

RESPONSE FORMAT:
Return a JSON object with:
{
    "optimized_query": "The optimized SQL query",
    "optimizations_applied": [
        {
            "pattern_id": "column_pruning",
            "pattern_name": "Column Pruning",
            "description": "What was changed and why",
            "expected_improvement": 0.3,
            "documentation_reference": "Reference to specific documentation section"
        }
    ],
    "estimated_improvement": 0.4,
    "explanation": "Summary of all optimizations applied"
}"""
    
    def _create_user_prompt(self, sql_query: str, all_docs_content: str, project_id: Optional[str]) -> str:
        """Create user prompt with query and ALL documentation."""
        prompt = f"""OPTIMIZE THIS BIGQUERY SQL QUERY:

```sql
{sql_query}
```

PROJECT CONTEXT:
- Project ID: {project_id or 'not-specified'}
- Target: 30-50% performance improvement minimum
- Requirement: Preserve exact business logic

COMPLETE BIGQUERY OPTIMIZATION DOCUMENTATION:

{all_docs_content}

INSTRUCTIONS:
1. Analyze the SQL query for inefficiencies using the documentation above
2. Apply the optimization patterns from the documentation that are relevant
3. Ensure the optimized query returns identical results to the original
4. Focus on high-impact optimizations first (50%+ improvement patterns)
5. Provide clear explanations for each optimization with documentation references
6. Use the exact documentation file locations and pattern names in your response

Generate the optimized query following the JSON format specified in the system prompt."""
        
        return prompt