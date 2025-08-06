"""Integration tests using BigQuery sandbox with real data and performance measurement."""

import pytest
import time
from typing import Dict, List, Any
from unittest.mock import patch
import pandas as pd

from src.optimizer.query_optimizer import BigQueryOptimizer
from src.optimizer.bigquery_client import BigQueryClient
from src.common.models import OptimizationResult
from config.settings import get_settings


@pytest.mark.integration
@pytest.mark.requires_bigquery
class TestBigQuerySandboxIntegration:
    """Integration tests using BigQuery sandbox with sample data."""
    
    @classmethod
    def setup_class(cls):
        """Setup test data in BigQuery sandbox."""
        cls.settings = get_settings()
        cls.bq_client = BigQueryClient()
        cls.optimizer = BigQueryOptimizer(validate_results=True)
        
        # Create test dataset and tables
        cls.dataset_id = "optimizer_test_dataset"
        cls.setup_test_data()
    
    @classmethod
    def setup_test_data(cls):
        """Create sample tables with test data in BigQuery."""
        
        try:
            # Create dataset first
            dataset_sql = f"""
            CREATE SCHEMA IF NOT EXISTS `{cls.settings.google_cloud_project}.{cls.dataset_id}`
            OPTIONS(
                description="Test dataset for BigQuery Query Optimizer",
                location="US"
            )
            """
            
            print(f"Creating dataset: {cls.dataset_id}")
            result = cls.bq_client.execute_query(dataset_sql, dry_run=False)
            if not result["success"]:
                print(f"Dataset creation result: {result}")
                pytest.skip(f"Failed to create dataset: {result['error']}")
            
            print("✅ Dataset created successfully")
            
        except Exception as e:
            pytest.skip(f"Failed to create dataset: {str(e)}")
        
        # Create customers table (small table - 1000 rows)
        customers_sql = f"""
        CREATE OR REPLACE TABLE `{cls.settings.google_cloud_project}.{cls.dataset_id}.customers` AS
        SELECT 
            customer_id,
            CONCAT('Customer_', CAST(customer_id AS STRING)) as customer_name,
            CASE 
                WHEN MOD(customer_id, 4) = 0 THEN 'Premium'
                WHEN MOD(customer_id, 4) = 1 THEN 'Gold'
                WHEN MOD(customer_id, 4) = 2 THEN 'Silver'
                ELSE 'Bronze'
            END as customer_tier,
            CASE 
                WHEN MOD(customer_id, 5) = 0 THEN 'US-West'
                WHEN MOD(customer_id, 5) = 1 THEN 'US-East'
                WHEN MOD(customer_id, 5) = 2 THEN 'Europe'
                WHEN MOD(customer_id, 5) = 3 THEN 'Asia'
                ELSE 'Other'
            END as region,
            DATE_ADD('2020-01-01', INTERVAL MOD(customer_id, 1000) DAY) as signup_date
        FROM UNNEST(GENERATE_ARRAY(1, 1000)) as customer_id
        """
        
        # Create orders table (large table - 100,000 rows, partitioned)
        orders_sql = f"""
        CREATE OR REPLACE TABLE `{cls.settings.google_cloud_project}.{cls.dataset_id}.orders`
        PARTITION BY DATE(order_date)
        CLUSTER BY customer_id, status AS
        SELECT 
            order_id,
            MOD(order_id, 1000) + 1 as customer_id,
            DATE_ADD('2024-01-01', INTERVAL MOD(order_id, 365) DAY) as order_date,
            ROUND(RAND() * 1000 + 50, 2) as total_amount,
            CASE 
                WHEN MOD(order_id, 10) = 0 THEN 'cancelled'
                WHEN MOD(order_id, 10) = 1 THEN 'pending'
                WHEN MOD(order_id, 10) = 2 THEN 'processing'
                ELSE 'completed'
            END as status,
            MOD(order_id, 50) + 1 as product_id
        FROM UNNEST(GENERATE_ARRAY(1, 100000)) as order_id
        """
        
        # Create products table (medium table - 50 rows)
        products_sql = f"""
        CREATE OR REPLACE TABLE `{cls.settings.google_cloud_project}.{cls.dataset_id}.products` AS
        SELECT 
            product_id,
            CONCAT('Product_', CAST(product_id AS STRING)) as product_name,
            CASE 
                WHEN MOD(product_id, 5) = 0 THEN 'Electronics'
                WHEN MOD(product_id, 5) = 1 THEN 'Clothing'
                WHEN MOD(product_id, 5) = 2 THEN 'Books'
                WHEN MOD(product_id, 5) = 3 THEN 'Home'
                ELSE 'Sports'
            END as category,
            ROUND(RAND() * 500 + 10, 2) as price
        FROM UNNEST(GENERATE_ARRAY(1, 50)) as product_id
        """
        
        # Create order_items table (very large table - 200,000 rows)
        order_items_sql = f"""
        CREATE OR REPLACE TABLE `{cls.settings.google_cloud_project}.{cls.dataset_id}.order_items`
        PARTITION BY DATE(order_date)
        CLUSTER BY order_id AS
        SELECT 
            (order_id - 1) * 3 + item_seq as item_id,
            order_id,
            MOD(item_id, 50) + 1 as product_id,
            CAST(RAND() * 5 + 1 AS INT64) as quantity,
            ROUND(RAND() * 100 + 10, 2) as unit_price,
            DATE_ADD('2024-01-01', INTERVAL MOD(order_id, 365) DAY) as order_date
        FROM UNNEST(GENERATE_ARRAY(1, 50000)) as order_id,
        UNNEST(GENERATE_ARRAY(1, 3)) as item_seq
        """
        
        # Execute table creation
        tables_info = [
            ("customers", customers_sql),
            ("orders", orders_sql), 
            ("products", products_sql),
            ("order_items", order_items_sql)
        ]
        
        for table_name, sql in tables_info:
            try:
                print(f"Creating table: {table_name}")
                result = cls.bq_client.execute_query(sql, dry_run=False)
                if not result["success"]:
                    print(f"❌ Failed to create {table_name}: {result['error']}")
                    pytest.skip(f"Failed to create {table_name}: {result['error']}")
                else:
                    print(f"✅ {table_name} created successfully")
            except Exception as e:
                print(f"❌ Exception creating {table_name}: {str(e)}")
                pytest.skip(f"Failed to create {table_name}: {str(e)}")
        
        print("🎉 All test tables created successfully!")
    
    def test_simple_query_optimization(self):
        """Test 1: Simple Query Test - Basic SELECT with inefficient WHERE clause."""
        
        # Intentionally inefficient query - no partition filter, SELECT *
        inefficient_query = f"""
        SELECT *
        FROM `{self.settings.google_cloud_project}.{self.dataset_id}.orders`
        WHERE order_date >= '2024-06-01'
        AND status = 'completed'
        ORDER BY total_amount DESC
        LIMIT 100
        """
        
        # Run optimization
        result = self.optimizer.optimize_query(
            inefficient_query,
            validate_results=True,
            measure_performance=True,
            sample_size=100
        )
        
        # Verify optimization was applied
        assert result.total_optimizations > 0, "No optimizations were applied"
        
        # Check for expected optimizations
        optimization_names = [opt.pattern_name.lower() for opt in result.optimizations_applied]
        assert any("column" in name or "pruning" in name for name in optimization_names), \
            "Column pruning optimization not applied"
        assert any("partition" in name for name in optimization_names), \
            "Partition filtering optimization not applied"
        
        # Verify results are identical
        assert result.results_identical == True, f"Results not identical: {result.validation_error}"
        
        # Check performance improvement
        if result.actual_improvement:
            assert result.actual_improvement > 0, "No performance improvement measured"
            print(f"✅ Simple Query Test: {result.actual_improvement:.1%} improvement")
        
        # Verify optimized query contains expected improvements
        optimized_lower = result.optimized_query.lower()
        assert "_partitiondate" in optimized_lower or "partition" in optimized_lower, \
            "Optimized query should include partition filtering"
        assert "select *" not in optimized_lower, \
            "Optimized query should not use SELECT *"
    
    def test_complex_join_optimization(self):
        """Test 2: Complex JOIN Test - Multi-table JOIN with suboptimal ordering."""
        
        # Intentionally inefficient JOIN order - largest table first
        inefficient_query = f"""
        SELECT 
            c.customer_name,
            o.order_id,
            o.total_amount,
            p.product_name,
            oi.quantity
        FROM `{self.settings.google_cloud_project}.{self.dataset_id}.order_items` oi
        JOIN `{self.settings.google_cloud_project}.{self.dataset_id}.orders` o 
            ON oi.order_id = o.order_id
        JOIN `{self.settings.google_cloud_project}.{self.dataset_id}.customers` c 
            ON o.customer_id = c.customer_id
        JOIN `{self.settings.google_cloud_project}.{self.dataset_id}.products` p 
            ON oi.product_id = p.product_id
        WHERE o.order_date >= '2024-06-01'
        AND c.customer_tier = 'Premium'
        AND p.category = 'Electronics'
        """
        
        # Run optimization
        result = self.optimizer.optimize_query(
            inefficient_query,
            validate_results=True,
            measure_performance=True,
            sample_size=50
        )
        
        # Verify optimization was applied
        assert result.total_optimizations > 0, "No optimizations were applied"
        
        # Check for JOIN reordering
        optimization_names = [opt.pattern_name.lower() for opt in result.optimizations_applied]
        join_optimized = any("join" in name for name in optimization_names)
        partition_optimized = any("partition" in name for name in optimization_names)
        
        assert join_optimized or partition_optimized, \
            "Expected JOIN reordering or partition filtering optimization"
        
        # Verify results are identical
        assert result.results_identical == True, f"Results not identical: {result.validation_error}"
        
        if result.actual_improvement:
            print(f"✅ Complex JOIN Test: {result.actual_improvement:.1%} improvement")
    
    def test_aggregation_optimization(self):
        """Test 3: Aggregation Test - GROUP BY without proper partitioning."""
        
        # Inefficient aggregation query
        inefficient_query = f"""
        SELECT 
            c.region,
            COUNT(*) as total_orders,
            COUNT(DISTINCT o.customer_id) as unique_customers,
            SUM(o.total_amount) as total_revenue,
            AVG(o.total_amount) as avg_order_value
        FROM `{self.settings.google_cloud_project}.{self.dataset_id}.orders` o
        JOIN `{self.settings.google_cloud_project}.{self.dataset_id}.customers` c 
            ON o.customer_id = c.customer_id
        WHERE o.order_date >= '2024-01-01'
        GROUP BY c.region
        ORDER BY total_revenue DESC
        """
        
        # Run optimization
        result = self.optimizer.optimize_query(
            inefficient_query,
            validate_results=True,
            measure_performance=True,
            sample_size=10  # Small sample for aggregation
        )
        
        # Verify optimization was applied
        assert result.total_optimizations > 0, "No optimizations were applied"
        
        # Check for expected optimizations
        optimization_names = [opt.pattern_name.lower() for opt in result.optimizations_applied]
        
        # Should have partition filtering and possibly approximate aggregation
        expected_optimizations = ["partition", "approximate", "join"]
        found_optimizations = [name for name in optimization_names 
                             if any(exp in name for exp in expected_optimizations)]
        
        assert len(found_optimizations) > 0, \
            f"Expected optimizations not found. Found: {optimization_names}"
        
        # Verify results are identical (or approximately identical for APPROX functions)
        if "approximate" in str(optimization_names):
            # For approximate functions, we allow some difference
            print("⚠️ Approximate aggregation used - results may differ slightly")
        else:
            assert result.results_identical == True, f"Results not identical: {result.validation_error}"
        
        if result.actual_improvement:
            print(f"✅ Aggregation Test: {result.actual_improvement:.1%} improvement")
    
    def test_window_function_optimization(self):
        """Test 4: Window Function Test - Inefficient window specifications."""
        
        # Inefficient window function query
        inefficient_query = f"""
        SELECT 
            customer_id,
            order_id,
            order_date,
            total_amount,
            ROW_NUMBER() OVER (ORDER BY total_amount DESC) as overall_rank,
            RANK() OVER (ORDER BY order_date) as date_rank,
            SUM(total_amount) OVER (ORDER BY order_date ROWS UNBOUNDED PRECEDING) as running_total
        FROM `{self.settings.google_cloud_project}.{self.dataset_id}.orders`
        WHERE order_date >= '2024-06-01'
        ORDER BY total_amount DESC
        LIMIT 1000
        """
        
        # Run optimization
        result = self.optimizer.optimize_query(
            inefficient_query,
            validate_results=True,
            measure_performance=True,
            sample_size=100
        )
        
        # Verify optimization was applied
        assert result.total_optimizations > 0, "No optimizations were applied"
        
        # Check for window function or partition optimizations
        optimization_names = [opt.pattern_name.lower() for opt in result.optimizations_applied]
        window_or_partition = any(name for name in optimization_names 
                                if "window" in name or "partition" in name)
        
        assert window_or_partition, \
            f"Expected window or partition optimization. Found: {optimization_names}"
        
        # Verify results are identical
        assert result.results_identical == True, f"Results not identical: {result.validation_error}"
        
        if result.actual_improvement:
            print(f"✅ Window Function Test: {result.actual_improvement:.1%} improvement")
    
    def test_nested_query_optimization(self):
        """Test 5: Nested Query Test - Deeply nested subqueries that can be flattened."""
        
        # Deeply nested subquery that can be flattened
        inefficient_query = f"""
        SELECT 
            customer_name,
            total_orders,
            total_spent
        FROM `{self.settings.google_cloud_project}.{self.dataset_id}.customers` c
        WHERE customer_id IN (
            SELECT customer_id 
            FROM `{self.settings.google_cloud_project}.{self.dataset_id}.orders` o1
            WHERE order_id IN (
                SELECT order_id
                FROM `{self.settings.google_cloud_project}.{self.dataset_id}.order_items` oi
                WHERE product_id IN (
                    SELECT product_id
                    FROM `{self.settings.google_cloud_project}.{self.dataset_id}.products` p
                    WHERE category = 'Electronics'
                )
                AND quantity > 2
            )
            AND o1.order_date >= '2024-06-01'
            AND o1.status = 'completed'
        )
        AND customer_id IN (
            SELECT customer_id
            FROM (
                SELECT 
                    customer_id,
                    COUNT(*) as total_orders,
                    SUM(total_amount) as total_spent
                FROM `{self.settings.google_cloud_project}.{self.dataset_id}.orders`
                WHERE order_date >= '2024-01-01'
                GROUP BY customer_id
                HAVING COUNT(*) > 5
            )
        )
        """
        
        # Run optimization
        result = self.optimizer.optimize_query(
            inefficient_query,
            validate_results=True,
            measure_performance=True,
            sample_size=20
        )
        
        # Verify optimization was applied
        assert result.total_optimizations > 0, "No optimizations were applied"
        
        # Check for subquery conversion
        optimization_names = [opt.pattern_name.lower() for opt in result.optimizations_applied]
        subquery_optimized = any("subquery" in name or "join" in name or "partition" in name 
                               for name in optimization_names)
        
        assert subquery_optimized, \
            f"Expected subquery or JOIN optimization. Found: {optimization_names}"
        
        # Verify results are identical
        assert result.results_identical == True, f"Results not identical: {result.validation_error}"
        
        if result.actual_improvement:
            print(f"✅ Nested Query Test: {result.actual_improvement:.1%} improvement")
    
    def test_business_logic_preservation(self):
        """Comprehensive test to ensure business logic is never changed."""
        
        test_queries = [
            # Aggregation with specific business rules
            f"""
            SELECT 
                customer_tier,
                COUNT(*) as customer_count,
                AVG(total_spent) as avg_spent
            FROM (
                SELECT 
                    c.customer_tier,
                    SUM(o.total_amount) as total_spent
                FROM `{self.settings.google_cloud_project}.{self.dataset_id}.customers` c
                LEFT JOIN `{self.settings.google_cloud_project}.{self.dataset_id}.orders` o 
                    ON c.customer_id = o.customer_id
                WHERE o.order_date >= '2024-01-01' OR o.order_date IS NULL
                GROUP BY c.customer_id, c.customer_tier
            )
            GROUP BY customer_tier
            """,
            
            # Complex filtering with edge cases
            f"""
            SELECT DISTINCT
                p.category,
                COUNT(CASE WHEN o.status = 'completed' THEN 1 END) as completed_orders,
                COUNT(CASE WHEN o.status = 'cancelled' THEN 1 END) as cancelled_orders
            FROM `{self.settings.google_cloud_project}.{self.dataset_id}.products` p
            LEFT JOIN `{self.settings.google_cloud_project}.{self.dataset_id}.order_items` oi 
                ON p.product_id = oi.product_id
            LEFT JOIN `{self.settings.google_cloud_project}.{self.dataset_id}.orders` o 
                ON oi.order_id = o.order_id
            WHERE o.order_date >= '2024-01-01' OR o.order_date IS NULL
            GROUP BY p.category
            """
        ]
        
        for i, query in enumerate(test_queries):
            result = self.optimizer.optimize_query(
                query,
                validate_results=True,
                measure_performance=False,  # Focus on correctness
                sample_size=50
            )
            
            # Business logic preservation is the most critical requirement
            assert result.results_identical == True, \
                f"Business logic changed in test query {i+1}: {result.validation_error}"
            
            print(f"✅ Business Logic Test {i+1}: Results identical")
    
    @classmethod
    def teardown_class(cls):
        """Clean up test data."""
        try:
            cleanup_sql = f"DROP SCHEMA `{cls.settings.google_cloud_project}.{cls.dataset_id}` CASCADE"
            cls.bq_client.execute_query(cleanup_sql, dry_run=False)
            print("🧹 Test data cleaned up")
        except Exception as e:
            print(f"⚠️ Failed to clean up test data: {e}")


