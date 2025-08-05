"""Integration tests for end-to-end optimization workflow."""

import pytest
from unittest.mock import Mock, patch, MagicMock
import json
import asyncio

from src.optimizer.query_optimizer import BigQueryOptimizer
from src.common.models import OptimizationResult, QueryComplexity
from src.common.exceptions import OptimizationError


@pytest.mark.integration
class TestEndToEndOptimization:
    """Test complete end-to-end optimization workflow."""
    
    @patch('src.optimizer.bigquery_client.BigQueryClient')
    @patch('src.optimizer.ai_optimizer.GeminiQueryOptimizer')
    @patch('src.crawler.documentation_processor.DocumentationProcessor')
    def test_simple_query_optimization_flow(self, mock_doc_processor, mock_ai_optimizer, mock_bq_client):
        """Test optimization flow for a simple query."""
        
        # Setup mocks
        mock_bq_instance = Mock()
        mock_bq_instance.test_connection.return_value = True
        mock_bq_client.return_value = mock_bq_instance
        
        mock_doc_instance = Mock()
        mock_doc_instance.get_documentation_summary.return_value = {
            "total_chunks": 100,
            "optimization_patterns": 9
        }
        mock_doc_processor.return_value = mock_doc_instance
        
        # Mock AI optimizer result
        mock_ai_instance = Mock()
        mock_optimization_result = OptimizationResult(
            original_query="SELECT * FROM orders WHERE date > '2024-01-01'",
            query_analysis=Mock(
                complexity=QueryComplexity.SIMPLE,
                table_count=1,
                join_count=0,
                potential_issues=["Using SELECT *"],
                applicable_patterns=["column_pruning"]
            ),
            optimized_query="SELECT order_id, customer_id, total FROM orders WHERE _PARTITIONDATE >= '2024-01-01' AND date > '2024-01-01'",
            optimizations_applied=[
                Mock(
                    pattern_name="Column Pruning",
                    description="Replaced SELECT * with specific columns",
                    expected_improvement=0.2
                ),
                Mock(
                    pattern_name="Partition Filtering", 
                    description="Added partition filter",
                    expected_improvement=0.5
                )
            ],
            total_optimizations=2,
            estimated_improvement=0.6
        )
        mock_ai_instance.optimize_query.return_value = mock_optimization_result
        mock_ai_optimizer.return_value = mock_ai_instance
        
        # Test the optimization
        optimizer = BigQueryOptimizer(validate_results=False)
        
        result = optimizer.optimize_query(
            "SELECT * FROM orders WHERE date > '2024-01-01'",
            validate_results=False,
            measure_performance=False
        )
        
        # Verify results
        assert result is not None
        assert result.total_optimizations == 2
        assert result.estimated_improvement == 0.6
        assert "SELECT order_id, customer_id" in result.optimized_query
        assert "_PARTITIONDATE" in result.optimized_query
    
    @patch('src.optimizer.bigquery_client.BigQueryClient')
    @patch('src.optimizer.ai_optimizer.GeminiQueryOptimizer')
    @patch('src.crawler.documentation_processor.DocumentationProcessor')
    def test_complex_query_with_joins_optimization(self, mock_doc_processor, mock_ai_optimizer, mock_bq_client):
        """Test optimization of complex query with JOINs."""
        
        # Setup mocks similar to previous test
        mock_bq_instance = Mock()
        mock_bq_instance.test_connection.return_value = True
        mock_bq_client.return_value = mock_bq_instance
        
        mock_doc_instance = Mock()
        mock_doc_processor.return_value = mock_doc_instance
        
        complex_query = """
            SELECT c.customer_name, o.order_id, p.product_name, oi.quantity
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            JOIN order_items oi ON o.order_id = oi.order_id
            JOIN products p ON oi.product_id = p.product_id
            WHERE o.order_date >= '2024-01-01'
        """
        
        optimized_query = """
            SELECT c.customer_name, o.order_id, p.product_name, oi.quantity
            FROM products p
            JOIN order_items oi ON p.product_id = oi.product_id
            JOIN orders o ON oi.order_id = o.order_id
            JOIN customers c ON o.customer_id = c.customer_id
            WHERE o._PARTITIONDATE >= '2024-01-01'
            AND o.order_date >= '2024-01-01'
        """
        
        mock_ai_instance = Mock()
        mock_optimization_result = OptimizationResult(
            original_query=complex_query,
            query_analysis=Mock(
                complexity=QueryComplexity.COMPLEX,
                table_count=4,
                join_count=3,
                potential_issues=["Multiple JOINs without optimization", "Missing partition filter"],
                applicable_patterns=["join_reordering", "partition_filtering"]
            ),
            optimized_query=optimized_query,
            optimizations_applied=[
                Mock(
                    pattern_name="JOIN Reordering",
                    description="Reordered JOINs to start with smaller tables",
                    expected_improvement=0.3
                ),
                Mock(
                    pattern_name="Partition Filtering",
                    description="Added partition filter to reduce data scanned",
                    expected_improvement=0.4
                )
            ],
            total_optimizations=2,
            estimated_improvement=0.58  # Combined improvement
        )
        mock_ai_instance.optimize_query.return_value = mock_optimization_result
        mock_ai_optimizer.return_value = mock_ai_instance
        
        optimizer = BigQueryOptimizer(validate_results=False)
        
        result = optimizer.optimize_query(complex_query, validate_results=False)
        
        # Verify complex query optimization
        assert result.total_optimizations == 2
        assert result.estimated_improvement > 0.5
        assert "products p" in result.optimized_query  # Should start with products table
        assert "_PARTITIONDATE" in result.optimized_query
    
    @patch('src.optimizer.bigquery_client.BigQueryClient')
    @patch('src.optimizer.ai_optimizer.GeminiQueryOptimizer')
    @patch('src.crawler.documentation_processor.DocumentationProcessor')
    def test_query_with_validation(self, mock_doc_processor, mock_ai_optimizer, mock_bq_client):
        """Test optimization with result validation."""
        
        # Setup BigQuery client mock for validation
        mock_bq_instance = Mock()
        mock_bq_instance.test_connection.return_value = True
        
        # Mock validation responses
        mock_bq_instance.validate_query.return_value = {
            "valid": True,
            "bytes_processed": 1000000,
            "error": None
        }
        
        # Mock query execution for validation
        mock_bq_instance.execute_query.side_effect = [
            {  # Original query result
                "success": True,
                "results": [{"customer_id": 1, "total": 100}, {"customer_id": 2, "total": 200}],
                "row_count": 2
            },
            {  # Optimized query result
                "success": True, 
                "results": [{"customer_id": 1, "total": 100}, {"customer_id": 2, "total": 200}],
                "row_count": 2
            }
        ]
        
        mock_bq_client.return_value = mock_bq_instance
        
        # Setup other mocks
        mock_doc_instance = Mock()
        mock_doc_processor.return_value = mock_doc_instance
        
        mock_ai_instance = Mock()
        mock_optimization_result = OptimizationResult(
            original_query="SELECT customer_id, SUM(amount) FROM orders GROUP BY customer_id",
            query_analysis=Mock(complexity=QueryComplexity.MODERATE),
            optimized_query="SELECT customer_id, SUM(amount) FROM orders WHERE _PARTITIONDATE >= '2024-01-01' GROUP BY customer_id",
            optimizations_applied=[Mock(pattern_name="Partition Filtering")],
            total_optimizations=1,
            estimated_improvement=0.3
        )
        mock_ai_instance.optimize_query.return_value = mock_optimization_result
        mock_ai_optimizer.return_value = mock_ai_instance
        
        optimizer = BigQueryOptimizer(validate_results=True)
        
        result = optimizer.optimize_query(
            "SELECT customer_id, SUM(amount) FROM orders GROUP BY customer_id",
            validate_results=True,
            sample_size=1000
        )
        
        # Verify validation was performed
        assert result.results_identical == True
        assert mock_bq_instance.execute_query.call_count == 2  # Original + optimized
    
    @patch('src.optimizer.bigquery_client.BigQueryClient')
    @patch('src.optimizer.ai_optimizer.GeminiQueryOptimizer')
    @patch('src.crawler.documentation_processor.DocumentationProcessor')
    def test_query_with_performance_measurement(self, mock_doc_processor, mock_ai_optimizer, mock_bq_client):
        """Test optimization with performance measurement."""
        
        # Setup BigQuery client mock
        mock_bq_instance = Mock()
        mock_bq_instance.test_connection.return_value = True
        
        # Mock performance comparison
        mock_bq_instance.compare_query_performance.return_value = {
            "success": True,
            "original_avg_ms": 5000,
            "optimized_avg_ms": 3000,
            "improvement_percentage": 0.4,  # 40% improvement
            "iterations": 3
        }
        
        mock_bq_client.return_value = mock_bq_instance
        
        # Setup other mocks
        mock_doc_instance = Mock()
        mock_doc_processor.return_value = mock_doc_instance
        
        mock_ai_instance = Mock()
        mock_optimization_result = OptimizationResult(
            original_query="SELECT COUNT(DISTINCT customer_id) FROM large_orders",
            query_analysis=Mock(complexity=QueryComplexity.MODERATE),
            optimized_query="SELECT APPROX_COUNT_DISTINCT(customer_id) FROM large_orders WHERE _PARTITIONDATE >= '2024-01-01'",
            optimizations_applied=[
                Mock(pattern_name="Approximate Aggregation"),
                Mock(pattern_name="Partition Filtering")
            ],
            total_optimizations=2,
            estimated_improvement=0.6
        )
        mock_ai_instance.optimize_query.return_value = mock_optimization_result
        mock_ai_optimizer.return_value = mock_ai_instance
        
        optimizer = BigQueryOptimizer(validate_results=False)
        
        result = optimizer.optimize_query(
            "SELECT COUNT(DISTINCT customer_id) FROM large_orders",
            validate_results=False,
            measure_performance=True
        )
        
        # Verify performance measurement
        assert result.actual_improvement == 0.4
        assert result.original_performance is not None
        assert result.optimized_performance is not None
        assert result.original_performance.execution_time_ms == 5000
        assert result.optimized_performance.execution_time_ms == 3000
    
    @patch('src.optimizer.bigquery_client.BigQueryClient')
    @patch('src.optimizer.ai_optimizer.GeminiQueryOptimizer')
    @patch('src.crawler.documentation_processor.DocumentationProcessor')
    def test_batch_optimization(self, mock_doc_processor, mock_ai_optimizer, mock_bq_client):
        """Test batch optimization of multiple queries."""
        
        # Setup mocks
        mock_bq_instance = Mock()
        mock_bq_instance.test_connection.return_value = True
        mock_bq_client.return_value = mock_bq_instance
        
        mock_doc_instance = Mock()
        mock_doc_processor.return_value = mock_doc_instance
        
        # Mock AI optimizer to return different results for different queries
        mock_ai_instance = Mock()
        
        def mock_optimize_query(query, analysis, patterns, context=None):
            if "SELECT *" in query:
                return OptimizationResult(
                    original_query=query,
                    query_analysis=analysis,
                    optimized_query=query.replace("SELECT *", "SELECT id, name"),
                    optimizations_applied=[Mock(pattern_name="Column Pruning")],
                    total_optimizations=1,
                    estimated_improvement=0.2
                )
            elif "COUNT(DISTINCT" in query:
                return OptimizationResult(
                    original_query=query,
                    query_analysis=analysis,
                    optimized_query=query.replace("COUNT(DISTINCT", "APPROX_COUNT_DISTINCT("),
                    optimizations_applied=[Mock(pattern_name="Approximate Aggregation")],
                    total_optimizations=1,
                    estimated_improvement=0.5
                )
            else:
                return OptimizationResult(
                    original_query=query,
                    query_analysis=analysis,
                    optimized_query=query,
                    optimizations_applied=[],
                    total_optimizations=0
                )
        
        mock_ai_instance.optimize_query.side_effect = mock_optimize_query
        mock_ai_optimizer.return_value = mock_ai_instance
        
        queries = [
            "SELECT * FROM customers",
            "SELECT COUNT(DISTINCT customer_id) FROM orders",
            "SELECT customer_id FROM orders WHERE date >= '2024-01-01'"
        ]
        
        optimizer = BigQueryOptimizer(validate_results=False)
        
        results = optimizer.batch_optimize_queries(queries, validate_results=False)
        
        # Verify batch results
        assert len(results) == 3
        assert results[0].total_optimizations == 1  # Column pruning
        assert results[1].total_optimizations == 1  # Approximate aggregation
        assert results[2].total_optimizations == 0  # No optimization needed
        
        assert "SELECT id, name" in results[0].optimized_query
        assert "APPROX_COUNT_DISTINCT" in results[1].optimized_query
    
    @patch('src.optimizer.bigquery_client.BigQueryClient')
    @patch('src.optimizer.ai_optimizer.GeminiQueryOptimizer')
    @patch('src.crawler.documentation_processor.DocumentationProcessor')
    def test_error_handling_in_optimization_flow(self, mock_doc_processor, mock_ai_optimizer, mock_bq_client):
        """Test error handling throughout the optimization flow."""
        
        # Setup BigQuery client to fail connection
        mock_bq_instance = Mock()
        mock_bq_instance.test_connection.return_value = False
        mock_bq_client.return_value = mock_bq_instance
        
        mock_doc_instance = Mock()
        mock_doc_processor.return_value = mock_doc_instance
        
        mock_ai_instance = Mock()
        mock_ai_optimizer.return_value = mock_ai_instance
        
        optimizer = BigQueryOptimizer(validate_results=False)
        
        # Test with connection failure
        result = optimizer.optimize_query("SELECT * FROM table", validate_results=False)
        
        # Should return a result with error information
        assert result is not None
        assert result.validation_error is not None
        assert result.total_optimizations == 0
        assert result.optimized_query == "SELECT * FROM table"  # Original query returned
    
    @patch('src.optimizer.bigquery_client.BigQueryClient')
    @patch('src.optimizer.ai_optimizer.GeminiQueryOptimizer')
    @patch('src.crawler.documentation_processor.DocumentationProcessor')
    def test_validation_failure_handling(self, mock_doc_processor, mock_ai_optimizer, mock_bq_client):
        """Test handling of validation failures."""
        
        # Setup BigQuery client
        mock_bq_instance = Mock()
        mock_bq_instance.test_connection.return_value = True
        
        # Mock validation to show different results
        mock_bq_instance.validate_query.return_value = {"valid": True}
        mock_bq_instance.execute_query.side_effect = [
            {  # Original query result
                "success": True,
                "results": [{"count": 100}],
                "row_count": 1
            },
            {  # Optimized query result (different!)
                "success": True,
                "results": [{"count": 95}],  # Different result!
                "row_count": 1
            }
        ]
        
        mock_bq_client.return_value = mock_bq_instance
        
        # Setup other mocks
        mock_doc_instance = Mock()
        mock_doc_processor.return_value = mock_doc_instance
        
        mock_ai_instance = Mock()
        mock_optimization_result = OptimizationResult(
            original_query="SELECT COUNT(*) as count FROM orders",
            query_analysis=Mock(complexity=QueryComplexity.SIMPLE),
            optimized_query="SELECT APPROX_COUNT_DISTINCT(order_id) as count FROM orders",
            optimizations_applied=[Mock(pattern_name="Approximate Aggregation")],
            total_optimizations=1,
            estimated_improvement=0.5
        )
        mock_ai_instance.optimize_query.return_value = mock_optimization_result
        mock_ai_optimizer.return_value = mock_ai_instance
        
        optimizer = BigQueryOptimizer(validate_results=True)
        
        result = optimizer.optimize_query(
            "SELECT COUNT(*) as count FROM orders",
            validate_results=True
        )
        
        # Should detect that results don't match
        assert result.results_identical == False
        assert result.validation_error is not None


