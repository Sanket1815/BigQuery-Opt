"""Integration tests using BigQuery sandbox with real data and queries."""

import pytest
import time
import uuid
from typing import Dict, List, Any
from google.cloud import bigquery
from google.cloud.exceptions import GoogleCloudError

from src.optimizer.query_optimizer import BigQueryOptimizer
from src.common.models import OptimizationResult
from config.settings import get_settings


@pytest.mark.integration
@pytest.mark.requires_bigquery
class TestBigQuerySandboxIntegration:
    """Integration tests using BigQuery sandbox with sample data."""
    
    @classmethod
    def setup_class(cls):
        """Setup test environment with sample data."""
        cls.settings = get_settings()
        cls.client = bigquery.Client(project=cls.settings.google_cloud_project)
        cls.dataset_id = f"optimizer_test_{uuid.uuid4().hex[:8]}"
        cls.optimizer = BigQueryOptimizer(validate_results=True)
        
        # Create test dataset
        cls._create_test_dataset()
        cls._create_sample_tables()
        cls._populate_sample_data()
    
    @classmethod
    def teardown_class(cls):
        """Cleanup test environment."""
        try:
            cls.client.delete_dataset(cls.dataset_id, delete_contents=True)
        except Exception as e:
            print(f"Warning: Failed to cleanup test dataset: {e}")
    
    @classmethod
    def _create_test_dataset(cls):
        """Create test dataset."""
        dataset = bigquery.Dataset(f"{cls.settings.google_cloud_project}.{cls.dataset_id}")
        dataset.location = "US"
        dataset.description = "Test dataset for BigQuery Query Optimizer"
        
        try:
            cls.client.create_dataset(dataset)
            print(f"Created test dataset: {cls.dataset_id}")
        except GoogleCloudError as e:
            if "already exists" not in str(e).lower():
                raise
    
    @classmethod
    def _create_sample_tables(cls):
        """Create sample tables for testing."""
        
        # Customers table (small table - 1000 rows)
        customers_schema = [
            bigquery.SchemaField("customer_id", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("customer_name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("email", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("registration_date", "DATE", mode="REQUIRED"),
            bigquery.SchemaField("status", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("region", "STRING", mode="REQUIRED"),
        ]
        
        # Orders table (large table - 100K rows, partitioned)
        orders_schema = [
            bigquery.SchemaField("order_id", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("customer_id", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("order_date", "DATE", mode="REQUIRED"),
            bigquery.SchemaField("total_amount", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("status", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("product_category", "STRING", mode="REQUIRED"),
        ]
        
        # Order items table (very large - 500K rows)
        order_items_schema = [
            bigquery.SchemaField("item_id", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("order_id", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("product_id", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("quantity", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("unit_price", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("item_date", "DATE", mode="REQUIRED"),
        ]
        
        # Products table (medium table - 10K rows)
        products_schema = [
            bigquery.SchemaField("product_id", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("product_name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("category", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("price", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("supplier_id", "INTEGER", mode="REQUIRED"),
        ]
        
        tables_config = [
            ("customers", customers_schema, None, None),
            ("orders", orders_schema, "order_date", ["customer_id", "status"]),
            ("order_items", order_items_schema, "item_date", ["order_id", "product_id"]),
            ("products", products_schema, None, ["category", "supplier_id"]),
        ]
        
        for table_name, schema, partition_field, clustering_fields in tables_config:
            table_id = f"{cls.settings.google_cloud_project}.{cls.dataset_id}.{table_name}"
            table = bigquery.Table(table_id, schema=schema)
            
            # Add partitioning if specified
            if partition_field:
                table.time_partitioning = bigquery.TimePartitioning(
                    type_=bigquery.TimePartitioningType.DAY,
                    field=partition_field
                )
            
            # Add clustering if specified
            if clustering_fields:
                table.clustering_fields = clustering_fields
            
            try:
                cls.client.create_table(table)
                print(f"Created table: {table_name}")
            except GoogleCloudError as e:
                if "already exists" not in str(e).lower():
                    raise
    
    @classmethod
    def _populate_sample_data(cls):
        """Populate tables with sample data."""
        
        # Generate customers data
        customers_query = f"""
        INSERT INTO `{cls.settings.google_cloud_project}.{cls.dataset_id}.customers`
        SELECT 
            customer_id,
            CONCAT('Customer_', CAST(customer_id AS STRING)) as customer_name,
            CONCAT('customer', CAST(customer_id AS STRING), '@example.com') as email,
            DATE_ADD('2020-01-01', INTERVAL MOD(customer_id * 7, 1460) DAY) as registration_date,
            CASE MOD(customer_id, 4)
                WHEN 0 THEN 'active'
                WHEN 1 THEN 'inactive'
                WHEN 2 THEN 'premium'
                ELSE 'trial'
            END as status,
            CASE MOD(customer_id, 5)
                WHEN 0 THEN 'North'
                WHEN 1 THEN 'South'
                WHEN 2 THEN 'East'
                WHEN 3 THEN 'West'
                ELSE 'Central'
            END as region
        FROM UNNEST(GENERATE_ARRAY(1, 1000)) as customer_id
        """
        
        # Generate orders data
        orders_query = f"""
        INSERT INTO `{cls.settings.google_cloud_project}.{cls.dataset_id}.orders`
        SELECT 
            order_id,
            MOD(order_id, 1000) + 1 as customer_id,
            DATE_ADD('2023-01-01', INTERVAL MOD(order_id * 3, 730) DAY) as order_date,
            ROUND(10 + (MOD(order_id * 17, 1000) / 10.0), 2) as total_amount,
            CASE MOD(order_id, 5)
                WHEN 0 THEN 'completed'
                WHEN 1 THEN 'pending'
                WHEN 2 THEN 'shipped'
                WHEN 3 THEN 'cancelled'
                ELSE 'processing'
            END as status,
            CASE MOD(order_id, 6)
                WHEN 0 THEN 'Electronics'
                WHEN 1 THEN 'Clothing'
                WHEN 2 THEN 'Books'
                WHEN 3 THEN 'Home'
                WHEN 4 THEN 'Sports'
                ELSE 'Beauty'
            END as product_category
        FROM UNNEST(GENERATE_ARRAY(1, 100000)) as order_id
        """
        
        # Generate products data
        products_query = f"""
        INSERT INTO `{cls.settings.google_cloud_project}.{cls.dataset_id}.products`
        SELECT 
            product_id,
            CONCAT('Product_', CAST(product_id AS STRING)) as product_name,
            CASE MOD(product_id, 6)
                WHEN 0 THEN 'Electronics'
                WHEN 1 THEN 'Clothing'
                WHEN 2 THEN 'Books'
                WHEN 3 THEN 'Home'
                WHEN 4 THEN 'Sports'
                ELSE 'Beauty'
            END as category,
            ROUND(5 + (MOD(product_id * 13, 500) / 5.0), 2) as price,
            MOD(product_id, 100) + 1 as supplier_id
        FROM UNNEST(GENERATE_ARRAY(1, 10000)) as product_id
        """
        
        # Generate order items data
        order_items_query = f"""
        INSERT INTO `{cls.settings.google_cloud_project}.{cls.dataset_id}.order_items`
        SELECT 
            item_id,
            MOD(item_id, 100000) + 1 as order_id,
            MOD(item_id * 7, 10000) + 1 as product_id,
            MOD(item_id, 5) + 1 as quantity,
            ROUND(5 + (MOD(item_id * 11, 200) / 10.0), 2) as unit_price,
            DATE_ADD('2023-01-01', INTERVAL MOD(item_id * 2, 730) DAY) as item_date
        FROM UNNEST(GENERATE_ARRAY(1, 500000)) as item_id
        """
        
        queries = [
            ("customers", customers_query),
            ("orders", orders_query), 
            ("products", products_query),
            ("order_items", order_items_query)
        ]
        
        for table_name, query in queries:
            try:
                job = cls.client.query(query)
                job.result()  # Wait for completion
                print(f"Populated {table_name} table")
            except Exception as e:
                print(f"Warning: Failed to populate {table_name}: {e}")
    
    def test_simple_query_optimization(self):
        """Test 1: Simple SELECT with inefficient WHERE clause."""
        
        # Intentionally inefficient query - no partition filter, SELECT *
        inefficient_query = f"""
        SELECT *
        FROM `{self.settings.google_cloud_project}.{self.dataset_id}.orders`
        WHERE order_date >= '2024-01-01'
        AND status = 'completed'
        ORDER BY total_amount DESC
        LIMIT 100
        """
        
        result = self.optimizer.optimize_query(
            inefficient_query,
            validate_results=True,
            measure_performance=True
        )
        
        # Assertions
        assert result.total_optimizations >= 1
        assert result.results_identical == True
        assert "SELECT *" not in result.optimized_query  # Should be pruned
        assert "_PARTITIONDATE" in result.optimized_query or "partition" in result.get_summary().lower()
        
        # Performance should improve
        if result.actual_improvement:
            assert result.actual_improvement > 0.1  # At least 10% improvement
        
        print(f"Simple Query Test - Optimizations: {result.total_optimizations}")
        print(f"Estimated improvement: {result.estimated_improvement:.1%}")
        if result.actual_improvement:
            print(f"Actual improvement: {result.actual_improvement:.1%}")
    
    def test_complex_join_optimization(self):
        """Test 2: Multi-table JOIN with suboptimal ordering."""
        
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
        WHERE o.order_date >= '2024-01-01'
        AND c.status = 'active'
        AND p.category = 'Electronics'
        """
        
        result = self.optimizer.optimize_query(
            inefficient_query,
            validate_results=True,
            measure_performance=True
        )
        
        # Assertions
        assert result.total_optimizations >= 1
        assert result.results_identical == True
        
        # Should suggest JOIN reordering and partition filtering
        optimization_types = [opt.pattern_id for opt in result.optimizations_applied]
        assert any("join" in opt_type.lower() for opt_type in optimization_types)
        
        print(f"Complex JOIN Test - Optimizations: {result.total_optimizations}")
        print(f"Applied patterns: {[opt.pattern_name for opt in result.optimizations_applied]}")
    
    def test_aggregation_without_partitioning(self):
        """Test 3: GROUP BY without proper partitioning."""
        
        # Inefficient aggregation - no partition filter, COUNT DISTINCT
        inefficient_query = f"""
        SELECT 
            product_category,
            COUNT(*) as total_orders,
            COUNT(DISTINCT customer_id) as unique_customers,
            SUM(total_amount) as total_revenue,
            AVG(total_amount) as avg_order_value
        FROM `{self.settings.google_cloud_project}.{self.dataset_id}.orders`
        WHERE status IN ('completed', 'shipped')
        GROUP BY product_category
        ORDER BY total_revenue DESC
        """
        
        result = self.optimizer.optimize_query(
            inefficient_query,
            validate_results=True,
            measure_performance=True
        )
        
        # Assertions
        assert result.total_optimizations >= 1
        assert result.results_identical == True
        
        # Should suggest approximate aggregation and partition filtering
        optimization_summary = result.get_summary().lower()
        assert "partition" in optimization_summary or "approx" in optimization_summary
        
        print(f"Aggregation Test - Optimizations: {result.total_optimizations}")
        print(f"Summary: {result.get_summary()}")
    
    def test_window_function_optimization(self):
        """Test 4: Inefficient window function specifications."""
        
        # Inefficient window function - no proper partitioning
        inefficient_query = f"""
        SELECT 
            customer_id,
            order_date,
            total_amount,
            ROW_NUMBER() OVER (ORDER BY total_amount DESC) as overall_rank,
            RANK() OVER (ORDER BY order_date) as date_rank,
            LAG(total_amount) OVER (ORDER BY order_date) as prev_amount
        FROM `{self.settings.google_cloud_project}.{self.dataset_id}.orders`
        WHERE order_date >= '2024-01-01'
        AND status = 'completed'
        LIMIT 1000
        """
        
        result = self.optimizer.optimize_query(
            inefficient_query,
            validate_results=True,
            measure_performance=True
        )
        
        # Assertions
        assert result.results_identical == True
        
        # May or may not have optimizations depending on the specific case
        print(f"Window Function Test - Optimizations: {result.total_optimizations}")
        if result.optimizations_applied:
            print(f"Applied: {[opt.pattern_name for opt in result.optimizations_applied]}")
    
    def test_nested_subquery_optimization(self):
        """Test 5: Deeply nested subqueries that can be flattened."""
        
        # Deeply nested subqueries
        inefficient_query = f"""
        SELECT *
        FROM `{self.settings.google_cloud_project}.{self.dataset_id}.customers` c
        WHERE c.customer_id IN (
            SELECT o.customer_id
            FROM `{self.settings.google_cloud_project}.{self.dataset_id}.orders` o
            WHERE o.order_id IN (
                SELECT oi.order_id
                FROM `{self.settings.google_cloud_project}.{self.dataset_id}.order_items` oi
                WHERE oi.product_id IN (
                    SELECT p.product_id
                    FROM `{self.settings.google_cloud_project}.{self.dataset_id}.products` p
                    WHERE p.category = 'Electronics'
                    AND p.price > 100
                )
                AND oi.quantity > 2
            )
            AND o.order_date >= '2024-01-01'
            AND o.status = 'completed'
        )
        AND c.status = 'active'
        """
        
        result = self.optimizer.optimize_query(
            inefficient_query,
            validate_results=True,
            measure_performance=True
        )
        
        # Assertions
        assert result.results_identical == True
        
        # Should suggest subquery conversion and column pruning
        optimization_types = [opt.pattern_id for opt in result.optimizations_applied]
        expected_optimizations = ["subquery_to_join", "column_pruning", "partition_filtering"]
        
        found_optimizations = sum(1 for expected in expected_optimizations 
                                if any(expected in opt_type for opt_type in optimization_types))
        
        assert found_optimizations >= 1  # At least one expected optimization
        
        print(f"Nested Subquery Test - Optimizations: {result.total_optimizations}")
        print(f"Applied patterns: {[opt.pattern_name for opt in result.optimizations_applied]}")
    
    def test_performance_regression_detection(self):
        """Test that we can detect when an optimization doesn't improve performance."""
        
        # Already well-optimized query
        optimized_query = f"""
        SELECT 
            customer_id,
            order_date,
            total_amount
        FROM `{self.settings.google_cloud_project}.{self.dataset_id}.orders`
        WHERE _PARTITIONDATE >= '2024-01-01'
        AND order_date >= '2024-01-01'
        AND customer_id = 123
        ORDER BY order_date
        LIMIT 10
        """
        
        result = self.optimizer.optimize_query(
            optimized_query,
            validate_results=True,
            measure_performance=True
        )
        
        # Should have minimal or no optimizations
        assert result.results_identical == True
        print(f"Well-optimized Query Test - Optimizations: {result.total_optimizations}")
        
        # If performance was measured and there were optimizations, 
        # ensure no significant regression
        if result.actual_improvement is not None and result.total_optimizations > 0:
            assert result.actual_improvement >= -0.1  # No more than 10% regression
    
    def test_batch_optimization(self):
        """Test batch optimization of multiple queries."""
        
        queries = [
            f"SELECT * FROM `{self.settings.google_cloud_project}.{self.dataset_id}.customers` WHERE status = 'active'",
            f"SELECT COUNT(DISTINCT customer_id) FROM `{self.settings.google_cloud_project}.{self.dataset_id}.orders`",
            f"SELECT customer_id, SUM(total_amount) FROM `{self.settings.google_cloud_project}.{self.dataset_id}.orders` GROUP BY customer_id"
        ]
        
        results = self.optimizer.batch_optimize_queries(
            queries,
            validate_results=True,
            max_concurrent=2
        )
        
        # Assertions
        assert len(results) == len(queries)
        
        for i, result in enumerate(results):
            assert result.results_identical == True, f"Query {i} results not identical"
            print(f"Batch Query {i+1} - Optimizations: {result.total_optimizations}")
    
    def test_table_optimization_suggestions(self):
        """Test table-level optimization suggestions."""
        
        table_id = f"{self.settings.google_cloud_project}.{self.dataset_id}.orders"
        sample_queries = [
            f"SELECT * FROM `{table_id}` WHERE order_date >= '2024-01-01'",
            f"SELECT customer_id, COUNT(*) FROM `{table_id}` GROUP BY customer_id"
        ]
        
        suggestions = self.optimizer.get_table_optimization_suggestions(
            table_id,
            sample_queries
        )
        
        assert len(suggestions) > 0
        print(f"Table optimization suggestions for orders:")
        for suggestion in suggestions:
            print(f"- {suggestion}")


@pytest.mark.integration
class TestOptimizationMetrics:
    """Test optimization metrics and reporting."""
    
    def test_optimization_statistics(self):
        """Test getting optimization statistics."""
        optimizer = BigQueryOptimizer(validate_results=False)
        
        stats = optimizer.get_optimization_statistics()
        
        assert "available_patterns" in stats
        assert "documentation_chunks" in stats
        assert "bigquery_project" in stats
        assert stats["available_patterns"] > 0
        
        print(f"Optimization Statistics:")
        print(f"- Available patterns: {stats['available_patterns']}")
        print(f"- Documentation chunks: {stats['documentation_chunks']}")
        print(f"- BigQuery project: {stats['bigquery_project']}")
    
    def test_connection_health(self):
        """Test system health and connections."""
        optimizer = BigQueryOptimizer(validate_results=False)
        
        connection_ok = optimizer.test_connection()
        assert connection_ok == True
        
        print("All system connections are healthy")


if __name__ == "__main__":
    # Run specific test
    pytest.main([__file__, "-v", "-s"])