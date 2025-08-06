"""Tests for the web UI interface."""

import pytest
import json
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

from src.web_ui.app import create_app
from src.common.models import OptimizationResult, QueryAnalysis, AppliedOptimization


@pytest.fixture
def client():
    """Create test client."""
    app = create_app()
    return TestClient(app)


@pytest.fixture
def mock_optimization_result():
    """Mock optimization result for testing."""
    return OptimizationResult(
        original_query="SELECT * FROM orders WHERE date > '2024-01-01'",
        query_analysis=Mock(
            complexity="moderate",
            table_count=1,
            join_count=0,
            potential_issues=["Using SELECT *", "Missing partition filter"]
        ),
        optimized_query="SELECT order_id, customer_id FROM orders WHERE _PARTITIONDATE >= '2024-01-01' AND date > '2024-01-01'",
        optimizations_applied=[
            AppliedOptimization(
                pattern_id="column_pruning",
                pattern_name="Column Pruning",
                description="Replaced SELECT * with specific columns",
                before_snippet="SELECT *",
                after_snippet="SELECT order_id, customer_id",
                expected_improvement=0.2
            ),
            AppliedOptimization(
                pattern_id="partition_filtering",
                pattern_name="Partition Filtering",
                description="Added partition filter",
                before_snippet="WHERE date > '2024-01-01'",
                after_snippet="WHERE _PARTITIONDATE >= '2024-01-01' AND date > '2024-01-01'",
                expected_improvement=0.5
            )
        ],
        total_optimizations=2,
        estimated_improvement=0.6,
        results_identical=True
    )


class TestWebInterface:
    """Test web interface endpoints."""
    
    def test_home_page(self, client):
        """Test home page loads."""
        response = client.get("/")
        assert response.status_code == 200
        assert "BigQuery Query Optimizer" in response.text
    
    def test_health_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get("/api/health")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert "timestamp" in data
    
    @patch('src.optimizer.query_optimizer.BigQueryOptimizer')
    def test_optimize_query_endpoint(self, mock_optimizer_class, client, mock_optimization_result):
        """Test query optimization endpoint."""
        
        # Setup mock
        mock_optimizer = Mock()
        mock_optimizer.optimize_query.return_value = mock_optimization_result
        mock_optimizer_class.return_value = mock_optimizer
        
        # Test request
        response = client.post("/api/optimize", json={
            "query": "SELECT * FROM orders WHERE date > '2024-01-01'",
            "validate_results": True,
            "measure_performance": False
        })
        
        assert response.status_code == 200
        
        data = response.json()
        assert "optimized_query" in data
        assert "optimizations_applied" in data
        assert "total_optimizations" in data
        assert data["total_optimizations"] == 2
    
    @patch('src.optimizer.query_optimizer.BigQueryOptimizer')
    def test_analyze_query_endpoint(self, mock_optimizer_class, client):
        """Test query analysis endpoint."""
        
        # Setup mock
        mock_optimizer = Mock()
        mock_analysis = Mock(
            complexity="moderate",
            table_count=1,
            join_count=0,
            potential_issues=["Using SELECT *"],
            applicable_patterns=["column_pruning"]
        )
        mock_optimizer.analyze_query_only.return_value = mock_analysis
        mock_optimizer_class.return_value = mock_optimizer
        
        # Test request
        response = client.post("/api/analyze", json={
            "query": "SELECT * FROM orders"
        })
        
        assert response.status_code == 200
        
        data = response.json()
        assert "complexity" in data
        assert "potential_issues" in data
        assert "applicable_patterns" in data
    
    @patch('src.optimizer.query_optimizer.BigQueryOptimizer')
    def test_batch_optimize_endpoint(self, mock_optimizer_class, client, mock_optimization_result):
        """Test batch optimization endpoint."""
        
        # Setup mock
        mock_optimizer = Mock()
        mock_optimizer.batch_optimize_queries.return_value = [mock_optimization_result]
        mock_optimizer_class.return_value = mock_optimizer
        
        # Test request
        response = client.post("/api/batch-optimize", json={
            "queries": ["SELECT * FROM orders"],
            "validate_results": True
        })
        
        assert response.status_code == 200
        
        data = response.json()
        assert "results" in data
        assert len(data["results"]) == 1
    
    def test_invalid_query_handling(self, client):
        """Test handling of invalid queries."""
        response = client.post("/api/optimize", json={
            "query": "",  # Empty query
            "validate_results": False
        })
        
        assert response.status_code == 400
        
        data = response.json()
        assert "error" in data
    
    def test_missing_parameters(self, client):
        """Test handling of missing parameters."""
        response = client.post("/api/optimize", json={})
        
        assert response.status_code == 422  # Validation error
    
    @patch('src.optimizer.query_optimizer.BigQueryOptimizer')
    def test_optimization_error_handling(self, mock_optimizer_class, client):
        """Test handling of optimization errors."""
        
        # Setup mock to raise exception
        mock_optimizer = Mock()
        mock_optimizer.optimize_query.side_effect = Exception("Optimization failed")
        mock_optimizer_class.return_value = mock_optimizer
        
        response = client.post("/api/optimize", json={
            "query": "SELECT * FROM orders",
            "validate_results": False
        })
        
        assert response.status_code == 500
        
        data = response.json()
        assert "error" in data
        assert "Optimization failed" in data["error"]


class TestWebUIComponents:
    """Test web UI components and functionality."""
    
    def test_query_editor_component(self, client):
        """Test query editor component."""
        response = client.get("/")
        assert response.status_code == 200
        
        # Check for query editor elements
        assert 'id="query-editor"' in response.text
        assert 'class="sql-editor"' in response.text
    
    def test_results_display_component(self, client):
        """Test results display component."""
        response = client.get("/")
        assert response.status_code == 200
        
        # Check for results display elements
        assert 'id="results-container"' in response.text
        assert 'class="optimization-results"' in response.text
    
    def test_performance_metrics_component(self, client):
        """Test performance metrics component."""
        response = client.get("/")
        assert response.status_code == 200
        
        # Check for performance metrics elements
        assert 'class="performance-metrics"' in response.text
        assert 'id="performance-chart"' in response.text


if __name__ == "__main__":
    pytest.main([__file__, "-v"])