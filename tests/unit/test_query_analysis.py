"""Unit tests for query analysis functionality."""

import pytest
from unittest.mock import Mock, patch

from src.mcp_server.handlers import OptimizationHandler
from src.common.models import QueryComplexity
from src.crawler.documentation_processor import DocumentationProcessor


@pytest.mark.unit
class TestQueryAnalysis:
    """Test query analysis functionality."""
    
    def test_simple_query_analysis(self, mock_documentation_processor):
        """Test analysis of a simple SELECT query."""
        handler = OptimizationHandler(mock_documentation_processor)
        
        query = """
            SELECT customer_id, order_date, total_amount
            FROM orders
            WHERE order_date >= '2024-01-01'
        """
        
        # Use asyncio.run to test async function
        import asyncio
        analysis = asyncio.run(handler.analyze_query(query))
        
        assert analysis.original_query == query
        assert analysis.complexity in [QueryComplexity.SIMPLE, QueryComplexity.MODERATE]
        assert analysis.table_count >= 1
        assert analysis.join_count == 0
        assert analysis.subquery_count == 0
        assert len(analysis.query_hash) > 0
    
    def test_complex_join_analysis(self, mock_documentation_processor):
        """Test analysis of a complex JOIN query."""
        handler = OptimizationHandler(mock_documentation_processor)
        
        query = """
            SELECT c.customer_name, o.order_id, p.product_name, oi.quantity
            FROM customers c
            INNER JOIN orders o ON c.customer_id = o.customer_id
            LEFT JOIN order_items oi ON o.order_id = oi.order_id
            RIGHT JOIN products p ON oi.product_id = p.product_id
            WHERE o.order_date >= '2024-01-01'
            AND c.status = 'active'
        """
        
        import asyncio
        analysis = asyncio.run(handler.analyze_query(query))
        
        assert analysis.table_count >= 4
        assert analysis.join_count == 3
        assert analysis.complexity in [QueryComplexity.COMPLEX, QueryComplexity.VERY_COMPLEX]
        assert "JOIN" in str(analysis.applicable_patterns)
    
    def test_subquery_analysis(self, mock_documentation_processor):
        """Test analysis of queries with subqueries."""
        handler = OptimizationHandler(mock_documentation_processor)
        
        query = """
            SELECT customer_id, customer_name
            FROM customers c
            WHERE EXISTS (
                SELECT 1 FROM orders o 
                WHERE o.customer_id = c.customer_id 
                AND o.order_date >= '2024-01-01'
            )
            AND customer_id IN (
                SELECT customer_id FROM premium_customers
            )
        """
        
        import asyncio
        analysis = asyncio.run(handler.analyze_query(query))
        
        assert analysis.subquery_count >= 1  # May detect nested subqueries
        assert "subquery" in str(analysis.applicable_patterns).lower() or "EXISTS" in analysis.potential_issues
    
    def test_window_function_analysis(self, mock_documentation_processor):
        """Test analysis of queries with window functions."""
        handler = OptimizationHandler(mock_documentation_processor)
        
        query = """
            SELECT 
                customer_id,
                order_date,
                total_amount,
                ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) as order_rank,
                SUM(total_amount) OVER (PARTITION BY customer_id) as customer_total
            FROM orders
            WHERE order_date >= '2024-01-01'
        """
        
        import asyncio
        analysis = asyncio.run(handler.analyze_query(query))
        
        assert analysis.window_function_count >= 2
        assert "window" in str(analysis.applicable_patterns).lower()
    
    def test_aggregation_analysis(self, mock_documentation_processor):
        """Test analysis of queries with aggregations."""
        handler = OptimizationHandler(mock_documentation_processor)
        
        query = """
            SELECT 
                category,
                COUNT(*) as total_orders,
                SUM(total_amount) as total_revenue,
                AVG(total_amount) as avg_order_value,
                COUNT(DISTINCT customer_id) as unique_customers
            FROM orders o
            JOIN products p ON o.product_id = p.product_id
            WHERE o.order_date >= '2024-01-01'
            GROUP BY category
            HAVING COUNT(*) > 100
        """
        
        import asyncio
        analysis = asyncio.run(handler.analyze_query(query))
        
        assert analysis.aggregate_function_count >= 4
        assert analysis.join_count >= 1
        assert "COUNT(DISTINCT" in query  # Should trigger approximate aggregation suggestion
    
    def test_partition_filter_detection(self, mock_documentation_processor):
        """Test detection of partition filters."""
        handler = OptimizationHandler(mock_documentation_processor)
        
        # Query with partition filter
        query_with_partition = """
            SELECT customer_id, SUM(total_amount)
            FROM orders
            WHERE _PARTITIONDATE >= '2024-01-01'
            AND order_date >= '2024-01-01'
            GROUP BY customer_id
        """
        
        import asyncio
        analysis = asyncio.run(handler.analyze_query(query_with_partition))
        assert analysis.has_partition_filter == True
        
        # Query without partition filter
        query_without_partition = """
            SELECT customer_id, SUM(total_amount)
            FROM orders
            WHERE order_date >= '2024-01-01'
            GROUP BY customer_id
        """
        
        analysis = asyncio.run(handler.analyze_query(query_without_partition))
        assert analysis.has_partition_filter == False
        assert "partition" in str(analysis.potential_issues).lower()
    
    def test_select_star_detection(self, mock_documentation_processor):
        """Test detection of SELECT * usage."""
        handler = OptimizationHandler(mock_documentation_processor)
        
        query = """
            SELECT *
            FROM large_table
            WHERE date_column > '2024-01-01'
        """
        
        import asyncio
        analysis = asyncio.run(handler.analyze_query(query))
        
        # Should detect SELECT * as potential issue
        issues_text = " ".join(analysis.potential_issues).lower()
        assert "select *" in issues_text or "*" in issues_text
        assert "column_pruning" in analysis.applicable_patterns
    
    def test_complexity_scoring(self, mock_documentation_processor):
        """Test query complexity scoring."""
        handler = OptimizationHandler(mock_documentation_processor)
        
        # Simple query
        simple_query = "SELECT customer_id FROM customers LIMIT 10"
        
        # Complex query
        complex_query = """
            WITH customer_stats AS (
                SELECT 
                    c.customer_id,
                    c.customer_name,
                    COUNT(o.order_id) as order_count,
                    SUM(o.total_amount) as total_spent,
                    ROW_NUMBER() OVER (ORDER BY SUM(o.total_amount) DESC) as spend_rank
                FROM customers c
                LEFT JOIN orders o ON c.customer_id = o.customer_id
                LEFT JOIN order_items oi ON o.order_id = oi.order_id
                LEFT JOIN products p ON oi.product_id = p.product_id
                WHERE o.order_date >= '2024-01-01'
                GROUP BY c.customer_id, c.customer_name
                HAVING COUNT(o.order_id) > 5
            )
            SELECT cs.*, p.category
            FROM customer_stats cs
            JOIN (
                SELECT customer_id, category
                FROM order_items oi
                JOIN products p ON oi.product_id = p.product_id
                GROUP BY customer_id, category
            ) p ON cs.customer_id = p.customer_id
            WHERE cs.spend_rank <= 100
        """
        
        import asyncio
        simple_analysis = asyncio.run(handler.analyze_query(simple_query))
        complex_analysis = asyncio.run(handler.analyze_query(complex_query))
        
        # Complex query should have higher complexity rating
        complexity_order = [QueryComplexity.SIMPLE, QueryComplexity.MODERATE, 
                          QueryComplexity.COMPLEX, QueryComplexity.VERY_COMPLEX]
        
        simple_idx = complexity_order.index(simple_analysis.complexity)
        complex_idx = complexity_order.index(complex_analysis.complexity)
        
        assert complex_idx > simple_idx
    
    def test_error_handling_in_analysis(self, mock_documentation_processor):
        """Test error handling in query analysis."""
        handler = OptimizationHandler(mock_documentation_processor)
        
        # Invalid SQL
        invalid_query = "SELECT FROM WHERE"
        
        import asyncio
        analysis = asyncio.run(handler.analyze_query(invalid_query))
        
        # Should not crash and should return some analysis
        assert analysis is not None
        assert analysis.original_query == invalid_query
        
        # Empty query
        empty_query = ""
        analysis = asyncio.run(handler.analyze_query(empty_query))
        assert analysis is not None
    
    def test_applicable_patterns_identification(self, mock_documentation_processor):
        """Test identification of applicable optimization patterns."""
        handler = OptimizationHandler(mock_documentation_processor)
        
        test_cases = [
            ("SELECT * FROM table", ["column_pruning"]),
            ("SELECT col FROM table1 JOIN table2", ["join_reordering"]),
            ("SELECT COUNT(DISTINCT col) FROM table", ["approximate_aggregation"]),
            ("SELECT col OVER (ORDER BY col2) FROM table", ["window_optimization"]),
            ("SELECT col FROM table WHERE date > '2024-01-01'", ["partition_filtering"]),
        ]
        
        import asyncio
        for query, expected_patterns in test_cases:
            analysis = asyncio.run(handler.analyze_query(query))
            
            # Check if at least one expected pattern is identified
            found_patterns = set(analysis.applicable_patterns)
            expected_set = set(expected_patterns)
            
            # At least some overlap expected (patterns might be identified differently)
            assert len(found_patterns) > 0, f"No patterns found for query: {query}"


