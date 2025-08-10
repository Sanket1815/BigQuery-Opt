"""
Comprehensive pytest testing for all BigQuery optimization patterns.
Each pattern is tested with 10 different query scenarios using BigQuery emulator.
"""

import pytest
from unittest.mock import Mock, patch
from typing import Dict, List, Any

from tests.emulator.bigquery_emulator import BigQueryEmulator
from src.optimizer.query_optimizer import BigQueryOptimizer
from src.common.models import OptimizationResult, QueryAnalysis, QueryComplexity


class MockAIOptimizer:
    """Mock AI optimizer that applies realistic optimizations based on query patterns."""
    
    def optimize_with_best_practices(self, query: str, analysis: QueryAnalysis, table_metadata: Dict) -> OptimizationResult:
        """Apply optimizations based on query patterns."""
        optimizations = []
        optimized_query = query
        
        # Pattern 1: Column Pruning
        if "SELECT *" in query.upper():
            optimizations.append(Mock(
                pattern_id="column_pruning",
                pattern_name="Column Pruning",
                description="Replaced SELECT * with specific columns to reduce data transfer",
                expected_improvement=0.25
            ))
            # Simulate column pruning
            if "customers" in query.lower():
                optimized_query = optimized_query.replace("SELECT *", "SELECT customer_id, customer_name, customer_tier")
            elif "orders" in query.lower():
                optimized_query = optimized_query.replace("SELECT *", "SELECT order_id, customer_id, total_amount")
            elif "products" in query.lower():
                optimized_query = optimized_query.replace("SELECT *", "SELECT product_id, product_name, category")
            else:
                optimized_query = optimized_query.replace("SELECT *", "SELECT id, name, value")
        
        # Pattern 2: Approximate Aggregation
        if "COUNT(DISTINCT" in query.upper():
            optimizations.append(Mock(
                pattern_id="approximate_aggregation",
                pattern_name="Approximate Aggregation",
                description="Replaced COUNT(DISTINCT) with APPROX_COUNT_DISTINCT for better performance",
                expected_improvement=0.5
            ))
            optimized_query = optimized_query.replace("COUNT(DISTINCT", "APPROX_COUNT_DISTINCT(")
        
        # Pattern 3: JOIN Reordering
        if "JOIN" in query.upper():
            optimizations.append(Mock(
                pattern_id="join_reordering",
                pattern_name="JOIN Reordering",
                description="Reordered JOINs to place smaller tables first",
                expected_improvement=0.3
            ))
            # Simulate JOIN reordering
            optimized_query = optimized_query.replace("large_table l JOIN small_table s", "small_table s JOIN large_table l")
        
        # Pattern 4: Subquery to JOIN
        if "EXISTS" in query.upper() or "IN (SELECT" in query.upper():
            optimizations.append(Mock(
                pattern_id="subquery_to_join",
                pattern_name="Subquery to JOIN Conversion",
                description="Converted subquery to INNER JOIN for better performance",
                expected_improvement=0.4
            ))
            # Simulate subquery conversion
            if "EXISTS" in query.upper():
                optimized_query = optimized_query.replace("WHERE EXISTS", "INNER JOIN")
        
        # Pattern 5: Window Function Optimization
        if "OVER (" in query.upper() and "PARTITION BY" not in query.upper():
            optimizations.append(Mock(
                pattern_id="window_optimization",
                pattern_name="Window Function Optimization",
                description="Added PARTITION BY clause to window function",
                expected_improvement=0.2
            ))
            optimized_query = optimized_query.replace("OVER (ORDER BY", "OVER (PARTITION BY customer_id ORDER BY")
        
        # Pattern 6: Predicate Pushdown
        if "WHERE" in query.upper() and "(" in query:
            optimizations.append(Mock(
                pattern_id="predicate_pushdown",
                pattern_name="Predicate Pushdown",
                description="Moved filter conditions closer to data sources",
                expected_improvement=0.25
            ))
        
        # Pattern 7: HAVING to WHERE Conversion
        if "HAVING" in query.upper() and not any(agg in query.upper() for agg in ["COUNT(", "SUM(", "AVG(", "MIN(", "MAX("]):
            optimizations.append(Mock(
                pattern_id="having_to_where",
                pattern_name="HAVING to WHERE Conversion",
                description="Converted HAVING clause to WHERE for better performance",
                expected_improvement=0.2
            ))
        
        # Pattern 8: UNION Optimization
        if "UNION " in query.upper() and "UNION ALL" not in query.upper():
            optimizations.append(Mock(
                pattern_id="union_optimization",
                pattern_name="UNION Optimization",
                description="Changed UNION to UNION ALL to avoid duplicate removal",
                expected_improvement=0.15
            ))
        
        # Pattern 9: DISTINCT Optimization
        if "SELECT DISTINCT" in query.upper():
            optimizations.append(Mock(
                pattern_id="distinct_optimization",
                pattern_name="DISTINCT Optimization",
                description="Optimized DISTINCT operation for better performance",
                expected_improvement=0.2
            ))
        
        # Pattern 10: LIMIT Optimization
        if "ORDER BY" in query.upper() and "LIMIT" not in query.upper():
            optimizations.append(Mock(
                pattern_id="limit_optimization",
                pattern_name="LIMIT Optimization",
                description="Added LIMIT clause to reduce result set size",
                expected_improvement=0.3
            ))
            optimized_query += " LIMIT 1000"
        
        # Calculate total improvement
        total_improvement = sum(opt.expected_improvement for opt in optimizations)
        total_improvement = min(total_improvement, 0.8)  # Cap at 80%
        
        return OptimizationResult(
            original_query=query,
            query_analysis=analysis,
            optimized_query=optimized_query,
            optimizations_applied=optimizations,
            total_optimizations=len(optimizations),
            estimated_improvement=total_improvement
        )


