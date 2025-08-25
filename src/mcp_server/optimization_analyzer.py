"""
Optimization analyzer that reads markdown pattern files and provides suggestions for LLM.
Simplified architecture that processes raw SQL queries directly.
"""

import re
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from src.common.logger import QueryOptimizerLogger


class OptimizationAnalyzer:
    """Analyzes SQL queries and provides optimization suggestions from markdown files."""
    
    def __init__(self, docs_file_path: str = "data/bigquery_optimizations.md"):
        self.logger = QueryOptimizerLogger(__name__)
        self.docs_file_path = Path(docs_file_path)
        self.optimization_patterns = self._load_optimization_patterns()
        
        print(f"✅ OptimizationAnalyzer initialized with {len(self.optimization_patterns)} patterns")
    
    def _load_optimization_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Load optimization patterns from markdown file."""
        patterns = {}
        
        try:
            if not self.docs_file_path.exists():
                self.logger.logger.warning(f"Documentation file not found: {self.docs_file_path}")
                return patterns
            
            content = self.docs_file_path.read_text(encoding='utf-8')
            
            # Split by pattern sections (## headers)
            sections = re.split(r'\n## ', content)
            
            for section in sections:
                pattern_data = self._parse_pattern_section(section)
                if pattern_data:
                    patterns[pattern_data['pattern_id']] = pattern_data
            
            self.logger.logger.info(f"Loaded {len(patterns)} optimization patterns")
            return patterns
            
        except Exception as e:
            self.logger.log_error(e, {"operation": "load_optimization_patterns"})
            return patterns
    
    def _parse_pattern_section(self, section: str) -> Optional[Dict[str, Any]]:
        """Parse a single pattern section from markdown."""
        lines = section.strip().split('\n')
        if not lines:
            return None
        
        pattern_data = {}
        
        # Extract title (first line)
        title = lines[0].strip()
        if title.startswith('# '):
            title = title[2:]
        pattern_data['title'] = title
        
        # Extract metadata
        for line in lines:
            if line.startswith('**Pattern ID**:'):
                pattern_id = line.split(':', 1)[1].strip().strip('`')
                pattern_data['pattern_id'] = pattern_id
            elif line.startswith('**Performance Impact**:'):
                pattern_data['performance_impact'] = line.split(':', 1)[1].strip()
            elif line.startswith('**Use Case**:'):
                pattern_data['use_case'] = line.split(':', 1)[1].strip()
            elif line.startswith('**Expected Improvement**'):
                pattern_data['expected_improvement'] = line.split(':', 1)[1].strip()
            elif line.startswith('**Documentation Reference**'):
                pattern_data['documentation_reference'] = line.split(':', 1)[1].strip()
        
        # Extract description and examples
        pattern_data['description'] = self._extract_description(section)
        pattern_data['example_before'] = self._extract_code_block(section, 'Before')
        pattern_data['example_after'] = self._extract_code_block(section, 'After')
        
        return pattern_data if pattern_data.get('pattern_id') else None
    
    def _extract_description(self, section: str) -> str:
        """Extract description from pattern section."""
        lines = section.split('\n')
        description_lines = []
        in_description = False
        
        for line in lines:
            if line.startswith('## Description') or line.startswith('### Description'):
                in_description = True
                continue
            elif line.startswith('##') or line.startswith('###'):
                in_description = False
            elif in_description and line.strip():
                description_lines.append(line.strip())
        
        return ' '.join(description_lines)
    
    def _extract_code_block(self, section: str, block_type: str) -> str:
        """Extract code block (Before/After) from pattern section."""
        lines = section.split('\n')
        in_code_block = False
        code_lines = []
        
        for line in lines:
            if f'-- {block_type}' in line:
                in_code_block = True
                continue
            elif line.startswith('-- ') and block_type not in line:
                in_code_block = False
            elif in_code_block and line.strip() and not line.startswith('```'):
                code_lines.append(line)
        
        return '\n'.join(code_lines)
    
    def get_optimization_suggestions_for_llm(self, sql_query: str) -> str:
        """Get optimization suggestions formatted for LLM consumption."""
        try:
            # Analyze SQL query
            analysis = self.analyze_sql_query(sql_query)
            
            if not analysis['applicable_patterns']:
                return "No specific optimization patterns found for this query."
            
            # Format suggestions for LLM consumption
            suggestions_text = "OPTIMIZATION SUGGESTIONS FROM BIGQUERY DOCUMENTATION:\n\n"
            
            for pattern in analysis['applicable_patterns'][:5]:  # Top 5 patterns
                suggestions_text += f"## {pattern['title']}\n"
                suggestions_text += f"**Performance Impact**: {pattern['performance_impact']}\n"
                suggestions_text += f"**Description**: {pattern['description']}\n"
                
                if pattern['example_before'] and pattern['example_after']:
                    suggestions_text += f"\n**Example Optimization**:\n"
                    suggestions_text += f"```sql\n-- Before (Inefficient)\n{pattern['example_before']}\n\n"
                    suggestions_text += f"-- After (Optimized)\n{pattern['example_after']}\n```\n"
                
                suggestions_text += f"**Expected Improvement**: {pattern['expected_improvement']}\n"
                suggestions_text += f"**Documentation**: {pattern['documentation_reference']}\n\n"
            
            return suggestions_text
            
        except Exception as e:
            self.logger.log_error(e, {"operation": "get_optimization_suggestions_for_llm"})
            return "Error retrieving optimization suggestions."
    
    def analyze_sql_query(self, sql_query: str) -> Dict[str, Any]:
        """Analyze SQL query and find applicable patterns."""
        try:
            query_upper = sql_query.upper()
            
            # Find applicable patterns
            applicable_patterns = []
            
            for pattern_id, pattern_data in self.optimization_patterns.items():
                if self._is_pattern_applicable(sql_query, pattern_data):
                    priority = self._calculate_priority(sql_query, pattern_data)
                    pattern_data['priority'] = priority
                    applicable_patterns.append(pattern_data)
            
            # Sort by priority
            applicable_patterns.sort(key=lambda x: x.get('priority', 0), reverse=True)
            
            return {
                'applicable_patterns': applicable_patterns,
                'total_patterns': len(applicable_patterns),
                'query_characteristics': {
                    'has_select_star': 'SELECT *' in query_upper,
                    'has_joins': 'JOIN' in query_upper,
                    'has_subqueries': 'EXISTS' in query_upper or 'IN (SELECT' in query_upper,
                    'has_count_distinct': 'COUNT(DISTINCT' in query_upper,
                    'has_window_functions': 'OVER (' in query_upper
                }
            }
            
        except Exception as e:
            self.logger.log_error(e, {"operation": "analyze_sql_query"})
            return {'applicable_patterns': [], 'total_patterns': 0}
    
    def _is_pattern_applicable(self, sql_query: str, pattern_data: Dict[str, Any]) -> bool:
        """Check if a pattern is applicable to the SQL query."""
        query_upper = sql_query.upper()
        pattern_id = pattern_data.get('pattern_id', '')
        
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
    
    def _calculate_priority(self, sql_query: str, pattern_data: Dict[str, Any]) -> int:
        """Calculate priority score for a pattern."""
        score = 0
        
        # Base score from performance impact
        performance_impact = pattern_data.get('performance_impact', '')
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
        pattern_id = pattern_data.get('pattern_id', '')
        
        if pattern_id == 'column_pruning' and 'SELECT *' in query_upper:
            score += 25
        elif pattern_id == 'approximate_aggregation' and 'COUNT(DISTINCT' in query_upper:
            score += 30
        elif pattern_id == 'subquery_to_join' and ('EXISTS' in query_upper or 'IN (SELECT' in query_upper):
            score += 35
        
        return score