"""Pytest configuration and fixtures for BigQuery Query Optimizer tests."""

import os
import pytest
from unittest.mock import Mock, MagicMock
from typing import Generator, Dict, Any

from config.settings import Settings
from src.optimizer.query_optimizer import BigQueryOptimizer
from src.optimizer.bigquery_client import BigQueryClient
from src.crawler.documentation_processor import DocumentationProcessor
from src.common.models import QueryAnalysis, OptimizationPattern, OptimizationType


@pytest.fixture(scope="session")
def test_settings() -> Settings:
    """Test settings with mock configuration."""
    return Settings(
        google_cloud_project="test-project",
        gemini_api_key="test-api-key",
        debug=True,
        dry_run=True,
        docs_output_dir="tests/data/documentation",
        vector_db_path="tests/data/vector_db"
    )


@pytest.fixture
def mock_bigquery_client() -> Generator[Mock, None, None]:
    """Mock BigQuery client for testing."""
    mock_client = Mock(spec=BigQueryClient)
    
    # Mock successful validation
    mock_client.validate_query.return_value = {
        "valid": True,
        "bytes_processed": 1000000,
        "estimated_cost": 0.005,
        "error": None
    }
    
    # Mock successful query execution
    mock_client.execute_query.return_value = {
        "success": True,
        "dry_run": False,
        "performance": Mock(execution_time_ms=1500, bytes_processed=1000000),
        "results": [{"col1": "value1", "col2": 123}],
        "row_count": 1
    }
    
    # Mock performance comparison
    mock_client.compare_query_performance.return_value = {
        "success": True,
        "original_avg_ms": 2000,
        "optimized_avg_ms": 1400,
        "improvement_percentage": 0.3,
        "original_times": [2000, 2100, 1900],
        "optimized_times": [1400, 1500, 1300],
        "iterations": 3
    }
    
    mock_client.test_connection.return_value = True
    mock_client.project_id = "test-project"
    
    yield mock_client


@pytest.fixture
def mock_documentation_processor() -> Generator[Mock, None, None]:
    """Mock documentation processor for testing."""
    mock_processor = Mock(spec=DocumentationProcessor)
    
    # Mock search results
    mock_processor.search_documentation.return_value = [
        {
            "content": "JOIN optimization best practices...",
            "title": "JOIN Performance",
            "url": "https://cloud.google.com/bigquery/docs/joins",
            "optimization_patterns": ["JOIN optimization"],
            "similarity_score": 0.9
        }
    ]
    
    # Mock optimization patterns
    mock_patterns = [
        OptimizationPattern(
            pattern_id="join_reordering",
            name="JOIN Reordering",
            description="Reorder JOINs for better performance",
            optimization_type=OptimizationType.JOIN_REORDERING,
            expected_improvement=0.3,
            applicability_conditions=["JOIN"]
        ),
        OptimizationPattern(
            pattern_id="partition_filtering",
            name="Partition Filtering", 
            description="Add partition filters",
            optimization_type=OptimizationType.PARTITION_FILTERING,
            expected_improvement=0.5,
            applicability_conditions=["WHERE"]
        )
    ]
    
    mock_processor.optimization_patterns = mock_patterns
    mock_processor.get_optimization_patterns_for_query.return_value = mock_patterns
    mock_processor.get_documentation_summary.return_value = {
        "total_chunks": 100,
        "optimization_patterns": 9,
        "embedding_model": "all-MiniLM-L6-v2"
    }
    
    yield mock_processor


@pytest.fixture
def sample_queries() -> Dict[str, str]:
    """Sample SQL queries for testing."""
    return {
        "simple_select": """
            SELECT customer_id, order_date, total_amount
            FROM orders
            WHERE order_date >= '2024-01-01'
        """,
        
        "select_star": """
            SELECT *
            FROM large_table
            WHERE date_column > '2024-01-01'
        """,
        
        "complex_join": """
            SELECT c.customer_name, o.order_id, p.product_name
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            JOIN order_items oi ON o.order_id = oi.order_id
            JOIN products p ON oi.product_id = p.product_id
            WHERE o.order_date >= '2024-01-01'
        """,
        
        "subquery_exists": """
            SELECT customer_id, customer_name
            FROM customers c
            WHERE EXISTS (
                SELECT 1 FROM orders o 
                WHERE o.customer_id = c.customer_id 
                AND o.order_date >= '2024-01-01'
            )
        """,
        
        "count_distinct": """
            SELECT 
                category,
                COUNT(DISTINCT customer_id) as unique_customers
            FROM orders o
            JOIN products p ON o.product_id = p.product_id
            WHERE o.order_date >= '2024-01-01'
            GROUP BY category
        """,
        
        "window_function": """
            SELECT 
                customer_id,
                order_date,
                total_amount,
                ROW_NUMBER() OVER (ORDER BY total_amount DESC) as rank
            FROM orders
            WHERE order_date >= '2024-01-01'
        """,
        
        "no_partition_filter": """
            SELECT customer_id, SUM(total_amount)
            FROM orders
            GROUP BY customer_id
        """,
        
        "inefficient_aggregation": """
            SELECT 
                region,
                COUNT(DISTINCT customer_id) as customers,
                AVG(order_amount) as avg_order
            FROM large_orders_table
            WHERE order_date BETWEEN '2023-01-01' AND '2024-12-31'
            GROUP BY region
        """
    }


