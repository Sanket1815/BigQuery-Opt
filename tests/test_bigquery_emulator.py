"""
BigQuery emulator for testing optimization patterns without real BigQuery connection.
Provides realistic query execution simulation for comprehensive testing.
"""

import pytest
import json
import re
from typing import Dict, List, Any, Optional
from unittest.mock import Mock, patch
import pandas as pd

from src.optimizer.query_optimizer import BigQueryOptimizer
from src.common.models import OptimizationResult, QueryAnalysis


class BigQueryEmulator:
    """
    Mock BigQuery emulator that simulates realistic query execution
    for testing optimization patterns without requiring actual BigQuery connection.
    """
    
    def __init__(self):
        # Define mock table schemas and metadata
        self.tables = {
            "customers": {
                "schema": ["customer_id", "customer_name", "customer_tier", "region", "signup_date"],
                "rows": 1000,
                "partitioned": False,
                "partition_field": None,
                "clustered": ["customer_id"],
                "size_bytes": 50000
            },
            "orders": {
                "schema": ["order_id", "customer_id", "order_date", "total_amount", "status", "product_id"],
                "rows": 50000,
                "partitioned": True,
                "partition_field": "order_date",
                "clustered": ["customer_id", "status"],
                "size_bytes": 5000000
            },
            "products": {
                "schema": ["product_id", "product_name", "category", "price"],
                "rows": 50,
                "partitioned": False,
                "partition_field": None,
                "clustered": [],
                "size_bytes": 5000
            },
            "order_items": {
                "schema": ["item_id", "order_id", "product_id", "quantity", "unit_price", "order_date"],
                "rows": 100000,
                "partitioned": True,
                "partition_field": "order_date",
                "clustered": ["order_id"],
                "size_bytes": 10000000
            },
            "large_table": {
                "schema": ["id", "name", "value", "date_column", "category"],
                "rows": 10000000,
                "partitioned": True,
                "partition_field": "date_column",
                "clustered": ["id", "category"],
                "size_bytes": 1000000000
            },
            "small_table": {
                "schema": ["id", "name", "value"],
                "rows": 100,
                "partitioned": False,
                "partition_field": None,
                "clustered": ["id"],
                "size_bytes": 1000
            }
        }
        
        # Sample data for different query types
        self.sample_data = {
            "customers": [
                {"customer_id": 1, "customer_name": "Customer_1", "customer_tier": "Gold", "region": "US-East"},
                {"customer_id": 2, "customer_name": "Customer_2", "customer_tier": "Silver", "region": "US-West"},
                {"customer_id": 3, "customer_name": "Customer_3", "customer_tier": "Bronze", "region": "Europe"}
            ],
            "orders": [
                {"order_id": 1, "customer_id": 1, "order_date": "2024-01-01", "total_amount": 150.75, "status": "completed"},
                {"order_id": 2, "customer_id": 2, "order_date": "2024-01-02", "total_amount": 89.50, "status": "processing"},
                {"order_id": 3, "customer_id": 3, "order_date": "2024-01-03", "total_amount": 234.99, "status": "completed"}
            ],
            "products": [
                {"product_id": 1, "product_name": "Product_1", "category": "Electronics", "price": 125.50},
                {"product_id": 2, "product_name": "Product_2", "category": "Books", "price": 89.25},
                {"product_id": 3, "product_name": "Product_3", "category": "Home", "price": 234.75}
            ]
        }
    
    def execute_query(self, query: str, dry_run: bool = False) -> Dict[str, Any]:
        """Simulate BigQuery query execution with realistic results."""
        
        # Simulate execution time based on query complexity
        execution_time = self._calculate_execution_time(query)
        bytes_processed = self._calculate_bytes_processed(query)
        
        if dry_run:
            return {
                "success": True,
                "dry_run": True,
                "performance": Mock(
                    execution_time_ms=execution_time,
                    bytes_processed=bytes_processed,
                    cache_hit=False
                ),
                "results": None,
                "row_count": None
            }
        
        # Generate realistic results based on query type
        results = self._generate_query_results(query)
        
        return {
            "success": True,
            "dry_run": False,
            "performance": Mock(
                execution_time_ms=execution_time,
                bytes_processed=bytes_processed,
                cache_hit=False
            ),
            "results": results,
            "row_count": len(results)
        }
    
    def get_table_info(self, table_id: str) -> Dict[str, Any]:
        """Get mock table metadata."""
        table_name = table_id.split('.')[-1]
        
        if table_name in self.tables:
            table_data = self.tables[table_name]
            return {
                "table_id": table_name,
                "num_rows": table_data["rows"],
                "num_bytes": table_data["size_bytes"],
                "partitioning": {
                    "type": "DAY" if table_data["partitioned"] else None,
                    "field": table_data["partition_field"]
                },
                "clustering": {
                    "fields": table_data["clustered"]
                },
                "schema": [
                    {"name": col, "type": "STRING", "mode": "NULLABLE"}
                    for col in table_data["schema"]
                ]
            }
        
        return {"error": f"Table {table_name} not found"}
    
    def validate_query(self, query: str) -> Dict[str, Any]:
        """Validate query syntax."""
        # Simple validation - check for basic SQL keywords
        query_upper = query.upper()
        
        if not query_upper.strip().startswith('SELECT'):
            return {
                "valid": False,
                "error": "Query must start with SELECT",
                "bytes_processed": None
            }
        
        if 'FROM' not in query_upper:
            return {
                "valid": False,
                "error": "Query must include FROM clause",
                "bytes_processed": None
            }
        
        return {
            "valid": True,
            "bytes_processed": self._calculate_bytes_processed(query),
            "estimated_cost": 0.005,
            "error": None
        }
    
    def test_connection(self) -> bool:
        """Mock connection test."""
        return True
    
    def _calculate_execution_time(self, query: str) -> int:
        """Calculate realistic execution time based on query complexity."""
        base_time = 500  # Base 500ms
        
        # Add time for different operations
        query_upper = query.upper()
        
        if "SELECT *" in query_upper:
            base_time += 200  # Extra time for full table scan
        
        join_count = len(re.findall(r'\bJOIN\b', query_upper))
        base_time += join_count * 300  # 300ms per JOIN
        
        if "COUNT(DISTINCT" in query_upper:
            base_time += 1000  # COUNT DISTINCT is expensive
        
        if "GROUP BY" in query_upper:
            base_time += 400  # Aggregation overhead
        
        if "ORDER BY" in query_upper:
            base_time += 300  # Sorting overhead
        
        # Simulate table size impact
        tables_referenced = self._extract_table_names(query)
        for table in tables_referenced:
            if table in self.tables:
                table_size = self.tables[table]["rows"]
                if table_size > 1000000:  # Large table
                    base_time += 500
                elif table_size > 10000:  # Medium table
                    base_time += 200
        
        return base_time
    
    def _calculate_bytes_processed(self, query: str) -> int:
        """Calculate bytes processed based on query and tables."""
        total_bytes = 0
        
        tables_referenced = self._extract_table_names(query)
        for table in tables_referenced:
            if table in self.tables:
                table_bytes = self.tables[table]["size_bytes"]
                
                # Reduce bytes if specific columns selected
                if "SELECT *" not in query.upper():
                    table_bytes = int(table_bytes * 0.6)  # Assume 40% reduction
                
                total_bytes += table_bytes
        
        return total_bytes or 1000000  # Default 1MB
    
    def _generate_query_results(self, query: str) -> List[Dict[str, Any]]:
        """Generate realistic query results based on query type."""
        query_upper = query.upper()
        
        # COUNT queries
        if "COUNT(" in query_upper:
            if "COUNT(DISTINCT" in query_upper:
                return [{"count": 1500}]
            else:
                return [{"count": 5000}]
        
        # Aggregation queries
        if "GROUP BY" in query_upper:
            if "region" in query.lower():
                return [
                    {"region": "US-East", "total": 15000, "count": 500},
                    {"region": "US-West", "total": 12000, "count": 400},
                    {"region": "Europe", "total": 8000, "count": 300}
                ]
            else:
                return [
                    {"group_key": "Group1", "total": 1000},
                    {"group_key": "Group2", "total": 1500}
                ]
        
        # JOIN queries
        if "JOIN" in query_upper:
            return [
                {"customer_name": "Customer_1", "order_total": 150.50, "product_name": "Product_A"},
                {"customer_name": "Customer_2", "order_total": 275.25, "product_name": "Product_B"},
                {"customer_name": "Customer_3", "order_total": 89.75, "product_name": "Product_C"}
            ]
        
        # Window function queries
        if "OVER (" in query_upper:
            return [
                {"customer_id": 1, "order_date": "2024-01-01", "total_amount": 150.75, "rank": 1},
                {"customer_id": 2, "order_date": "2024-01-02", "total_amount": 275.25, "rank": 2},
                {"customer_id": 3, "order_date": "2024-01-03", "total_amount": 89.75, "rank": 3}
            ]
        
        # Simple SELECT queries
        table_name = self._extract_primary_table(query)
        if table_name and table_name in self.sample_data:
            return self.sample_data[table_name][:3]  # Return first 3 rows
        
        # Default result
        return [
            {"id": 1, "name": "Item1", "value": 100},
            {"id": 2, "name": "Item2", "value": 200},
            {"id": 3, "name": "Item3", "value": 300}
        ]
    
    def _extract_table_names(self, query: str) -> List[str]:
        """Extract table names from query."""
        # Simple regex to find table names
        patterns = [
            r'FROM\s+(\w+)',
            r'JOIN\s+(\w+)',
            r'FROM\s+`[^`]*\.([^`]+)`',
            r'JOIN\s+`[^`]*\.([^`]+)`'
        ]
        
        tables = set()
        for pattern in patterns:
            matches = re.findall(pattern, query, re.IGNORECASE)
            tables.update(matches)
        
        return list(tables)
    
    def _extract_primary_table(self, query: str) -> Optional[str]:
        """Extract the primary table from FROM clause."""
        match = re.search(r'FROM\s+(\w+)', query, re.IGNORECASE)
        if match:
            return match.group(1)
        return None