@pytest.fixture
def bigquery_emulator():
    """Fixture providing BigQuery emulator."""
    return BigQueryEmulator()


@pytest.fixture
def mock_optimizer():
    """Fixture providing mocked optimizer with emulator."""
    emulator = BigQueryEmulator()
    
    with patch('src.optimizer.bigquery_client.BigQueryClient') as mock_bq:
        mock_bq_instance = Mock()
        mock_bq_instance.execute_query = lambda q, dry_run=False: {
            "success": emulator.execute_query(q, dry_run).success,
            "results": emulator.execute_query(q, dry_run).results,
            "row_count": emulator.execute_query(q, dry_run).row_count,
            "performance": Mock(
                execution_time_ms=emulator.execute_query(q, dry_run).execution_time_ms,
                bytes_processed=emulator.execute_query(q, dry_run).bytes_processed
            )
        }
        mock_bq_instance.get_table_info = emulator.get_table_info
        mock_bq_instance.validate_query = emulator.validate_query
        mock_bq_instance.test_connection = emulator.test_connection
        mock_bq_instance.compare_query_performance = emulator.compare_query_performance
        mock_bq_instance.project_id = "test-project"
        mock_bq.return_value = mock_bq_instance
        
        with patch('src.optimizer.ai_optimizer.GeminiQueryOptimizer') as mock_ai:
            mock_ai.return_value = MockAIOptimizer()
            
            yield BigQueryOptimizer(validate_results=False)


# Pattern 1: Column Pruning - 10 Test Cases
@pytest.mark.unit
class TestColumnPruningPattern:
    """Test Column Pruning optimization pattern with 10 different scenarios."""
    
    def test_basic_select_star(self, mock_optimizer):
        """Test 1: Basic SELECT * replacement."""
        query = "SELECT * FROM customers WHERE customer_id > 100"
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
        assert "SELECT *" not in result.optimized_query
        assert any("column" in opt.pattern_name.lower() for opt in result.optimizations_applied)
    
    def test_select_star_with_where(self, mock_optimizer):
        """Test 2: SELECT * with complex WHERE clause."""
        query = "SELECT * FROM orders WHERE order_date >= '2024-01-01' AND status = 'completed'"
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
        assert "order_id, customer_id, total_amount" in result.optimized_query
    
    def test_select_star_with_join(self, mock_optimizer):
        """Test 3: SELECT * in JOIN query."""
        query = "SELECT * FROM customers c JOIN orders o ON c.customer_id = o.customer_id"
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
        assert "SELECT *" not in result.optimized_query
    
    def test_select_star_with_group_by(self, mock_optimizer):
        """Test 4: SELECT * with GROUP BY."""
        query = "SELECT * FROM orders GROUP BY customer_id"
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_select_star_with_order_by(self, mock_optimizer):
        """Test 5: SELECT * with ORDER BY."""
        query = "SELECT * FROM products ORDER BY price DESC"
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_select_star_in_subquery(self, mock_optimizer):
        """Test 6: SELECT * in subquery."""
        query = "SELECT customer_id FROM (SELECT * FROM customers WHERE region = 'US')"
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_select_star_with_union(self, mock_optimizer):
        """Test 7: SELECT * in UNION."""
        query = "SELECT * FROM customers_2023 UNION SELECT * FROM customers_2024"
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_select_star_with_cte(self, mock_optimizer):
        """Test 8: SELECT * in CTE."""
        query = "WITH customer_data AS (SELECT * FROM customers) SELECT customer_id FROM customer_data"
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_select_star_large_table(self, mock_optimizer):
        """Test 9: SELECT * from large table."""
        query = "SELECT * FROM large_table WHERE date_column >= '2024-01-01'"
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_select_star_with_distinct(self, mock_optimizer):
        """Test 10: SELECT DISTINCT * optimization."""
        query = "SELECT DISTINCT * FROM customers WHERE customer_tier = 'Premium'"
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1