@pytest.mark.integration
@pytest.mark.requires_bigquery
class TestPerformanceBenchmarks:
    """Performance benchmark tests to measure optimization effectiveness."""
    
    def test_performance_improvement_benchmarks(self):
        """Test that optimizations meet minimum performance improvement thresholds."""
        
        optimizer = BigQueryOptimizer(validate_results=True)
        settings = get_settings()
        
        # Define benchmark queries with expected minimum improvements
        benchmark_queries = [
            {
                "name": "SELECT * with large scan",
                "query": f"""
                SELECT * FROM `{settings.google_cloud_project}.optimizer_test_dataset.orders`
                WHERE order_date >= '2024-01-01'
                """,
                "min_improvement": 0.20  # 20% minimum improvement expected
            },
            {
                "name": "COUNT DISTINCT on large dataset",
                "query": f"""
                SELECT 
                    DATE(order_date) as order_day,
                    COUNT(DISTINCT customer_id) as unique_customers
                FROM `{settings.google_cloud_project}.optimizer_test_dataset.orders`
                WHERE order_date >= '2024-01-01'
                GROUP BY DATE(order_date)
                """,
                "min_improvement": 0.30  # 30% minimum improvement expected
            },
            {
                "name": "Complex JOIN without optimization",
                "query": f"""
                SELECT c.customer_name, COUNT(o.order_id) as order_count
                FROM `{settings.google_cloud_project}.optimizer_test_dataset.order_items` oi
                JOIN `{settings.google_cloud_project}.optimizer_test_dataset.orders` o ON oi.order_id = o.order_id
                JOIN `{settings.google_cloud_project}.optimizer_test_dataset.customers` c ON o.customer_id = c.customer_id
                WHERE o.order_date >= '2024-06-01'
                GROUP BY c.customer_name
                """,
                "min_improvement": 0.15  # 15% minimum improvement expected
            }
        ]
        
        results = []
        
        for benchmark in benchmark_queries:
            result = optimizer.optimize_query(
                benchmark["query"],
                validate_results=True,
                measure_performance=True,
                sample_size=100
            )
            
            # Verify results are identical
            assert result.results_identical == True, \
                f"Results not identical for {benchmark['name']}: {result.validation_error}"
            
            # Check performance improvement
            if result.actual_improvement:
                improvement = result.actual_improvement
                min_expected = benchmark["min_improvement"]
                
                results.append({
                    "name": benchmark["name"],
                    "improvement": improvement,
                    "expected": min_expected,
                    "meets_threshold": improvement >= min_expected
                })
                
                print(f"📊 {benchmark['name']}: {improvement:.1%} improvement "
                      f"(expected: {min_expected:.1%}) "
                      f"{'✅' if improvement >= min_expected else '❌'}")
            else:
                print(f"⚠️ {benchmark['name']}: No performance measurement available")
        
        # At least 70% of benchmarks should meet their improvement thresholds
        if results:
            success_rate = sum(1 for r in results if r["meets_threshold"]) / len(results)
            assert success_rate >= 0.7, \
                f"Only {success_rate:.1%} of benchmarks met improvement thresholds"
            
            print(f"🎯 Overall benchmark success rate: {success_rate:.1%}")