@pytest.mark.unit
class TestBigQueryEmulator:
    """Test the BigQuery emulator functionality."""
    
    def test_emulator_basic_functionality(self):
        """Test basic emulator operations."""
        emulator = BigQueryEmulator()
        
        # Test connection
        assert emulator.test_connection() == True
        
        # Test table info
        table_info = emulator.get_table_info("project.dataset.customers")
        assert table_info["num_rows"] == 1000
        assert table_info["partitioning"]["type"] is None
        
        # Test partitioned table
        orders_info = emulator.get_table_info("project.dataset.orders")
        assert orders_info["partitioning"]["type"] == "DAY"
        assert orders_info["partitioning"]["field"] == "order_date"
    
    def test_query_execution_simulation(self):
        """Test query execution with different query types."""
        emulator = BigQueryEmulator()
        
        # Test simple SELECT
        result = emulator.execute_query("SELECT * FROM customers")
        assert result["success"] == True
        assert len(result["results"]) == 3
        assert "customer_name" in result["results"][0]
        
        # Test COUNT query
        count_result = emulator.execute_query("SELECT COUNT(*) FROM orders")
        assert count_result["results"][0]["count"] == 5000
        
        # Test JOIN query
        join_result = emulator.execute_query("SELECT c.name, o.total FROM customers c JOIN orders o ON c.id = o.customer_id")
        assert "customer_name" in join_result["results"][0]
        assert "order_total" in join_result["results"][0]
    
    def test_performance_simulation(self):
        """Test performance calculation simulation."""
        emulator = BigQueryEmulator()
        
        # Simple query should be faster
        simple_result = emulator.execute_query("SELECT customer_id FROM customers")
        simple_time = simple_result["performance"].execution_time_ms
        
        # Complex query should be slower
        complex_result = emulator.execute_query("""
            SELECT c.*, o.*, p.*
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            JOIN order_items oi ON o.order_id = oi.order_id
            JOIN products p ON oi.product_id = p.product_id
            WHERE COUNT(DISTINCT o.product_id) > 5
        """)
        complex_time = complex_result["performance"].execution_time_ms
        
        assert complex_time > simple_time
    
    def test_bytes_processed_calculation(self):
        """Test bytes processed calculation."""
        emulator = BigQueryEmulator()
        
        # SELECT * should process more bytes
        select_star = emulator.execute_query("SELECT * FROM large_table")
        star_bytes = select_star["performance"].bytes_processed
        
        # Specific columns should process fewer bytes
        select_specific = emulator.execute_query("SELECT id, name FROM large_table")
        specific_bytes = select_specific["performance"].bytes_processed
        
        assert specific_bytes < star_bytes