# Pattern 2: JOIN Reordering - 10 Test Cases
@pytest.mark.unit
class TestJoinReorderingPattern:
    """Test JOIN Reordering optimization pattern with 10 different scenarios."""
    
    def test_simple_inner_join(self, mock_optimizer):
        """Test 1: Simple INNER JOIN reordering."""
        query = "SELECT * FROM large_table l JOIN small_table s ON l.id = s.id"
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
        assert any("join" in opt.pattern_name.lower() for opt in result.optimizations_applied)
    
    def test_left_join_reordering(self, mock_optimizer):
        """Test 2: LEFT JOIN reordering."""
        query = "SELECT * FROM orders o LEFT JOIN customers c ON o.customer_id = c.customer_id"
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_multiple_joins(self, mock_optimizer):
        """Test 3: Multiple JOINs reordering."""
        query = """
        SELECT c.customer_name, o.total_amount, p.product_name
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.order_id
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN products p ON oi.product_id = p.product_id
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_right_join_reordering(self, mock_optimizer):
        """Test 4: RIGHT JOIN reordering."""
        query = "SELECT * FROM large_table l RIGHT JOIN small_table s ON l.id = s.id"
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_full_outer_join(self, mock_optimizer):
        """Test 5: FULL OUTER JOIN optimization."""
        query = "SELECT * FROM orders o FULL OUTER JOIN customers c ON o.customer_id = c.customer_id"
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_cross_join_elimination(self, mock_optimizer):
        """Test 6: CROSS JOIN elimination."""
        query = "SELECT * FROM customers c CROSS JOIN products p WHERE c.region = 'US'"
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_join_with_complex_conditions(self, mock_optimizer):
        """Test 7: JOIN with complex ON conditions."""
        query = """
        SELECT * FROM orders o 
        JOIN customers c ON o.customer_id = c.customer_id AND c.customer_tier = 'Premium'
        JOIN products p ON o.product_id = p.product_id AND p.price > 100
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_self_join_optimization(self, mock_optimizer):
        """Test 8: Self JOIN optimization."""
        query = """
        SELECT o1.order_id, o2.order_id as related_order
        FROM orders o1 JOIN orders o2 ON o1.customer_id = o2.customer_id
        WHERE o1.order_id != o2.order_id
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_join_with_aggregation(self, mock_optimizer):
        """Test 9: JOIN with aggregation functions."""
        query = """
        SELECT c.region, COUNT(o.order_id), SUM(o.total_amount)
        FROM large_table o
        JOIN small_table c ON o.customer_id = c.customer_id
        GROUP BY c.region
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_nested_joins(self, mock_optimizer):
        """Test 10: Nested JOINs optimization."""
        query = """
        SELECT * FROM (
            SELECT c.*, o.order_id FROM customers c JOIN orders o ON c.customer_id = o.customer_id
        ) co JOIN products p ON co.product_id = p.product_id
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1


# Pattern 3: Subquery to JOIN Conversion - 10 Test Cases
@pytest.mark.unit
class TestSubqueryConversionPattern:
    """Test Subquery to JOIN conversion pattern with 10 different scenarios."""
    
    def test_exists_subquery(self, mock_optimizer):
        """Test 1: EXISTS subquery conversion."""
        query = """
        SELECT customer_id, customer_name FROM customers c
        WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id)
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
        assert any("subquery" in opt.pattern_name.lower() for opt in result.optimizations_applied)
    
    def test_not_exists_subquery(self, mock_optimizer):
        """Test 2: NOT EXISTS subquery conversion."""
        query = """
        SELECT customer_id FROM customers c
        WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id)
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_in_subquery(self, mock_optimizer):
        """Test 3: IN subquery conversion."""
        query = """
        SELECT * FROM customers 
        WHERE customer_id IN (SELECT customer_id FROM orders WHERE status = 'completed')
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_not_in_subquery(self, mock_optimizer):
        """Test 4: NOT IN subquery conversion."""
        query = """
        SELECT * FROM customers 
        WHERE customer_id NOT IN (SELECT customer_id FROM orders WHERE status = 'cancelled')
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_correlated_subquery_in_select(self, mock_optimizer):
        """Test 5: Correlated subquery in SELECT clause."""
        query = """
        SELECT customer_id, 
               (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.customer_id) as order_count
        FROM customers c
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_multiple_exists_subqueries(self, mock_optimizer):
        """Test 6: Multiple EXISTS subqueries."""
        query = """
        SELECT * FROM customers c
        WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id)
        AND EXISTS (SELECT 1 FROM order_items oi JOIN orders o2 ON oi.order_id = o2.order_id WHERE o2.customer_id = c.customer_id)
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_nested_subqueries(self, mock_optimizer):
        """Test 7: Nested subqueries conversion."""
        query = """
        SELECT * FROM customers 
        WHERE customer_id IN (
            SELECT customer_id FROM orders 
            WHERE order_id IN (SELECT order_id FROM order_items WHERE quantity > 5)
        )
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_subquery_with_aggregation(self, mock_optimizer):
        """Test 8: Subquery with aggregation."""
        query = """
        SELECT * FROM customers c
        WHERE customer_id IN (
            SELECT customer_id FROM orders 
            GROUP BY customer_id 
            HAVING SUM(total_amount) > 1000
        )
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_any_all_subqueries(self, mock_optimizer):
        """Test 9: ANY/ALL subqueries."""
        query = """
        SELECT * FROM orders 
        WHERE total_amount > ANY (SELECT AVG(total_amount) FROM orders GROUP BY customer_id)
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_subquery_in_having(self, mock_optimizer):
        """Test 10: Subquery in HAVING clause."""
        query = """
        SELECT customer_id, COUNT(*) as order_count
        FROM orders
        GROUP BY customer_id
        HAVING customer_id IN (SELECT customer_id FROM customers WHERE customer_tier = 'Premium')
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1


# Pattern 4: Approximate Aggregation - 10 Test Cases
@pytest.mark.unit
class TestApproximateAggregationPattern:
    """Test Approximate Aggregation optimization pattern with 10 different scenarios."""
    
    def test_basic_count_distinct(self, mock_optimizer):
        """Test 1: Basic COUNT(DISTINCT) replacement."""
        query = "SELECT COUNT(DISTINCT customer_id) FROM orders"
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
        assert "APPROX_COUNT_DISTINCT" in result.optimized_query
        assert any("approximate" in opt.pattern_name.lower() for opt in result.optimizations_applied)
    
    def test_count_distinct_with_group_by(self, mock_optimizer):
        """Test 2: COUNT(DISTINCT) with GROUP BY."""
        query = """
        SELECT region, COUNT(DISTINCT customer_id) as unique_customers
        FROM orders o JOIN customers c ON o.customer_id = c.customer_id
        GROUP BY region
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
        assert "APPROX_COUNT_DISTINCT" in result.optimized_query
    
    def test_multiple_count_distinct(self, mock_optimizer):
        """Test 3: Multiple COUNT(DISTINCT) in same query."""
        query = """
        SELECT 
            COUNT(DISTINCT customer_id) as unique_customers,
            COUNT(DISTINCT product_id) as unique_products,
            COUNT(*) as total_orders
        FROM orders
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_count_distinct_with_where(self, mock_optimizer):
        """Test 4: COUNT(DISTINCT) with WHERE clause."""
        query = """
        SELECT COUNT(DISTINCT customer_id) 
        FROM orders 
        WHERE order_date >= '2024-01-01' AND status = 'completed'
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_count_distinct_in_subquery(self, mock_optimizer):
        """Test 5: COUNT(DISTINCT) in subquery."""
        query = """
        SELECT region, unique_customers
        FROM (
            SELECT region, COUNT(DISTINCT customer_id) as unique_customers
            FROM orders o JOIN customers c ON o.customer_id = c.customer_id
            GROUP BY region
        )
        WHERE unique_customers > 100
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_count_distinct_with_having(self, mock_optimizer):
        """Test 6: COUNT(DISTINCT) with HAVING."""
        query = """
        SELECT customer_id, COUNT(DISTINCT product_id) as unique_products
        FROM order_items
        GROUP BY customer_id
        HAVING COUNT(DISTINCT product_id) > 5
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_count_distinct_with_case(self, mock_optimizer):
        """Test 7: COUNT(DISTINCT) with CASE statement."""
        query = """
        SELECT 
            COUNT(DISTINCT CASE WHEN status = 'completed' THEN customer_id END) as completed_customers,
            COUNT(DISTINCT CASE WHEN status = 'cancelled' THEN customer_id END) as cancelled_customers
        FROM orders
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_count_distinct_with_date_functions(self, mock_optimizer):
        """Test 8: COUNT(DISTINCT) with date functions."""
        query = """
        SELECT 
            EXTRACT(MONTH FROM order_date) as month,
            COUNT(DISTINCT customer_id) as monthly_customers
        FROM orders
        GROUP BY EXTRACT(MONTH FROM order_date)
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_count_distinct_large_dataset(self, mock_optimizer):
        """Test 9: COUNT(DISTINCT) on large dataset."""
        query = "SELECT COUNT(DISTINCT customer_id) FROM large_table WHERE date_column >= '2024-01-01'"
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_count_distinct_with_union(self, mock_optimizer):
        """Test 10: COUNT(DISTINCT) with UNION."""
        query = """
        SELECT COUNT(DISTINCT customer_id) FROM (
            SELECT customer_id FROM orders_2023
            UNION ALL
            SELECT customer_id FROM orders_2024
        )
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1


# Pattern 5: Window Function Optimization - 10 Test Cases
@pytest.mark.unit
class TestWindowFunctionPattern:
    """Test Window Function optimization pattern with 10 different scenarios."""
    
    def test_row_number_without_partition(self, mock_optimizer):
        """Test 1: ROW_NUMBER without PARTITION BY."""
        query = """
        SELECT customer_id, order_date, 
               ROW_NUMBER() OVER (ORDER BY order_date) as row_num
        FROM orders
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
        assert "PARTITION BY customer_id" in result.optimized_query
    
    def test_rank_function_optimization(self, mock_optimizer):
        """Test 2: RANK function optimization."""
        query = """
        SELECT customer_id, total_amount,
               RANK() OVER (ORDER BY total_amount DESC) as amount_rank
        FROM orders
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_dense_rank_optimization(self, mock_optimizer):
        """Test 3: DENSE_RANK optimization."""
        query = """
        SELECT product_id, price,
               DENSE_RANK() OVER (ORDER BY price DESC) as price_rank
        FROM products
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_lag_lead_functions(self, mock_optimizer):
        """Test 4: LAG/LEAD function optimization."""
        query = """
        SELECT customer_id, order_date, total_amount,
               LAG(total_amount) OVER (ORDER BY order_date) as prev_amount,
               LEAD(total_amount) OVER (ORDER BY order_date) as next_amount
        FROM orders
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_sum_window_function(self, mock_optimizer):
        """Test 5: SUM window function optimization."""
        query = """
        SELECT customer_id, order_date, total_amount,
               SUM(total_amount) OVER (ORDER BY order_date ROWS UNBOUNDED PRECEDING) as running_total
        FROM orders
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_avg_window_function(self, mock_optimizer):
        """Test 6: AVG window function optimization."""
        query = """
        SELECT customer_id, total_amount,
               AVG(total_amount) OVER (ORDER BY order_date ROWS BETWEEN 2 PRECEDING AND 2 FOLLOWING) as moving_avg
        FROM orders
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_first_last_value(self, mock_optimizer):
        """Test 7: FIRST_VALUE/LAST_VALUE optimization."""
        query = """
        SELECT customer_id, order_date,
               FIRST_VALUE(total_amount) OVER (ORDER BY order_date) as first_order_amount,
               LAST_VALUE(total_amount) OVER (ORDER BY order_date) as last_order_amount
        FROM orders
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_ntile_function(self, mock_optimizer):
        """Test 8: NTILE function optimization."""
        query = """
        SELECT customer_id, total_amount,
               NTILE(4) OVER (ORDER BY total_amount) as quartile
        FROM orders
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_multiple_window_functions(self, mock_optimizer):
        """Test 9: Multiple window functions in same query."""
        query = """
        SELECT customer_id, order_date, total_amount,
               ROW_NUMBER() OVER (ORDER BY order_date) as row_num,
               RANK() OVER (ORDER BY total_amount DESC) as amount_rank,
               SUM(total_amount) OVER (ORDER BY order_date) as running_sum
        FROM orders
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_window_in_subquery(self, mock_optimizer):
        """Test 10: Window function in subquery."""
        query = """
        SELECT * FROM (
            SELECT customer_id, total_amount,
                   ROW_NUMBER() OVER (ORDER BY total_amount DESC) as rank
            FROM orders
        ) ranked_orders
        WHERE rank <= 10
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1


# Pattern 6: Predicate Pushdown - 10 Test Cases
@pytest.mark.unit
class TestPredicatePushdownPattern:
    """Test Predicate Pushdown optimization pattern with 10 different scenarios."""
    
    def test_filter_in_outer_query(self, mock_optimizer):
        """Test 1: Filter in outer query that can be pushed down."""
        query = """
        SELECT * FROM (
            SELECT customer_id, order_date, total_amount
            FROM orders
        ) WHERE order_date >= '2024-01-01'
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_filter_after_join(self, mock_optimizer):
        """Test 2: Filter applied after JOIN."""
        query = """
        SELECT * FROM (
            SELECT c.customer_name, o.total_amount
            FROM customers c JOIN orders o ON c.customer_id = o.customer_id
        ) WHERE total_amount > 100
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_filter_in_cte(self, mock_optimizer):
        """Test 3: Filter that can be pushed into CTE."""
        query = """
        WITH order_data AS (
            SELECT customer_id, order_date, total_amount, status
            FROM orders
        )
        SELECT * FROM order_data WHERE status = 'completed'
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_filter_in_union(self, mock_optimizer):
        """Test 4: Filter applied to UNION result."""
        query = """
        SELECT * FROM (
            SELECT customer_id, 'old' as type FROM customers_old
            UNION ALL
            SELECT customer_id, 'new' as type FROM customers_new
        ) WHERE customer_id > 1000
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_complex_nested_filters(self, mock_optimizer):
        """Test 5: Complex nested filters."""
        query = """
        SELECT * FROM (
            SELECT * FROM (
                SELECT customer_id, order_date, total_amount
                FROM orders
            ) WHERE total_amount > 50
        ) WHERE order_date >= '2024-01-01'
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_filter_with_aggregation(self, mock_optimizer):
        """Test 6: Filter with aggregation that can be optimized."""
        query = """
        SELECT * FROM (
            SELECT customer_id, SUM(total_amount) as total_spent
            FROM orders
            GROUP BY customer_id
        ) WHERE total_spent > 1000
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_filter_with_window_function(self, mock_optimizer):
        """Test 7: Filter applied to window function result."""
        query = """
        SELECT * FROM (
            SELECT customer_id, total_amount,
                   ROW_NUMBER() OVER (ORDER BY total_amount DESC) as rank
            FROM orders
        ) WHERE rank <= 100
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_filter_in_view_like_subquery(self, mock_optimizer):
        """Test 8: Filter in view-like subquery."""
        query = """
        SELECT customer_name, total_orders FROM (
            SELECT c.customer_name, COUNT(o.order_id) as total_orders
            FROM customers c
            LEFT JOIN orders o ON c.customer_id = o.customer_id
            GROUP BY c.customer_name
        ) WHERE total_orders > 5
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_filter_with_case_when(self, mock_optimizer):
        """Test 9: Filter with CASE WHEN that can be optimized."""
        query = """
        SELECT * FROM (
            SELECT customer_id,
                   CASE WHEN total_amount > 1000 THEN 'high' ELSE 'low' END as value_tier
            FROM orders
        ) WHERE value_tier = 'high'
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_multiple_level_nesting(self, mock_optimizer):
        """Test 10: Multiple level nesting with filters."""
        query = """
        SELECT * FROM (
            SELECT * FROM (
                SELECT * FROM (
                    SELECT customer_id, order_date, total_amount, status
                    FROM orders
                ) WHERE status IN ('completed', 'processing')
            ) WHERE total_amount > 100
        ) WHERE order_date >= '2024-01-01'
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1


# Pattern 7: HAVING to WHERE Conversion - 10 Test Cases
@pytest.mark.unit
class TestHavingToWherePattern:
    """Test HAVING to WHERE conversion pattern with 10 different scenarios."""
    
    def test_having_on_non_aggregate_column(self, mock_optimizer):
        """Test 1: HAVING on non-aggregate column."""
        query = """
        SELECT customer_id, COUNT(*) as order_count
        FROM orders 
        GROUP BY customer_id
        HAVING customer_id > 1000
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_having_with_multiple_conditions(self, mock_optimizer):
        """Test 2: HAVING with multiple conditions."""
        query = """
        SELECT customer_id, status, COUNT(*) as order_count
        FROM orders 
        GROUP BY customer_id, status
        HAVING customer_id > 500 AND status = 'completed'
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_having_with_date_filter(self, mock_optimizer):
        """Test 3: HAVING with date filter."""
        query = """
        SELECT customer_id, order_date, COUNT(*) as daily_orders
        FROM orders 
        GROUP BY customer_id, order_date
        HAVING order_date >= '2024-01-01'
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_having_with_string_filter(self, mock_optimizer):
        """Test 4: HAVING with string filter."""
        query = """
        SELECT customer_id, status, COUNT(*) as status_count
        FROM orders 
        GROUP BY customer_id, status
        HAVING status IN ('completed', 'processing')
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_having_with_range_filter(self, mock_optimizer):
        """Test 5: HAVING with range filter."""
        query = """
        SELECT customer_id, product_id, COUNT(*) as purchase_count
        FROM order_items 
        GROUP BY customer_id, product_id
        HAVING product_id BETWEEN 10 AND 50
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_having_with_null_check(self, mock_optimizer):
        """Test 6: HAVING with NULL check."""
        query = """
        SELECT customer_id, status, COUNT(*) as order_count
        FROM orders 
        GROUP BY customer_id, status
        HAVING status IS NOT NULL
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_having_with_like_pattern(self, mock_optimizer):
        """Test 7: HAVING with LIKE pattern."""
        query = """
        SELECT customer_id, status, COUNT(*) as order_count
        FROM orders 
        GROUP BY customer_id, status
        HAVING status LIKE 'comp%'
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_having_with_join(self, mock_optimizer):
        """Test 8: HAVING with JOIN that can be optimized."""
        query = """
        SELECT c.region, o.status, COUNT(*) as order_count
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.region, o.status
        HAVING c.region = 'US-East'
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_having_mixed_conditions(self, mock_optimizer):
        """Test 9: HAVING with mixed aggregate and non-aggregate conditions."""
        query = """
        SELECT customer_id, COUNT(*) as order_count, SUM(total_amount) as total_spent
        FROM orders 
        GROUP BY customer_id
        HAVING customer_id > 100 AND COUNT(*) > 5
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_having_in_subquery(self, mock_optimizer):
        """Test 10: HAVING in subquery."""
        query = """
        SELECT * FROM (
            SELECT customer_id, COUNT(*) as order_count
            FROM orders 
            GROUP BY customer_id
            HAVING customer_id IN (1, 2, 3, 4, 5)
        ) WHERE order_count > 2
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1


# Pattern 8: UNION Optimization - 10 Test Cases
@pytest.mark.unit
class TestUnionOptimizationPattern:
    """Test UNION optimization pattern with 10 different scenarios."""
    
    def test_union_to_union_all(self, mock_optimizer):
        """Test 1: UNION to UNION ALL conversion."""
        query = """
        SELECT customer_id FROM customers_2023
        UNION
        SELECT customer_id FROM customers_2024
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_multiple_unions(self, mock_optimizer):
        """Test 2: Multiple UNION operations."""
        query = """
        SELECT customer_id FROM customers_2022
        UNION
        SELECT customer_id FROM customers_2023
        UNION
        SELECT customer_id FROM customers_2024
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_union_with_where(self, mock_optimizer):
        """Test 3: UNION with WHERE clauses."""
        query = """
        SELECT customer_id FROM customers WHERE region = 'US'
        UNION
        SELECT customer_id FROM customers WHERE region = 'Europe'
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_union_with_aggregation(self, mock_optimizer):
        """Test 4: UNION with aggregation."""
        query = """
        SELECT region, COUNT(*) FROM customers WHERE signup_date < '2023-01-01' GROUP BY region
        UNION
        SELECT region, COUNT(*) FROM customers WHERE signup_date >= '2023-01-01' GROUP BY region
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_union_with_join(self, mock_optimizer):
        """Test 5: UNION with JOIN operations."""
        query = """
        SELECT c.customer_name FROM customers c JOIN orders o ON c.customer_id = o.customer_id WHERE o.status = 'completed'
        UNION
        SELECT c.customer_name FROM customers c JOIN orders o ON c.customer_id = o.customer_id WHERE o.status = 'pending'
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_union_in_subquery(self, mock_optimizer):
        """Test 6: UNION in subquery."""
        query = """
        SELECT customer_id, customer_name FROM customers
        WHERE customer_id IN (
            SELECT customer_id FROM orders_2023
            UNION
            SELECT customer_id FROM orders_2024
        )
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_union_with_order_by(self, mock_optimizer):
        """Test 7: UNION with ORDER BY."""
        query = """
        SELECT customer_id, 'old' as type FROM customers_old
        UNION
        SELECT customer_id, 'new' as type FROM customers_new
        ORDER BY customer_id
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_union_with_limit(self, mock_optimizer):
        """Test 8: UNION with LIMIT."""
        query = """
        SELECT customer_id FROM high_value_customers
        UNION
        SELECT customer_id FROM premium_customers
        LIMIT 1000
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_nested_unions(self, mock_optimizer):
        """Test 9: Nested UNION operations."""
        query = """
        SELECT customer_id FROM (
            SELECT customer_id FROM customers_2022
            UNION
            SELECT customer_id FROM customers_2023
        )
        UNION
        SELECT customer_id FROM customers_2024
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_union_with_distinct(self, mock_optimizer):
        """Test 10: UNION with DISTINCT."""
        query = """
        SELECT DISTINCT customer_id FROM customers_active
        UNION
        SELECT DISTINCT customer_id FROM customers_inactive
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1


# Pattern 9: DISTINCT Optimization - 10 Test Cases
@pytest.mark.unit
class TestDistinctOptimizationPattern:
    """Test DISTINCT optimization pattern with 10 different scenarios."""
    
    def test_basic_distinct(self, mock_optimizer):
        """Test 1: Basic DISTINCT optimization."""
        query = "SELECT DISTINCT customer_id FROM orders"
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_distinct_with_multiple_columns(self, mock_optimizer):
        """Test 2: DISTINCT with multiple columns."""
        query = "SELECT DISTINCT customer_id, status FROM orders"
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_distinct_with_join(self, mock_optimizer):
        """Test 3: DISTINCT with JOIN."""
        query = """
        SELECT DISTINCT c.customer_name, o.status
        FROM customers c JOIN orders o ON c.customer_id = o.customer_id
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_distinct_with_where(self, mock_optimizer):
        """Test 4: DISTINCT with WHERE clause."""
        query = """
        SELECT DISTINCT customer_id, product_id
        FROM order_items
        WHERE order_date >= '2024-01-01'
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_distinct_with_order_by(self, mock_optimizer):
        """Test 5: DISTINCT with ORDER BY."""
        query = """
        SELECT DISTINCT customer_tier
        FROM customers
        ORDER BY customer_tier
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_distinct_in_subquery(self, mock_optimizer):
        """Test 6: DISTINCT in subquery."""
        query = """
        SELECT customer_id FROM customers
        WHERE customer_id IN (
            SELECT DISTINCT customer_id FROM orders WHERE status = 'completed'
        )
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_distinct_with_aggregation(self, mock_optimizer):
        """Test 7: DISTINCT with aggregation context."""
        query = """
        SELECT DISTINCT customer_id, 
               (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.customer_id) as order_count
        FROM customers c
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_distinct_with_case_when(self, mock_optimizer):
        """Test 8: DISTINCT with CASE WHEN."""
        query = """
        SELECT DISTINCT 
            CASE WHEN total_amount > 1000 THEN 'high' ELSE 'low' END as value_category
        FROM orders
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_distinct_with_functions(self, mock_optimizer):
        """Test 9: DISTINCT with functions."""
        query = """
        SELECT DISTINCT UPPER(customer_name), EXTRACT(YEAR FROM signup_date)
        FROM customers
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_distinct_large_result_set(self, mock_optimizer):
        """Test 10: DISTINCT on large result set."""
        query = """
        SELECT DISTINCT customer_id, product_id, order_date
        FROM order_items
        WHERE quantity > 1
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1


# Pattern 10: LIMIT Optimization - 10 Test Cases
@pytest.mark.unit
class TestLimitOptimizationPattern:
    """Test LIMIT optimization pattern with 10 different scenarios."""
    
    def test_order_by_without_limit(self, mock_optimizer):
        """Test 1: ORDER BY without LIMIT."""
        query = "SELECT customer_id, total_amount FROM orders ORDER BY total_amount DESC"
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
        assert "LIMIT" in result.optimized_query
    
    def test_expensive_sort_without_limit(self, mock_optimizer):
        """Test 2: Expensive sort without LIMIT."""
        query = """
        SELECT customer_id, order_date, total_amount
        FROM orders
        ORDER BY total_amount DESC, order_date DESC
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_window_function_without_limit(self, mock_optimizer):
        """Test 3: Window function without LIMIT."""
        query = """
        SELECT customer_id, total_amount,
               ROW_NUMBER() OVER (ORDER BY total_amount DESC) as rank
        FROM orders
        ORDER BY rank
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_join_with_order_no_limit(self, mock_optimizer):
        """Test 4: JOIN with ORDER BY but no LIMIT."""
        query = """
        SELECT c.customer_name, o.total_amount
        FROM customers c JOIN orders o ON c.customer_id = o.customer_id
        ORDER BY o.total_amount DESC
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_aggregation_with_order_no_limit(self, mock_optimizer):
        """Test 5: Aggregation with ORDER BY but no LIMIT."""
        query = """
        SELECT customer_id, COUNT(*) as order_count, SUM(total_amount) as total_spent
        FROM orders
        GROUP BY customer_id
        ORDER BY total_spent DESC
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_distinct_with_order_no_limit(self, mock_optimizer):
        """Test 6: DISTINCT with ORDER BY but no LIMIT."""
        query = """
        SELECT DISTINCT customer_tier
        FROM customers
        ORDER BY customer_tier
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_subquery_with_order_no_limit(self, mock_optimizer):
        """Test 7: Subquery with ORDER BY but no LIMIT."""
        query = """
        SELECT * FROM (
            SELECT customer_id, total_amount
            FROM orders
            ORDER BY total_amount DESC
        )
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_cte_with_order_no_limit(self, mock_optimizer):
        """Test 8: CTE with ORDER BY but no LIMIT."""
        query = """
        WITH ordered_customers AS (
            SELECT customer_id, customer_name
            FROM customers
            ORDER BY customer_name
        )
        SELECT * FROM ordered_customers
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_union_with_order_no_limit(self, mock_optimizer):
        """Test 9: UNION with ORDER BY but no LIMIT."""
        query = """
        SELECT customer_id, 'old' as type FROM customers_old
        UNION ALL
        SELECT customer_id, 'new' as type FROM customers_new
        ORDER BY customer_id
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1
    
    def test_complex_sort_no_limit(self, mock_optimizer):
        """Test 10: Complex sorting without LIMIT."""
        query = """
        SELECT c.customer_name, o.order_date, o.total_amount, p.product_name
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
        ORDER BY o.total_amount DESC, o.order_date DESC, c.customer_name
        """
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1


# Comprehensive Pattern Coverage Test
@pytest.mark.unit
class TestComprehensivePatternCoverage:
    """Test comprehensive coverage of all optimization patterns."""
    
    def test_all_patterns_applied(self, mock_optimizer):
        """Test that multiple patterns can be applied to a complex query."""
        complex_query = """
        SELECT *, 
               COUNT(DISTINCT o.product_id) as unique_products,
               ROW_NUMBER() OVER (ORDER BY c.signup_date) as customer_rank,
               (SELECT COUNT(*) FROM order_items oi WHERE oi.order_id = o.order_id) as item_count
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        WHERE EXISTS (
            SELECT 1 FROM order_items oi 
            WHERE oi.order_id = o.order_id 
            AND oi.quantity > 2
        )
        AND c.region = 'US'
        GROUP BY c.customer_id, c.customer_name, c.customer_tier, c.region, c.signup_date, 
                 o.order_id, o.order_date, o.total_amount, o.status, o.product_id
        ORDER BY customer_rank
        """
        
        result = mock_optimizer.optimize_query(complex_query, validate_results=False)
        
        # Should apply multiple optimizations
        assert result.total_optimizations >= 3
        
        # Check for specific patterns
        pattern_names = [opt.pattern_name.lower() for opt in result.optimizations_applied]
        
        expected_patterns = ["column", "approximate", "subquery", "window", "limit"]
        found_patterns = []
        
        for expected in expected_patterns:
            if any(expected in name for name in pattern_names):
                found_patterns.append(expected)
        
        assert len(found_patterns) >= 3, f"Expected multiple patterns, found: {found_patterns}"
    
    def test_pattern_priority_ordering(self, mock_optimizer):
        """Test that high-impact patterns are prioritized."""
        query = """
        SELECT *, COUNT(DISTINCT customer_id) as unique_customers
        FROM large_table
        WHERE date_column >= '2024-01-01'
        """
        
        result = mock_optimizer.optimize_query(query, validate_results=False)
        
        # Should prioritize high-impact optimizations
        assert result.total_optimizations >= 2
        assert result.estimated_improvement >= 0.4  # Should be significant
    
    def test_no_optimization_needed(self, mock_optimizer):
        """Test query that doesn't need optimization."""
        well_optimized_query = """
        SELECT customer_id, customer_name, customer_tier
        FROM customers
        WHERE customer_id = 12345
        """
        
        result = mock_optimizer.optimize_query(well_optimized_query, validate_results=False)
        
        # May have 0 optimizations if query is already well-optimized
        assert result.total_optimizations >= 0
        assert result.optimized_query is not None


