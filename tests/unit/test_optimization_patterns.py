"""Unit tests for optimization patterns and AI optimization."""

import pytest
from unittest.mock import Mock, patch, MagicMock
import json

from src.optimizer.ai_optimizer import GeminiQueryOptimizer
from src.common.models import (
    QueryAnalysis, OptimizationPattern, OptimizationType, 
    QueryComplexity, AppliedOptimization
)
from src.common.exceptions import OptimizationError


@pytest.mark.unit
class TestOptimizationPatterns:
    """Test optimization pattern identification and application."""
    
    def test_optimization_pattern_creation(self):
        """Test creation of optimization patterns."""
        pattern = OptimizationPattern(
            pattern_id="test_pattern",
            name="Test Pattern",
            description="A test optimization pattern",
            optimization_type=OptimizationType.JOIN_REORDERING,
            expected_improvement=0.3,
            applicability_conditions=["JOIN", "WHERE"],
            sql_pattern=r".*JOIN.*",
            replacement_pattern="Optimized JOIN"
        )
        
        assert pattern.pattern_id == "test_pattern"
        assert pattern.expected_improvement == 0.3
        assert "JOIN" in pattern.applicability_conditions
        assert pattern.optimization_type == OptimizationType.JOIN_REORDERING
    
    def test_pattern_applicability_matching(self, mock_documentation_processor):
        """Test matching patterns to queries based on applicability conditions."""
        from src.mcp_server.handlers import OptimizationHandler
        
        handler = OptimizationHandler(mock_documentation_processor)
        
        # Test JOIN pattern matching
        join_query = "SELECT * FROM table1 t1 JOIN table2 t2 ON t1.id = t2.id"
        join_patterns = handler._find_applicable_patterns(join_query)
        
        assert "join_reordering" in join_patterns
        
        # Test SELECT * pattern matching
        select_star_query = "SELECT * FROM table WHERE date > '2024-01-01'"
        star_patterns = handler._find_applicable_patterns(select_star_query)
        
        assert "column_pruning" in star_patterns
        
        # Test COUNT DISTINCT pattern matching
        count_distinct_query = "SELECT COUNT(DISTINCT customer_id) FROM orders"
        count_patterns = handler._find_applicable_patterns(count_distinct_query)
        
        assert "approximate_aggregation" in count_patterns
    
    def test_pattern_priority_calculation(self, mock_documentation_processor):
        """Test priority calculation for optimization patterns."""
        from src.mcp_server.handlers import OptimizationHandler
        
        handler = OptimizationHandler(mock_documentation_processor)
        
        # Create test patterns with different expected improvements
        high_impact_pattern = OptimizationPattern(
            pattern_id="high_impact",
            name="High Impact",
            description="High impact optimization",
            optimization_type=OptimizationType.PARTITION_FILTERING,
            expected_improvement=0.7
        )
        
        low_impact_pattern = OptimizationPattern(
            pattern_id="low_impact", 
            name="Low Impact",
            description="Low impact optimization",
            optimization_type=OptimizationType.COLUMN_PRUNING,
            expected_improvement=0.1
        )
        
        # Create test analysis
        analysis = QueryAnalysis(
            original_query="test",
            query_hash="test",
            complexity=QueryComplexity.COMPLEX,
            table_count=1,
            join_count=0,
            subquery_count=0,
            window_function_count=0,
            aggregate_function_count=0,
            potential_issues=[],
            applicable_patterns=[]
        )
        
        high_priority = handler._calculate_priority(high_impact_pattern, analysis)
        low_priority = handler._calculate_priority(low_impact_pattern, analysis)
        
        assert high_priority > low_priority