@pytest.fixture
def expected_optimizations() -> Dict[str, Dict[str, Any]]:
    """Expected optimization results for sample queries."""
    return {
        "select_star": {
            "patterns": ["column_pruning"],
            "min_optimizations": 1,
            "should_improve": True
        },
        
        "complex_join": {
            "patterns": ["join_reordering", "predicate_pushdown"],
            "min_optimizations": 1,
            "should_improve": True
        },
        
        "subquery_exists": {
            "patterns": ["subquery_to_join"],
            "min_optimizations": 1,
            "should_improve": True
        },
        
        "count_distinct": {
            "patterns": ["approximate_aggregation"],
            "min_optimizations": 1,
            "should_improve": True
        },
        
        "window_function": {
            "patterns": ["window_optimization"],
            "min_optimizations": 0,  # May not always need optimization
            "should_improve": False
        },
        
        "no_partition_filter": {
            "patterns": ["partition_filtering"],
            "min_optimizations": 1,
            "should_improve": True
        }
    }


@pytest.fixture
def mock_gemini_response() -> Dict[str, Any]:
    """Mock response from Gemini API."""
    return {
        "optimized_query": """
            SELECT customer_id, order_date, total_amount
            FROM orders
            WHERE _PARTITIONDATE >= '2024-01-01'
            AND order_date >= '2024-01-01'
        """,
        "optimizations_applied": [
            {
                "pattern_id": "partition_filtering",
                "pattern_name": "Partition Filtering",
                "description": "Added partition filter to reduce data scanned",
                "before_snippet": "WHERE order_date >= '2024-01-01'",
                "after_snippet": "WHERE _PARTITIONDATE >= '2024-01-01' AND order_date >= '2024-01-01'",
                "expected_improvement": 0.5,
                "confidence_score": 0.9
            }
        ],
        "estimated_improvement": 0.5,
        "explanation": "Added partition filtering to reduce data scanning"
    }


@pytest.fixture
def test_query_analysis() -> QueryAnalysis:
    """Sample query analysis for testing."""
    return QueryAnalysis(
        original_query="SELECT * FROM table WHERE date > '2024-01-01'",
        query_hash="test_hash",
        complexity="moderate",
        table_count=1,
        join_count=0,
        subquery_count=0,
        window_function_count=0,
        aggregate_function_count=0,
        has_partition_filter=False,
        has_clustering_filter=True,
        potential_issues=["Using SELECT *", "Missing partition filter"],
        applicable_patterns=["column_pruning", "partition_filtering"]
    )


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment."""
    # Create test directories
    os.makedirs("tests/data/documentation", exist_ok=True)
    os.makedirs("tests/data/vector_db", exist_ok=True)
    os.makedirs("tests/data/queries", exist_ok=True)
    
    yield
    
    # Cleanup is handled by pytest-tmp-path


@pytest.fixture
def integration_test_queries() -> Dict[str, str]:
    """Queries specifically for integration testing."""
    return {
        "performance_test": """
            SELECT 
                customer_id,
                COUNT(*) as order_count,
                SUM(total_amount) as total_spent,
                AVG(total_amount) as avg_order
            FROM orders
            WHERE order_date >= '2024-01-01'
            GROUP BY customer_id
            HAVING COUNT(*) > 5
            ORDER BY total_spent DESC
            LIMIT 100
        """,
        
        "validation_test": """
            SELECT DISTINCT
                p.category,
                COUNT(o.order_id) as total_orders
            FROM products p
            LEFT JOIN order_items oi ON p.product_id = oi.product_id
            LEFT JOIN orders o ON oi.order_id = o.order_id
            WHERE o.order_date >= '2024-01-01' 
            OR o.order_date IS NULL
            GROUP BY p.category
        """
    }


# Pytest markers for different test categories
pytest.mark.unit = pytest.mark.unit
pytest.mark.integration = pytest.mark.integration  
pytest.mark.performance = pytest.mark.performance
pytest.mark.slow = pytest.mark.slow