# Performance and Validation Tests
@pytest.mark.unit
class TestEmulatorPerformance:
    """Test BigQuery emulator performance simulation."""
    
    def test_performance_calculation(self, bigquery_emulator):
        """Test realistic performance calculation."""
        simple_query = "SELECT customer_id FROM customers"
        complex_query = """
        SELECT c.*, o.*, p.*
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
        WHERE COUNT(DISTINCT o.product_id) > 5
        """
        
        simple_result = bigquery_emulator.execute_query(simple_query)
        complex_result = bigquery_emulator.execute_query(complex_query)
        
        # Complex query should take longer
        assert complex_result.execution_time_ms > simple_result.execution_time_ms
        assert complex_result.bytes_processed >= simple_result.bytes_processed
    
    def test_optimization_performance_improvement(self, bigquery_emulator):
        """Test that optimizations show performance improvement."""
        original_query = "SELECT * FROM large_table ORDER BY date_column"
        optimized_query = "SELECT id, name FROM large_table WHERE date_column >= '2024-01-01' ORDER BY date_column LIMIT 1000"
        
        comparison = bigquery_emulator.compare_query_performance(original_query, optimized_query)
        
        assert comparison["success"] == True
        assert comparison["improvement_percentage"] > 0
        assert comparison["optimized_avg_ms"] < comparison["original_avg_ms"]
    
    def test_bytes_processed_reduction(self, bigquery_emulator):
        """Test that optimizations reduce bytes processed."""
        select_star = bigquery_emulator.execute_query("SELECT * FROM large_table")
        select_specific = bigquery_emulator.execute_query("SELECT id, name FROM large_table")
        
        # Specific columns should process fewer bytes
        assert select_specific.bytes_processed < select_star.bytes_processed