@pytest.mark.unit
class TestOptimizationPatternsWithEmulator:
    """Test optimization patterns using BigQuery emulator."""
    
    @pytest.fixture(autouse=True)
    def setup_emulator(self):
        """Setup BigQuery emulator for all tests."""
        self.emulator = BigQueryEmulator()
        
        # Patch BigQuery client to use emulator
        with patch('src.optimizer.bigquery_client.BigQueryClient') as mock_bq:
            mock_instance = Mock()
            mock_instance.execute_query = self.emulator.execute_query
            mock_instance.get_table_info = self.emulator.get_table_info
            mock_instance.validate_query = self.emulator.validate_query
            mock_instance.test_connection = self.emulator.test_connection
            mock_instance.project_id = "test-project"
            mock_bq.return_value = mock_instance
            
            # Patch AI optimizer to apply realistic optimizations
            with patch('src.optimizer.ai_optimizer.GeminiQueryOptimizer') as mock_ai:
                mock_ai.return_value = self._create_realistic_ai_optimizer()
                
                self.optimizer = BigQueryOptimizer(validate_results=True)
                yield
    
    def _create_realistic_ai_optimizer(self):
        """Create realistic AI optimizer that applies appropriate patterns."""
        mock_ai = Mock()
        
        def realistic_optimize(query, analysis, table_metadata):
            optimizations = []
            optimized_query = query
            
            # Column Pruning
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
                else:
                    optimized_query = optimized_query.replace("SELECT *", "SELECT id, name, value")
            
            # Approximate Aggregation
            if "COUNT(DISTINCT" in query.upper():
                optimizations.append(Mock(
                    pattern_id="approximate_aggregation",
                    pattern_name="Approximate Aggregation",
                    description="Replaced COUNT(DISTINCT) with APPROX_COUNT_DISTINCT for better performance",
                    expected_improvement=0.5
                ))
                optimized_query = optimized_query.replace("COUNT(DISTINCT", "APPROX_COUNT_DISTINCT(")
            
            # JOIN Reordering
            if "JOIN" in query.upper():
                optimizations.append(Mock(
                    pattern_id="join_reordering",
                    pattern_name="JOIN Reordering",
                    description="Reordered JOINs to place smaller tables first",
                    expected_improvement=0.3
                ))
            
            # Subquery to JOIN
            if "EXISTS" in query.upper() or "IN (SELECT" in query.upper():
                optimizations.append(Mock(
                    pattern_id="subquery_to_join",
                    pattern_name="Subquery to JOIN Conversion",
                    description="Converted subquery to INNER JOIN for better performance",
                    expected_improvement=0.4
                ))
            
            # Window Function Optimization
            if "OVER (" in query.upper() and "PARTITION BY" not in query.upper():
                optimizations.append(Mock(
                    pattern_id="window_optimization",
                    pattern_name="Window Function Optimization",
                    description="Added PARTITION BY clause to window function",
                    expected_improvement=0.2
                ))
                optimized_query = optimized_query.replace("OVER (ORDER BY", "OVER (PARTITION BY customer_id ORDER BY")
            
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
        
        mock_ai.optimize_with_best_practices = realistic_optimize
        return mock_ai
    
    def _calculate_execution_time(self, query: str) -> int:
        """Calculate execution time based on query complexity."""
        base_time = 500
        query_upper = query.upper()
        
        # Add complexity factors
        if "SELECT *" in query_upper:
            base_time += 300
        if "COUNT(DISTINCT" in query_upper:
            base_time += 1500
        if "JOIN" in query_upper:
            base_time += len(re.findall(r'\bJOIN\b', query_upper)) * 400
        if "GROUP BY" in query_upper:
            base_time += 600
        if "ORDER BY" in query_upper:
            base_time += 400
        
        return base_time
    
    def _calculate_bytes_processed(self, query: str) -> int:
        """Calculate bytes processed based on tables and operations."""
        total_bytes = 0
        tables = self._extract_table_names(query)
        
        for table in tables:
            if table in self.emulator.tables:
                table_bytes = self.emulator.tables[table]["size_bytes"]
                
                # Column pruning reduces bytes
                if "SELECT *" not in query.upper():
                    table_bytes = int(table_bytes * 0.6)
                
                total_bytes += table_bytes
        
        return total_bytes or 1000000
    
    def _extract_table_names(self, query: str) -> List[str]:
        """Extract table names from query."""
        patterns = [r'FROM\s+(\w+)', r'JOIN\s+(\w+)']
        tables = set()
        
        for pattern in patterns:
            matches = re.findall(pattern, query, re.IGNORECASE)
            tables.update(matches)
        
        return list(tables)
    
    def _generate_query_results(self, query: str) -> List[Dict[str, Any]]:
        """Generate appropriate results based on query type."""
        return self.emulator._generate_query_results(query)
    
    # Test cases for each optimization pattern
    
    def test_column_pruning_patterns(self):
        """Test 10 different column pruning scenarios."""
        test_queries = [
            "SELECT * FROM customers",
            "SELECT * FROM customers WHERE region = 'US'",
            "SELECT * FROM orders WHERE order_date >= '2024-01-01'",
            "SELECT * FROM products WHERE category = 'Electronics'",
            "SELECT * FROM customers c JOIN orders o ON c.customer_id = o.customer_id",
            "SELECT * FROM (SELECT * FROM customers) WHERE customer_tier = 'Gold'",
            "SELECT DISTINCT * FROM customers",
            "SELECT * FROM customers ORDER BY signup_date",
            "SELECT * FROM customers WHERE customer_id IN (1,2,3)",
            "SELECT * FROM customers LIMIT 100"
        ]
        
        for i, query in enumerate(test_queries, 1):
            result = self.optimizer.optimize_query(query, validate_results=False)
            
            # Should apply column pruning
            assert result.total_optimizations >= 1, f"Query {i}: No optimizations applied"
            
            # Should not have SELECT * in optimized query
            assert "SELECT *" not in result.optimized_query, f"Query {i}: SELECT * not removed"
            
            print(f"✅ Column Pruning Test {i}: {result.total_optimizations} optimizations applied")
    
    def test_join_reordering_patterns(self):
        """Test 10 different JOIN reordering scenarios."""
        test_queries = [
            "SELECT * FROM large_table l JOIN small_table s ON l.id = s.id",
            "SELECT * FROM orders o JOIN customers c ON o.customer_id = c.customer_id",
            "SELECT * FROM order_items oi JOIN orders o ON oi.order_id = o.order_id JOIN customers c ON o.customer_id = c.customer_id",
            "SELECT * FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id",
            "SELECT * FROM products p RIGHT JOIN order_items oi ON p.product_id = oi.product_id",
            "SELECT * FROM customers c FULL OUTER JOIN orders o ON c.customer_id = o.customer_id",
            "SELECT * FROM orders o1 JOIN orders o2 ON o1.customer_id = o2.customer_id",
            "SELECT * FROM customers c JOIN orders o ON c.customer_id = o.customer_id JOIN products p ON o.product_id = p.product_id",
            "SELECT * FROM large_table l1 JOIN large_table l2 ON l1.id = l2.parent_id JOIN small_table s ON l1.category = s.category",
            "SELECT * FROM customers c, orders o WHERE c.customer_id = o.customer_id"
        ]
        
        for i, query in enumerate(test_queries, 1):
            result = self.optimizer.optimize_query(query, validate_results=False)
            
            # Should apply JOIN optimization
            assert result.total_optimizations >= 1, f"Query {i}: No optimizations applied"
            
            # Check that JOIN reordering was applied
            optimization_names = [opt.pattern_name.lower() for opt in result.optimizations_applied]
            has_join_opt = any("join" in name for name in optimization_names)
            assert has_join_opt, f"Query {i}: JOIN optimization not applied"
            
            print(f"✅ JOIN Reordering Test {i}: {result.total_optimizations} optimizations applied")
    
    def test_approximate_aggregation_patterns(self):
        """Test 10 different approximate aggregation scenarios."""
        test_queries = [
            "SELECT COUNT(DISTINCT customer_id) FROM orders",
            "SELECT region, COUNT(DISTINCT customer_id) FROM customers GROUP BY region",
            "SELECT COUNT(DISTINCT product_id) FROM order_items WHERE order_date >= '2024-01-01'",
            "SELECT category, COUNT(DISTINCT customer_id) FROM products p JOIN order_items oi ON p.product_id = oi.product_id GROUP BY category",
            "SELECT DATE(order_date), COUNT(DISTINCT customer_id) FROM orders GROUP BY DATE(order_date)",
            "SELECT COUNT(DISTINCT customer_id), COUNT(DISTINCT product_id) FROM order_items",
            "SELECT customer_tier, COUNT(DISTINCT order_id) FROM customers c JOIN orders o ON c.customer_id = o.customer_id GROUP BY customer_tier",
            "SELECT COUNT(DISTINCT CASE WHEN status = 'completed' THEN customer_id END) FROM orders",
            "SELECT COUNT(DISTINCT customer_id) FROM (SELECT customer_id FROM orders UNION SELECT customer_id FROM order_items)",
            "SELECT AVG(unique_customers) FROM (SELECT region, COUNT(DISTINCT customer_id) as unique_customers FROM customers GROUP BY region)"
        ]
        
        for i, query in enumerate(test_queries, 1):
            result = self.optimizer.optimize_query(query, validate_results=False)
            
            # Should apply approximate aggregation
            assert result.total_optimizations >= 1, f"Query {i}: No optimizations applied"
            
            # Should have APPROX_COUNT_DISTINCT in optimized query
            assert "APPROX_COUNT_DISTINCT" in result.optimized_query, f"Query {i}: Approximate aggregation not applied"
            
            print(f"✅ Approximate Aggregation Test {i}: {result.total_optimizations} optimizations applied")
    
    def test_subquery_conversion_patterns(self):
        """Test 10 different subquery conversion scenarios."""
        test_queries = [
            "SELECT * FROM customers WHERE customer_id IN (SELECT customer_id FROM orders)",
            "SELECT * FROM customers c WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id)",
            "SELECT * FROM customers c WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id)",
            "SELECT * FROM products WHERE product_id NOT IN (SELECT product_id FROM order_items WHERE quantity = 0)",
            "SELECT customer_id, (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.customer_id) FROM customers c",
            "SELECT * FROM customers WHERE customer_id = ANY (SELECT customer_id FROM orders WHERE status = 'completed')",
            "SELECT * FROM customers WHERE customer_id > ALL (SELECT AVG(customer_id) FROM orders GROUP BY region)",
            "SELECT * FROM orders WHERE customer_id IN (SELECT customer_id FROM customers WHERE region IN (SELECT region FROM top_regions))",
            "SELECT * FROM customers c WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id AND EXISTS (SELECT 1 FROM order_items oi WHERE oi.order_id = o.order_id))",
            "SELECT * FROM products WHERE category IN (SELECT DISTINCT category FROM order_items oi JOIN products p ON oi.product_id = p.product_id)"
        ]
        
        for i, query in enumerate(test_queries, 1):
            result = self.optimizer.optimize_query(query, validate_results=False)
            
            # Should apply subquery conversion
            assert result.total_optimizations >= 1, f"Query {i}: No optimizations applied"
            
            # Check for subquery optimization
            optimization_names = [opt.pattern_name.lower() for opt in result.optimizations_applied]
            has_subquery_opt = any("subquery" in name or "join" in name for name in optimization_names)
            assert has_subquery_opt, f"Query {i}: Subquery optimization not applied"
            
            print(f"✅ Subquery Conversion Test {i}: {result.total_optimizations} optimizations applied")
    
    def test_window_function_patterns(self):
        """Test 10 different window function optimization scenarios."""
        test_queries = [
            "SELECT customer_id, ROW_NUMBER() OVER (ORDER BY order_date) FROM orders",
            "SELECT customer_id, RANK() OVER (ORDER BY total_amount DESC) FROM orders",
            "SELECT customer_id, DENSE_RANK() OVER (ORDER BY signup_date) FROM customers",
            "SELECT order_id, LAG(total_amount) OVER (ORDER BY order_date) FROM orders",
            "SELECT order_id, LEAD(total_amount) OVER (ORDER BY order_date) FROM orders",
            "SELECT customer_id, SUM(total_amount) OVER (ORDER BY order_date ROWS UNBOUNDED PRECEDING) FROM orders",
            "SELECT customer_id, AVG(total_amount) OVER (ORDER BY order_date ROWS BETWEEN 2 PRECEDING AND 2 FOLLOWING) FROM orders",
            "SELECT customer_id, FIRST_VALUE(total_amount) OVER (ORDER BY order_date) FROM orders",
            "SELECT customer_id, LAST_VALUE(total_amount) OVER (ORDER BY order_date) FROM orders",
            "SELECT customer_id, NTILE(4) OVER (ORDER BY total_amount) FROM orders"
        ]
        
        for i, query in enumerate(test_queries, 1):
            result = self.optimizer.optimize_query(query, validate_results=False)
            
            # Should apply window function optimization
            assert result.total_optimizations >= 1, f"Query {i}: No optimizations applied"
            
            # Should have PARTITION BY in optimized query
            assert "PARTITION BY" in result.optimized_query, f"Query {i}: PARTITION BY not added"
            
            print(f"✅ Window Function Test {i}: {result.total_optimizations} optimizations applied")
    
    def test_comprehensive_pattern_coverage(self):
        """Test comprehensive coverage of all major patterns."""
        
        # Complex query that should trigger multiple patterns
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
        GROUP BY c.customer_id, c.customer_name, c.customer_tier, c.region, c.signup_date, o.order_id, o.order_date, o.total_amount, o.status, o.product_id
        """
        
        result = self.optimizer.optimize_query(complex_query, validate_results=False)
        
        # Should apply multiple optimizations
        assert result.total_optimizations >= 3, f"Expected multiple optimizations, got {result.total_optimizations}"
        
        # Check for specific patterns
        pattern_names = [opt.pattern_name.lower() for opt in result.optimizations_applied]
        
        expected_patterns = ["column", "approximate", "subquery", "window"]
        found_patterns = []
        
        for expected in expected_patterns:
            if any(expected in name for name in pattern_names):
                found_patterns.append(expected)
        
        assert len(found_patterns) >= 2, f"Expected multiple patterns, found: {found_patterns}"
        
        print(f"✅ Comprehensive Pattern Test: {result.total_optimizations} optimizations, patterns: {found_patterns}")
    
    def test_performance_improvement_simulation(self):
        """Test performance improvement simulation."""
        
        # Test queries with expected performance improvements
        test_cases = [
            {
                "query": "SELECT * FROM large_table WHERE date_column >= '2024-01-01'",
                "expected_min_improvement": 0.2
            },
            {
                "query": "SELECT COUNT(DISTINCT customer_id) FROM large_table",
                "expected_min_improvement": 0.4
            },
            {
                "query": "SELECT * FROM large_table l JOIN small_table s ON l.id = s.id",
                "expected_min_improvement": 0.15
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            # Get original performance
            original_result = self.emulator.execute_query(test_case["query"])
            original_time = original_result["performance"].execution_time_ms
            
            # Optimize query
            optimization_result = self.optimizer.optimize_query(test_case["query"], validate_results=False)
            
            # Get optimized performance
            optimized_result = self.emulator.execute_query(optimization_result.optimized_query)
            optimized_time = optimized_result["performance"].execution_time_ms
            
            # Calculate improvement
            improvement = (original_time - optimized_time) / original_time
            
            assert improvement >= test_case["expected_min_improvement"], \
                f"Test {i}: Improvement {improvement:.1%} below expected {test_case['expected_min_improvement']:.1%}"
            
            print(f"✅ Performance Test {i}: {improvement:.1%} improvement (expected: {test_case['expected_min_improvement']:.1%})")


if __name__ == "__main__":
    # Run comprehensive pattern tests
    pytest.main([__file__, "-v", "--tb=short"])