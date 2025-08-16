"""
MCP Server handlers for direct SQL query optimization using markdown documentation.
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
            
            # Step 1: Analyze the raw SQL query
            query_analysis = self._analyze_raw_sql(sql_query)
            
            # Step 2: Find applicable optimization patterns
            applicable_patterns = self._find_applicable_patterns(sql_query)
            
            # Step 3: Prepare all documentation content for LLM
            all_docs_content = self._prepare_all_docs_content()
            
            # Step 4: Create system prompt for LLM
            system_prompt = self._create_system_prompt()
            
            # Step 5: Create user prompt with query and all docs
            user_prompt = self._create_user_prompt(sql_query, all_docs_content, project_id)
            
            processing_time = int((time.time() - start_time) * 1000)
            
            return {
                "success": True,
                "query_analysis": query_analysis,
                "applicable_patterns": [p["pattern_id"] for p in applicable_patterns],
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
    
    def _analyze_raw_sql(self, sql_query: str) -> Dict[str, Any]:
        """Analyze raw SQL query structure."""
        query_upper = sql_query.upper()
        
        return {
            "has_select_star": "SELECT *" in query_upper,
            "has_joins": "JOIN" in query_upper,
            "join_count": len(re.findall(r'\bJOIN\b', query_upper)),
            "has_subqueries": "EXISTS" in query_upper or "IN (SELECT" in query_upper,
            "has_count_distinct": "COUNT(DISTINCT" in query_upper,
            "has_window_functions": "OVER (" in query_upper,
            "has_group_by": "GROUP BY" in query_upper,
            "has_order_by": "ORDER BY" in query_upper,
            "has_having": "HAVING" in query_upper,
            "table_count": len(self._extract_table_names(sql_query)),
            "query_length": len(sql_query),
            "complexity": self._assess_complexity(sql_query)
        }
    
    def _find_applicable_patterns(self, sql_query: str) -> List[Dict[str, Any]]:
        """Find applicable optimization patterns for the SQL query."""
        applicable = []
        query_upper = sql_query.upper()
        
        # Check each pattern for applicability
        for pattern_name, pattern_content in self.optimization_patterns.items():
            pattern_info = self._parse_pattern_metadata(pattern_content)
            
            if self._is_pattern_applicable(sql_query, pattern_info):
                applicable.append({
                    "pattern_id": pattern_name,
                    "pattern_name": pattern_info.get("title", pattern_name),
                    "content": pattern_content,
                    "priority": self._calculate_priority(sql_query, pattern_info)
                })
        
        # Sort by priority
        applicable.sort(key=lambda x: x["priority"], reverse=True)
        return applicable
    
    def _prepare_all_docs_content(self) -> str:
        """Prepare ALL documentation content for LLM."""
        all_content = "BIGQUERY OPTIMIZATION DOCUMENTATION:\n\n"
        
        for file_name, content in self.optimization_patterns.items():
            all_content += f"## FILE: {file_name}.md\n"
            all_content += f"LOCATION: data/optimization_docs_md/{file_name}.md\n\n"
            all_content += content
            all_content += "\n\n" + "="*80 + "\n\n"
        
        return all_content
    
    def _parse_pattern_metadata(self, pattern_content: str) -> Dict[str, Any]:
        """Parse metadata from pattern markdown content."""
        metadata = {}
        lines = pattern_content.split('\n')
        
        for line in lines:
            if line.startswith('# '):
                metadata['title'] = line[2:].strip()
            elif line.startswith('**Pattern ID**:'):
                metadata['pattern_id'] = line.split(':', 1)[1].strip().strip('`')
            elif line.startswith('**Performance Impact**:'):
                metadata['performance_impact'] = line.split(':', 1)[1].strip()
            elif line.startswith('**Use Case**:'):
                metadata['use_case'] = line.split(':', 1)[1].strip()
        
        return metadata
    
    def _is_pattern_applicable(self, sql_query: str, pattern_info: Dict[str, Any]) -> bool:
        """Check if a pattern is applicable to the SQL query."""
        query_upper = sql_query.upper()
        pattern_id = pattern_info.get('pattern_id', '')
        
        if pattern_id == 'column_pruning':
            return 'SELECT *' in query_upper
        elif pattern_id == 'join_reordering':
            return 'JOIN' in query_upper
        elif pattern_id == 'approximate_aggregation':
            return 'COUNT(DISTINCT' in query_upper
        elif pattern_id == 'subquery_to_join':
            return 'EXISTS (' in query_upper or 'IN (SELECT' in query_upper
        elif pattern_id == 'window_optimization':
            return 'OVER (' in query_upper
        elif pattern_id == 'predicate_pushdown':
            return 'WHERE' in query_upper and ('JOIN' in query_upper or query_upper.count('SELECT') > 1)
        elif pattern_id == 'having_to_where_conversion':
            return 'HAVING' in query_upper
        elif pattern_id == 'unnecessary_operations':
            return any(op in query_upper for op in ['CAST(', 'SUBSTR(', 'LOWER(', 'UPPER('])
        
        return False
    
    def _calculate_priority(self, sql_query: str, pattern_info: Dict[str, Any]) -> int:
        """Calculate priority score for a pattern."""
        score = 0
        
        # Base score from performance impact
        performance_impact = pattern_info.get('performance_impact', '')
        if '50-80%' in performance_impact or '60-90%' in performance_impact:
            score += 50
        elif '30-60%' in performance_impact or '40-70%' in performance_impact:
            score += 40
        elif '20-40%' in performance_impact or '25-50%' in performance_impact:
            score += 30
        elif '15-30%' in performance_impact:
            score += 20
        
        # Boost for common issues
        query_upper = sql_query.upper()
        pattern_id = pattern_info.get('pattern_id', '')
        
        if pattern_id == 'column_pruning' and 'SELECT *' in query_upper:
            score += 25
        elif pattern_id == 'approximate_aggregation' and 'COUNT(DISTINCT' in query_upper:
            score += 30
        elif pattern_id == 'subquery_to_join' and ('EXISTS' in query_upper or 'IN (SELECT' in query_upper):
            score += 35
        
        return score
    
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
    
    def _extract_table_names(self, query: str) -> List[str]:
        """Extract table names from SQL query."""
        patterns = [
            r'FROM\s+`([^`]+)`',
            r'JOIN\s+`([^`]+)`',
            r'FROM\s+([a-zA-Z_][a-zA-Z0-9_\.]*?)(?:\s+[a-zA-Z_]|\s*$|\s*WHERE|\s*GROUP|\s*ORDER|\s*LIMIT)',
            r'JOIN\s+([a-zA-Z_][a-zA-Z0-9_\.]*?)(?:\s+[a-zA-Z_]|\s+ON|\s*$)',
        ]
        
        tables = set()
        for pattern in patterns:
            matches = re.findall(pattern, query, re.IGNORECASE)
            for match in matches:
                table_name = match.strip()
                if table_name and table_name.upper() not in ['ON', 'WHERE', 'GROUP', 'ORDER', 'LIMIT', 'AS']:
                    tables.add(table_name)
        
        return list(tables)
    
    def _assess_complexity(self, sql_query: str) -> str:
        """Assess query complexity."""
        query_upper = sql_query.upper()
        
        complexity_score = 0
        complexity_score += len(re.findall(r'\bJOIN\b', query_upper)) * 2
        complexity_score += len(re.findall(r'\bSELECT\b', query_upper)) * 1
        complexity_score += len(re.findall(r'\bGROUP BY\b', query_upper)) * 2
        complexity_score += len(re.findall(r'\bOVER\s*\(', query_upper)) * 2
        
        if complexity_score <= 3:
            return "simple"
        elif complexity_score <= 8:
            return "moderate"
        elif complexity_score <= 15:
            return "complex"
        else:
            return "very_complex"