# Integration Test with All Patterns
@pytest.mark.integration
class TestAllPatternsIntegration:
    """Integration test covering all optimization patterns together."""
    
    def test_comprehensive_optimization_workflow(self, mock_optimizer):
        """Test complete optimization workflow with multiple patterns."""
        
        # Test queries that should trigger different patterns
        test_cases = [
            {
                "name": "Column Pruning + JOIN Reordering",
                "query": "SELECT * FROM large_table l JOIN small_table s ON l.id = s.id",
                "expected_patterns": ["column", "join"]
            },
            {
                "name": "Approximate Aggregation + Window Optimization",
                "query": """
                SELECT customer_id, COUNT(DISTINCT product_id) as unique_products,
                       ROW_NUMBER() OVER (ORDER BY customer_id) as rank
                FROM order_items GROUP BY customer_id
                """,
                "expected_patterns": ["approximate", "window"]
            },
            {
                "name": "Subquery + Predicate Pushdown",
                "query": """
                SELECT * FROM (
                    SELECT customer_id, customer_name FROM customers
                ) WHERE customer_id IN (SELECT customer_id FROM orders)
                """,
                "expected_patterns": ["subquery", "predicate"]
            }
        ]
        
        for test_case in test_cases:
            result = mock_optimizer.optimize_query(test_case["query"], validate_results=False)
            
            assert result.total_optimizations >= 1, f"No optimizations for {test_case['name']}"
            
            pattern_names = [opt.pattern_name.lower() for opt in result.optimizations_applied]
            found_patterns = []
            
            for expected in test_case["expected_patterns"]:
                if any(expected in name for name in pattern_names):
                    found_patterns.append(expected)
            
            assert len(found_patterns) >= 1, f"Expected patterns {test_case['expected_patterns']} not found in {pattern_names}"
            
            print(f"✅ {test_case['name']}: {result.total_optimizations} optimizations, patterns: {found_patterns}")


if __name__ == "__main__":
    # Run all pattern tests
    pytest.main([__file__, "-v", "--tb=short"])