@pytest.mark.integration
class TestAnalysisOnlyWorkflow:
    """Test analysis-only functionality."""
    
    @patch('src.optimizer.bigquery_client.BigQueryClient')
    @patch('src.crawler.documentation_processor.DocumentationProcessor')
    def test_query_analysis_only(self, mock_doc_processor, mock_bq_client):
        """Test analyzing a query without optimization."""
        
        # Setup mocks
        mock_bq_instance = Mock()
        mock_bq_instance.test_connection.return_value = True
        mock_bq_client.return_value = mock_bq_instance
        
        mock_doc_instance = Mock()
        mock_doc_processor.return_value = mock_doc_instance
        
        optimizer = BigQueryOptimizer(validate_results=False)
        
        query = """
            SELECT c.customer_name, COUNT(*) as order_count
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            WHERE o.order_date >= '2024-01-01'
            GROUP BY c.customer_name
            HAVING COUNT(*) > 5
        """
        
        analysis = optimizer.analyze_query_only(query)
        
        # Verify analysis results
        assert analysis is not None
        assert analysis.original_query == query
        assert analysis.table_count >= 2
        assert analysis.join_count >= 1
        assert analysis.aggregate_function_count >= 1
        assert len(analysis.potential_issues) >= 0
        assert len(analysis.applicable_patterns) >= 0
    
    @patch('src.optimizer.bigquery_client.BigQueryClient')
    @patch('src.crawler.documentation_processor.DocumentationProcessor')
    def test_optimization_suggestions_only(self, mock_doc_processor, mock_bq_client):
        """Test getting optimization suggestions without applying them."""
        
        # Setup mocks
        mock_bq_instance = Mock()
        mock_bq_instance.test_connection.return_value = True
        mock_bq_client.return_value = mock_bq_instance
        
        mock_doc_instance = Mock()
        # Mock documentation search results
        mock_doc_instance.search_documentation.return_value = [
            {
                "content": "JOIN optimization techniques...",
                "title": "JOIN Performance",
                "optimization_patterns": ["join_reordering"]
            }
        ]
        mock_doc_processor.return_value = mock_doc_instance
        
        optimizer = BigQueryOptimizer(validate_results=False)
        
        query = "SELECT * FROM table1 t1 JOIN table2 t2 ON t1.id = t2.id"
        
        suggestions = optimizer.get_optimization_suggestions(query)
        
        # Verify suggestions structure
        assert "analysis" in suggestions
        assert "applicable_patterns" in suggestions
        assert "specific_suggestions" in suggestions
        assert "documentation_references" in suggestions
        assert "priority_optimizations" in suggestions
        
        # Verify analysis was performed
        analysis = suggestions["analysis"]
        assert analysis["table_count"] >= 2
        assert analysis["join_count"] >= 1


