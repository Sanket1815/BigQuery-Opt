#!/usr/bin/env python3
"""
Test script to validate that optimized queries return identical results.
This demonstrates the core requirement that business logic must never change.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.optimizer.query_optimizer import BigQueryOptimizer
from config.settings import get_settings


def test_query_validation():
    """Test that optimized queries return identical results."""
    
    print("🧪 QUERY VALIDATION TEST")
    print("=" * 60)
    print("Testing that optimized queries return IDENTICAL results to original queries")
    print("This is the core requirement - business logic must NEVER change!")
    print()
    
    # Initialize optimizer
    try:
        optimizer = BigQueryOptimizer(validate_results=True)
        settings = get_settings()
        
        if not settings.google_cloud_project:
            print("❌ Error: GOOGLE_CLOUD_PROJECT not set")
            return False
            
        project_id = settings.google_cloud_project
        dataset_id = "optimizer_test_dataset"
        
    except Exception as e:
        print(f"❌ Failed to initialize optimizer: {e}")
        return False
    
    # Test queries that should return identical results
    test_queries = [
        {
            "name": "Simple SELECT with WHERE clause",
            "query": f"""
                SELECT customer_id, order_date, total_amount, status
                FROM `{project_id}.{dataset_id}.orders`
                WHERE order_date >= '2024-06-01'
                AND status = 'completed'
                ORDER BY total_amount DESC
                LIMIT 10
            """,
            "description": "Should add partition filter and maintain exact same results"
        },
        {
            "name": "Aggregation query",
            "query": f"""
                SELECT 
                    status,
                    COUNT(*) as order_count,
                    SUM(total_amount) as total_revenue,
                    AVG(total_amount) as avg_order_value
                FROM `{project_id}.{dataset_id}.orders`
                WHERE order_date >= '2024-01-01'
                GROUP BY status
                ORDER BY total_revenue DESC
            """,
            "description": "Should add partition filter, results must be identical"
        },
        {
            "name": "JOIN query",
            "query": f"""
                SELECT 
                    c.customer_name,
                    c.customer_tier,
                    COUNT(o.order_id) as order_count,
                    SUM(o.total_amount) as total_spent
                FROM `{project_id}.{dataset_id}.customers` c
                JOIN `{project_id}.{dataset_id}.orders` o ON c.customer_id = o.customer_id
                WHERE o.order_date >= '2024-06-01'
                AND c.customer_tier IN ('Premium', 'Gold')
                GROUP BY c.customer_name, c.customer_tier
                ORDER BY total_spent DESC
                LIMIT 20
            """,
            "description": "Should optimize JOIN order and add partition filter"
        },
        {
            "name": "Window function query",
            "query": f"""
                SELECT 
                    customer_id,
                    order_date,
                    total_amount,
                    ROW_NUMBER() OVER (ORDER BY total_amount DESC) as amount_rank
                FROM `{project_id}.{dataset_id}.orders`
                WHERE order_date >= '2024-06-01'
                ORDER BY total_amount DESC
                LIMIT 50
            """,
            "description": "Should optimize window function and add partition filter"
        }
    ]
    
    all_passed = True
    
    for i, test_case in enumerate(test_queries, 1):
        print(f"\n🧪 TEST {i}: {test_case['name']}")
        print(f"📝 Description: {test_case['description']}")
        print("-" * 60)
        
        try:
            # Run optimization with validation
            result = optimizer.optimize_query(
                test_case['query'],
                validate_results=True,
                measure_performance=False,  # Focus on correctness
                sample_size=100,
                show_result_comparison=True
            )
            
            # Check if results are identical
            if result.results_identical:
                print(f"✅ TEST {i} PASSED: Results are identical")
                print(f"   Optimizations applied: {result.total_optimizations}")
                if result.optimizations_applied:
                    for opt in result.optimizations_applied:
                        print(f"   - {opt.pattern_name}: {opt.description}")
            else:
                print(f"❌ TEST {i} FAILED: Results are NOT identical")
                print(f"   Error: {result.validation_error}")
                all_passed = False
                
        except Exception as e:
            print(f"❌ TEST {i} ERROR: {str(e)}")
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Business logic preservation verified")
        print("✅ All optimized queries return identical results")
    else:
        print("❌ SOME TESTS FAILED!")
        print("⚠️  Business logic preservation violated")
        print("⚠️  Optimized queries returned different results")
    
    return all_passed


if __name__ == "__main__":
    success = test_query_validation()
    sys.exit(0 if success else 1)