@pytest.mark.unit
class TestAIOptimizer:
    """Test AI-powered query optimization."""
    
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_ai_optimizer_initialization(self, mock_model, mock_configure, test_settings):
        """Test AI optimizer initialization."""
        with patch('config.settings.get_settings', return_value=test_settings):
            optimizer = GeminiQueryOptimizer()
            
            assert optimizer.settings.gemini_api_key == "test-api-key"
            mock_configure.assert_called_once_with(api_key="test-api-key")
            mock_model.assert_called_once_with("gemini-pro")
    
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_optimization_prompt_building(self, mock_model, mock_configure, 
                                        test_settings, test_query_analysis):
        """Test building of optimization prompts."""
        with patch('config.settings.get_settings', return_value=test_settings):
            optimizer = GeminiQueryOptimizer()
            
            patterns = [
                OptimizationPattern(
                    pattern_id="test_pattern",
                    name="Test Pattern",
                    description="Test optimization",
                    optimization_type=OptimizationType.COLUMN_PRUNING,
                    expected_improvement=0.2
                )
            ]
            
            documentation_context = [
                {
                    "title": "Test Doc",
                    "content": "Test documentation content",
                    "optimization_patterns": ["column_pruning"]
                }
            ]
            
            prompt = optimizer._build_optimization_prompt(
                "SELECT * FROM table",
                test_query_analysis,
                patterns,
                documentation_context
            )
            
            assert "SELECT * FROM table" in prompt
            assert "Test Pattern" in prompt
            assert "Test documentation content" in prompt
            assert "moderate" in prompt.lower()  # complexity from test_query_analysis
    
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_ai_response_parsing(self, mock_model, mock_configure, test_settings, mock_gemini_response):
        """Test parsing of AI responses."""
        with patch('config.settings.get_settings', return_value=test_settings):
            optimizer = GeminiQueryOptimizer()
            
            # Test valid JSON response
            json_response = json.dumps(mock_gemini_response)
            parsed_data = optimizer._parse_ai_response(json_response)
            
            assert "optimized_query" in parsed_data
            assert "optimizations_applied" in parsed_data
            assert len(parsed_data["optimizations_applied"]) > 0
            
            # Test response with markdown code blocks
            markdown_response = f"```json\n{json_response}\n```"
            parsed_data = optimizer._parse_ai_response(markdown_response)
            
            assert "optimized_query" in parsed_data
            
            # Test invalid JSON response
            with pytest.raises(OptimizationError):
                optimizer._parse_ai_response("invalid json")
    
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_optimization_result_creation(self, mock_model, mock_configure, 
                                        test_settings, test_query_analysis, mock_gemini_response):
        """Test creation of optimization results from AI responses."""
        with patch('config.settings.get_settings', return_value=test_settings):
            optimizer = GeminiQueryOptimizer()
            
            result = optimizer._create_optimization_result(
                "SELECT * FROM table",
                test_query_analysis,
                mock_gemini_response,
                0.0  # start_time
            )
            
            assert result.original_query == "SELECT * FROM table"
            assert result.query_analysis == test_query_analysis
            assert result.total_optimizations == 1
            assert result.estimated_improvement == 0.5
            assert len(result.optimizations_applied) == 1
            
            optimization = result.optimizations_applied[0]
            assert optimization.pattern_id == "partition_filtering"
            assert optimization.expected_improvement == 0.5
    
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_full_optimization_flow(self, mock_model, mock_configure, 
                                  test_settings, test_query_analysis, mock_gemini_response):
        """Test complete optimization flow."""
        with patch('config.settings.get_settings', return_value=test_settings):
            # Setup mock model response
            mock_response = Mock()
            mock_response.text = json.dumps(mock_gemini_response)
            
            mock_model_instance = Mock()
            mock_model_instance.generate_content.return_value = mock_response
            mock_model.return_value = mock_model_instance
            
            optimizer = GeminiQueryOptimizer()
            
            patterns = [
                OptimizationPattern(
                    pattern_id="partition_filtering",
                    name="Partition Filtering",
                    description="Add partition filters",
                    optimization_type=OptimizationType.PARTITION_FILTERING,
                    expected_improvement=0.5
                )
            ]
            
            result = optimizer.optimize_query(
                "SELECT * FROM table WHERE date > '2024-01-01'",
                test_query_analysis,
                patterns
            )
            
            # Verify optimization was applied
            assert result.total_optimizations == 1
            assert result.estimated_improvement == 0.5
            assert "partition" in result.optimizations_applied[0].pattern_name.lower()
            
            # Verify AI model was called
            mock_model_instance.generate_content.assert_called_once()
    
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_optimization_error_handling(self, mock_model, mock_configure, 
                                       test_settings, test_query_analysis):
        """Test error handling in optimization process."""
        with patch('config.settings.get_settings', return_value=test_settings):
            # Setup mock to raise exception
            mock_model_instance = Mock()
            mock_model_instance.generate_content.side_effect = Exception("API Error")
            mock_model.return_value = mock_model_instance
            
            optimizer = GeminiQueryOptimizer()
            
            result = optimizer.optimize_query(
                "SELECT * FROM table",
                test_query_analysis,
                []
            )
            
            # Should return original query on error
            assert result.optimized_query == "SELECT * FROM table"
            assert result.total_optimizations == 0
            assert result.validation_error is not None
    
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_explanation_generation(self, mock_model, mock_configure, test_settings):
        """Test generation of optimization explanations."""
        with patch('config.settings.get_settings', return_value=test_settings):
            mock_response = Mock()
            mock_response.text = "This optimization improves performance by..."
            
            mock_model_instance = Mock()
            mock_model_instance.generate_content.return_value = mock_response
            mock_model.return_value = mock_model_instance
            
            optimizer = GeminiQueryOptimizer()
            
            optimizations = [
                AppliedOptimization(
                    pattern_id="test",
                    pattern_name="Test Optimization",
                    description="Test description",
                    before_snippet="SELECT *",
                    after_snippet="SELECT col1, col2",
                    expected_improvement=0.2
                )
            ]
            
            explanation = optimizer.generate_explanation(
                "SELECT * FROM table",
                "SELECT col1, col2 FROM table",
                optimizations
            )
            
            assert "improves performance" in explanation
            mock_model_instance.generate_content.assert_called_once()
    
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_table_optimization_suggestions(self, mock_model, mock_configure, test_settings):
        """Test generation of table-level optimization suggestions."""
        with patch('config.settings.get_settings', return_value=test_settings):
            mock_response = Mock()
            mock_response.text = json.dumps([
                "Consider partitioning by date column",
                "Add clustering keys for frequently filtered columns"
            ])
            
            mock_model_instance = Mock()
            mock_model_instance.generate_content.return_value = mock_response
            mock_model.return_value = mock_model_instance
            
            optimizer = GeminiQueryOptimizer()
            
            table_info = {
                "table_id": "test_table",
                "num_rows": 1000000,
                "partitioning": {"type": None},
                "clustering": {"fields": []}
            }
            
            suggestions = optimizer.suggest_table_optimizations(
                "SELECT * FROM test_table WHERE date > '2024-01-01'",
                table_info
            )
            
            assert len(suggestions) == 2
            assert "partitioning" in suggestions[0].lower()
            assert "clustering" in suggestions[1].lower()