@pytest.mark.integration
class TestSystemIntegration:
    """Test system-level integration functionality."""
    
    @patch('src.optimizer.bigquery_client.BigQueryClient')
    @patch('src.crawler.documentation_processor.DocumentationProcessor')
    def test_system_status_check(self, mock_doc_processor, mock_bq_client):
        """Test system status and connection testing."""
        
        # Setup mocks for successful connections
        mock_bq_instance = Mock()
        mock_bq_instance.test_connection.return_value = True
        mock_bq_client.return_value = mock_bq_instance
        
        mock_doc_instance = Mock()
        mock_doc_instance.get_documentation_summary.return_value = {
            "total_chunks": 150,
            "optimization_patterns": 9,
            "embedding_model": "all-MiniLM-L6-v2"
        }
        mock_doc_processor.return_value = mock_doc_instance
        
        optimizer = BigQueryOptimizer(validate_results=False)
        
        # Test connection
        connection_ok = optimizer.test_connection()
        assert connection_ok == True
        
        # Test statistics
        stats = optimizer.get_optimization_statistics()
        assert "available_patterns" in stats
        assert "documentation_chunks" in stats
        assert "bigquery_project" in stats
        assert stats["documentation_chunks"] == 150
        assert stats["available_patterns"] == 9
    
    @patch('src.optimizer.bigquery_client.BigQueryClient')
    @patch('src.crawler.documentation_processor.DocumentationProcessor')
    def test_table_optimization_suggestions(self, mock_doc_processor, mock_bq_client):
        """Test table-level optimization suggestions."""
        
        # Setup mocks
        mock_bq_instance = Mock()
        mock_bq_instance.test_connection.return_value = True
        mock_bq_instance.get_table_info.return_value = {
            "table_id": "orders",
            "num_rows": 10000000,
            "num_bytes": 5000000000,  # 5GB
            "partitioning": {"type": None},
            "clustering": {"fields": []},
            "schema": [
                {"name": "order_id", "type": "INTEGER"},
                {"name": "customer_id", "type": "INTEGER"},
                {"name": "order_date", "type": "DATE"}
            ]
        }
        mock_bq_client.return_value = mock_bq_instance
        
        mock_doc_instance = Mock()
        mock_doc_processor.return_value = mock_doc_instance
        
        optimizer = BigQueryOptimizer(validate_results=False)
        
        suggestions = optimizer.get_table_optimization_suggestions(
            "project.dataset.orders",
            sample_queries=["SELECT * FROM orders WHERE order_date >= '2024-01-01'"]
        )
        
        # Verify suggestions
        assert len(suggestions) > 0
        
        # Should suggest partitioning for large table without partitioning
        partitioning_suggested = any("partition" in s.lower() for s in suggestions)
        assert partitioning_suggested == True
        
        # Should suggest clustering for table without clustering
        clustering_suggested = any("cluster" in s.lower() for s in suggestions)
        assert clustering_suggested == True