"""
MCP Server optimization analyzer that reads markdown documentation and provides
SQL query optimization suggestions directly.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from src.common.logger import QueryOptimizerLogger


class OptimizationAnalyzer:
    """Analyzes SQL queries and provides optimization suggestions from markdown documentation."""
    
    def __init__(self, docs_file_path: str = "data/bigquery_optimizations.md"):
        self.logger = QueryOptimizerLogger(__name__)
        self.docs_file_path = Path(docs_file_path)
        self.optimization_patterns = self._load_optimization_patterns()
    
    def _load_optimization_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Load optimization patterns from markdown file."""
        patterns = {}
        
        try:
            if not self.docs_file_path.exists():
                self.logger.logger.warning(f"Documentation file not found: {self.docs_file_path}")
                return patterns
            
            content = self.docs_file_path.read_text(encoding='utf-8')
            
            # Split content by pattern sections (marked by ## headers)
            sections = re.split(r'\n## ', content)
            
            for section in sections:
                if not section.strip():
                    continue
                
                pattern_data = self._parse_pattern_section(section)
                if pattern_data:
                    patterns[pattern_data['pattern_id']] = pattern_data
            
            self.logger.logger.info(f"Loaded {len(patterns)} optimization patterns from markdown")
            return patterns
            
        except Exception as e:
            self.logger.log_error(e, {"operation": "load_optimization_patterns"})
            return patterns
    
    def _parse_pattern_section(self, section: str) -> Optional[Dict[str, Any]]:
        """Parse a single optimization pattern section from markdown."""
        try:
            lines = section.strip().split('\n')
            if not lines:
                return None
            
            # Extract title (first line)
            title = lines[0].strip()
            
            pattern_data = {
                'title': title,
                'pattern_id': '',
                'performance_impact': '',
                'use_case': '',
                'description': '',
                'when_to_apply': [],
                'example_before': '',
                'example_after': '',
                'expected_improvement': '',
                'documentation_reference': '',
                'full_content': section
            }
            
            current_section = None
            current_content = []
            
            for line in lines[1:]:
                line = line.strip()
                
                if line.startswith('**Pattern ID**:'):
                    pattern_data['pattern_id'] = line.split(':', 1)[1].strip().strip('`')
                elif line.startswith('**Performance Impact**:'):
                    pattern_data['performance_impact'] = line.split(':', 1)[1].strip()
                elif line.startswith('**Use Case**:'):
                    pattern_data['use_case'] = line.split(':', 1)[1].strip()
                elif line.startswith('### Description'):
                    current_section = 'description'
                    current_content = []
                elif line.startswith('### When to Apply'):
                    current_section = 'when_to_apply'
                    current_content = []
                elif line.startswith('### Example'):
                    current_section = 'example'
                    current_content = []
                elif line.startswith('### Expected Improvement'):
                    current_section = 'expected_improvement'
                    current_content = []
                elif line.startswith('### Documentation Reference'):
                    current_section = 'documentation_reference'
                    current_content = []
                elif line.startswith('---'):
                    # End of section
                    break
                elif current_section:
                    current_content.append(line)
                
                # Process accumulated content
                if current_section and (line.startswith('###') or line.startswith('---')):
                    content_text = '\n'.join(current_content).strip()
                    
                    if current_section == 'description':
                        pattern_data['description'] = content_text
                    elif current_section == 'when_to_apply':
                        # Extract bullet points
                        pattern_data['when_to_apply'] = [
                            item.strip('- ').strip() 
                            for item in content_text.split('\n') 
                            if item.strip().startswith('-')
                        ]
                    elif current_section == 'example':
                        # Extract before/after examples
                        if '-- Before' in content_text and '-- After' in content_text:
                            parts = content_text.split('-- After')
                            if len(parts) == 2:
                                pattern_data['example_before'] = parts[0].replace('-- Before', '').strip()
                                pattern_data['example_after'] = parts[1].strip()
                    elif current_section == 'expected_improvement':
                        pattern_data['expected_improvement'] = content_text
                    elif current_section == 'documentation_reference':
                        pattern_data['documentation_reference'] = content_text.strip()
            
            return pattern_data if pattern_data['pattern_id'] else None
            
        except Exception as e:
            self.logger.log_error(e, {"operation": "parse_pattern_section"})
            return None
    
    def analyze_sql_query(self, sql_query: str) -> Dict[str, Any]:
        """Analyze SQL query and return applicable optimization patterns."""
        try:
            applicable_patterns = []
            query_upper = sql_query.upper()
            
            # Check each pattern for applicability
            for pattern_id, pattern_data in self.optimization_patterns.items():
                if self._is_pattern_applicable(sql_query, pattern_data):
                    applicable_patterns.append({
                        'pattern_id': pattern_id,
                        'title': pattern_data['title'],
                        'description': pattern_data['description'],
                        'performance_impact': pattern_data['performance_impact'],
                        'use_case': pattern_data['use_case'],
                        'example_before': pattern_data['example_before'],
                        'example_after': pattern_data['example_after'],
                        'expected_improvement': pattern_data['expected_improvement'],
                        'documentation_reference': pattern_data['documentation_reference'],
                        'priority_score': self._calculate_priority_score(sql_query, pattern_data)
                    })
            
            # Sort by priority score
            applicable_patterns.sort(key=lambda x: x['priority_score'], reverse=True)
            
            return {
                'sql_query': sql_query,
                'applicable_patterns': applicable_patterns,
                'total_patterns': len(applicable_patterns),
                'analysis_summary': self._generate_analysis_summary(sql_query, applicable_patterns)
            }
            
        except Exception as e:
            self.logger.log_error(e, {"operation": "analyze_sql_query"})
            return {
                'sql_query': sql_query,
                'applicable_patterns': [],
                'total_patterns': 0,
                'error': str(e)
            }
    
    def _is_pattern_applicable(self, sql_query: str, pattern_data: Dict[str, Any]) -> bool:
        """Check if an optimization pattern is applicable to the SQL query."""
        query_upper = sql_query.upper()
        pattern_id = pattern_data['pattern_id']
        
        # Pattern-specific applicability rules
        if pattern_id == 'column_pruning':
            return 'SELECT *' in query_upper
        
        elif pattern_id == 'join_reordering':
            return 'JOIN' in query_upper
        
        elif pattern_id == 'subquery_to_join':
            return ('EXISTS (' in query_upper or 
                    'IN (SELECT' in query_upper or 
                    'NOT EXISTS' in query_upper)
        
        elif pattern_id == 'approximate_aggregation':
            return 'COUNT(DISTINCT' in query_upper or 'COUNT( DISTINCT' in query_upper
        
        elif pattern_id == 'window_optimization':
            return 'OVER (' in query_upper or 'OVER(' in query_upper
        
        elif pattern_id == 'predicate_pushdown':
            return ('WHERE' in query_upper and 
                    ('JOIN' in query_upper or 'SELECT' in query_upper.count('SELECT') > 1))
        
        elif pattern_id == 'clustering_optimization':
            return 'WHERE' in query_upper and ('=' in query_upper or 'IN (' in query_upper)
        
        elif pattern_id == 'materialized_view_suggestion':
            return 'GROUP BY' in query_upper and ('COUNT(' in query_upper or 'SUM(' in query_upper)
        
        elif pattern_id == 'case_when_optimization':
            return 'CASE WHEN' in query_upper or 'CASE' in query_upper
        
        elif pattern_id == 'having_to_where_conversion':
            return 'HAVING' in query_upper
        
        return False
    
    def _calculate_priority_score(self, sql_query: str, pattern_data: Dict[str, Any]) -> int:
        """Calculate priority score for an optimization pattern."""
        score = 0
        
        # Base score from performance impact
        performance_impact = pattern_data.get('performance_impact', '')
        if '40-70%' in performance_impact or '60-90%' in performance_impact:
            score += 50  # High impact
        elif '30-60%' in performance_impact or '25-45%' in performance_impact:
            score += 30  # Medium-high impact
        elif '20-40%' in performance_impact or '20-35%' in performance_impact:
            score += 20  # Medium impact
        elif '15-30%' in performance_impact or '15-25%' in performance_impact:
            score += 10  # Lower impact
        
        # Boost score for common performance issues
        query_upper = sql_query.upper()
        
        if pattern_data['pattern_id'] == 'column_pruning' and 'SELECT *' in query_upper:
            score += 20  # Very common issue
        
        if pattern_data['pattern_id'] == 'approximate_aggregation' and 'COUNT(DISTINCT' in query_upper:
            score += 25  # High impact on large datasets
        
        if pattern_data['pattern_id'] == 'subquery_to_join' and ('EXISTS' in query_upper or 'IN (SELECT' in query_upper):
            score += 30  # Often significant improvement
        
        return score
    
    def _generate_analysis_summary(self, sql_query: str, applicable_patterns: List[Dict]) -> str:
        """Generate a summary of the query analysis."""
        if not applicable_patterns:
            return "No optimization patterns found for this query. The query may already be well-optimized."
        
        high_priority = [p for p in applicable_patterns if p['priority_score'] >= 40]
        medium_priority = [p for p in applicable_patterns if 20 <= p['priority_score'] < 40]
        low_priority = [p for p in applicable_patterns if p['priority_score'] < 20]
        
        summary_parts = []
        
        if high_priority:
            summary_parts.append(f"High priority optimizations ({len(high_priority)}): {', '.join(p['title'] for p in high_priority)}")
        
        if medium_priority:
            summary_parts.append(f"Medium priority optimizations ({len(medium_priority)}): {', '.join(p['title'] for p in medium_priority)}")
        
        if low_priority:
            summary_parts.append(f"Low priority optimizations ({len(low_priority)}): {', '.join(p['title'] for p in low_priority)}")
        
        return '. '.join(summary_parts)
    
    def get_optimization_suggestions_for_llm(self, sql_query: str) -> str:
        """Get optimization suggestions formatted for LLM consumption."""
        analysis = self.analyze_sql_query(sql_query)
        
        if not analysis['applicable_patterns']:
            return "No specific optimization patterns found for this query."
        
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
            suggestions_text += "---\n\n"
        
        return suggestions_text