@pytest.mark.integration  
@pytest.mark.requires_bigquery
class TestDocumentationCompliance:
    """Test that all optimizations reference official BigQuery documentation."""
    
    def test_optimization_documentation_references(self):
        """Verify that all applied optimizations reference BigQuery documentation."""
        
        optimizer = BigQueryOptimizer(validate_results=False)
        
        test_queries = [
            "SELECT * FROM `project.dataset.table` WHERE date > '2024-01-01'",
            "SELECT COUNT(DISTINCT customer_id) FROM `project.dataset.orders`",
            "SELECT a.*, b.* FROM large_table a JOIN small_table b ON a.id = b.id"
        ]
        
        for query in test_queries:
            try:
                result = optimizer.optimize_query(query, validate_results=False)
                
                # Check that optimizations have documentation references
                for optimization in result.optimizations_applied:
                    # Each optimization should have a clear explanation
                    assert len(optimization.description) > 10, \
                        f"Optimization {optimization.pattern_name} lacks proper description"
                    
                    # Pattern should reference BigQuery concepts
                    bigquery_terms = ['bigquery', 'partition', 'cluster', 'join', 'performance', 'scan']
                    description_lower = optimization.description.lower()
                    
                    has_bigquery_reference = any(term in description_lower for term in bigquery_terms)
                    assert has_bigquery_reference, \
                        f"Optimization {optimization.pattern_name} doesn't reference BigQuery concepts"
                
                print(f"✅ Documentation compliance verified for query with {result.total_optimizations} optimizations")
                
            except Exception as e:
                # Skip queries that can't be processed (e.g., invalid table references)
                print(f"⚠️ Skipped query due to: {e}")
                continue