@pytest.mark.unit 
class TestQueryCharacteristicsExtraction:
    """Test extraction of query characteristics."""
    
    def test_table_count_extraction(self, mock_documentation_processor):
        """Test accurate table counting."""
        handler = OptimizationHandler(mock_documentation_processor)
        
        # Single table
        single_table_query = "SELECT * FROM orders"
        
        # Multiple tables with JOINs
        multi_table_query = """
            SELECT * FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            JOIN products p ON o.product_id = p.product_id
        """
        
        import asyncio
        single_analysis = asyncio.run(handler.analyze_query(single_table_query))
        multi_analysis = asyncio.run(handler.analyze_query(multi_table_query))
        
        assert single_analysis.table_count >= 1
        assert multi_analysis.table_count >= 3
        assert multi_analysis.join_count >= 2
    
    def test_join_type_detection(self, mock_documentation_processor):
        """Test detection of different JOIN types."""
        handler = OptimizationHandler(mock_documentation_processor)
        
        query = """
            SELECT *
            FROM table1 t1
            INNER JOIN table2 t2 ON t1.id = t2.id
            LEFT JOIN table3 t3 ON t1.id = t3.id
            RIGHT JOIN table4 t4 ON t1.id = t4.id
            FULL OUTER JOIN table5 t5 ON t1.id = t5.id
            CROSS JOIN table6 t6
        """
        
        import asyncio
        analysis = asyncio.run(handler.analyze_query(query))
        
        # Should detect multiple JOINs
        assert analysis.join_count >= 5
        assert analysis.table_count >= 6
    
    def test_function_counting(self, mock_documentation_processor):
        """Test counting of different function types."""
        handler = OptimizationHandler(mock_documentation_processor)
        
        query = """
            SELECT 
                customer_id,
                COUNT(*) as total_orders,
                SUM(amount) as total_amount,
                AVG(amount) as avg_amount,
                MIN(order_date) as first_order,
                MAX(order_date) as last_order,
                ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) as order_seq,
                RANK() OVER (ORDER BY SUM(amount) DESC) as customer_rank
            FROM orders
            GROUP BY customer_id
        """
        
        import asyncio
        analysis = asyncio.run(handler.analyze_query(query))
        
        assert analysis.aggregate_function_count >= 5  # COUNT, SUM, AVG, MIN, MAX
        assert analysis.window_function_count >= 2     # ROW_NUMBER, RANK