@pytest.mark.unit
class TestOptimizationSpecificPatterns:
    """Test specific optimization pattern implementations."""
    
    def test_join_reordering_pattern(self, mock_documentation_processor):
        """Test JOIN reordering optimization pattern."""
        from src.mcp_server.handlers import OptimizationHandler
        
        handler = OptimizationHandler(mock_documentation_processor)
        
        # Query with multiple JOINs that could benefit from reordering
        query = """
            SELECT c.name, o.total, p.name
            FROM large_customers c
            JOIN small_products p ON c.preferred_product = p.id
            JOIN huge_orders o ON c.id = o.customer_id
            WHERE o.date >= '2024-01-01'
        """
        
        advice = handler._generate_specific_advice(query, OptimizationPattern(
            pattern_id="join_reordering",
            name="JOIN Reordering",
            description="Reorder JOINs",
            optimization_type=OptimizationType.JOIN_REORDERING
        ))
        
        assert "smaller tables first" in advice.lower()
        assert "selective conditions" in advice.lower()
    
    def test_partition_filtering_pattern(self, mock_documentation_processor):
        """Test partition filtering optimization pattern."""
        from src.mcp_server.handlers import OptimizationHandler
        
        handler = OptimizationHandler(mock_documentation_processor)
        
        query = "SELECT * FROM orders WHERE order_date >= '2024-01-01'"
        
        advice = handler._generate_specific_advice(query, OptimizationPattern(
            pattern_id="partition_filtering",
            name="Partition Filtering",
            description="Add partition filters",
            optimization_type=OptimizationType.PARTITION_FILTERING
        ))
        
        assert "_PARTITIONDATE" in advice or "partition filter" in advice.lower()
    
    def test_approximate_aggregation_pattern(self, mock_documentation_processor):
        """Test approximate aggregation optimization pattern."""
        from src.mcp_server.handlers import OptimizationHandler
        
        handler = OptimizationHandler(mock_documentation_processor)
        
        query = "SELECT COUNT(DISTINCT customer_id) FROM large_orders"
        
        advice = handler._generate_specific_advice(query, OptimizationPattern(
            pattern_id="approximate_aggregation",
            name="Approximate Aggregation",
            description="Use approximate functions",
            optimization_type=OptimizationType.APPROXIMATE_AGGREGATION
        ))
        
        assert "APPROX_COUNT_DISTINCT" in advice
    
    def test_column_pruning_pattern(self, mock_documentation_processor):
        """Test column pruning optimization pattern."""
        from src.mcp_server.handlers import OptimizationHandler
        
        handler = OptimizationHandler(mock_documentation_processor)
        
        query = "SELECT * FROM large_table WHERE date > '2024-01-01'"
        
        advice = handler._generate_specific_advice(query, OptimizationPattern(
            pattern_id="column_pruning",
            name="Column Pruning",
            description="Select specific columns",
            optimization_type=OptimizationType.COLUMN_PRUNING
        ))
        
        assert "specific column" in advice.lower()
        assert "SELECT *" in advice or "reduce data transfer" in advice.lower()
    
    def test_window_function_optimization_pattern(self, mock_documentation_processor):
        """Test window function optimization pattern."""
        from src.mcp_server.handlers import OptimizationHandler
        
        handler = OptimizationHandler(mock_documentation_processor)
        
        query = """
            SELECT customer_id, 
                   ROW_NUMBER() OVER (ORDER BY order_date) as rn
            FROM orders
        """
        
        advice = handler._generate_specific_advice(query, OptimizationPattern(
            pattern_id="window_optimization",
            name="Window Function Optimization",
            description="Optimize window functions",
            optimization_type=OptimizationType.WINDOW_OPTIMIZATION
        ))
        
        assert "PARTITION BY" in advice
        assert "ORDER BY" in advice