#!/usr/bin/env python3
"""
Test script to validate that optimized queries return IDENTICAL results.
This demonstrates the CRITICAL requirement that business logic must NEVER change.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.optimizer.query_optimizer import BigQueryOptimizer
from config.settings import get_settings


def test_query_validation():
    """Test that optimized queries return IDENTICAL results."""
    
    print("🧪 CRITICAL QUERY VALIDATION TEST")
    print("=" * 80)
    print("🎯 TESTING: Optimized queries MUST return IDENTICAL results")
    print("🚨 REQUIREMENT: Business logic must NEVER change!")
    print("📊 VALIDATION: Both query results will be shown side-by-side")
    print("=" * 80)
    
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
    
    # Test queries that MUST return identical results
    test_queries = [
        {
            "name": "Simple SELECT Test",
            "query": f"""
                SELECT customer_id, order_date, total_amount, status
                FROM `{project_id}.{dataset_id}.orders`
                WHERE order_date >= '2024-06-01'
                AND status = 'completed'
                ORDER BY customer_id, order_date
                LIMIT 10
            """,
            "description": "Should add _PARTITIONDATE filter while keeping IDENTICAL results"
        },
        {
            "name": "Aggregation Test",
            "query": f"""
                SELECT 
                    status,
                    COUNT(*) as order_count,
                    SUM(total_amount) as total_revenue,
                    AVG(total_amount) as avg_order_value
                FROM `{project_id}.{dataset_id}.orders`
                WHERE order_date >= '2024-06-01'
                GROUP BY status
                ORDER BY status
            """,
            "description": "Should add partition filter, aggregated results MUST be identical"
        },
        {
            "name": "JOIN Test",
            "query": f"""
                SELECT 
                    c.customer_name,
                    c.customer_tier,
                    o.order_id,
                    o.total_amount
                FROM `{project_id}.{dataset_id}.customers` c
                JOIN `{project_id}.{dataset_id}.orders` o ON c.customer_id = o.customer_id
                WHERE o.order_date >= '2024-06-01'
                AND c.customer_tier = 'Premium'
                ORDER BY o.order_id
                LIMIT 15
            """,
            "description": "Should optimize JOIN and add partition filter, results MUST be identical"
        },
        {
            "name": "Window Function Test",
            "query": f"""
                SELECT 
                    customer_id,
                    order_date,
                    total_amount,
                    ROW_NUMBER() OVER (ORDER BY total_amount DESC) as amount_rank
                FROM `{project_id}.{dataset_id}.orders`
                WHERE order_date >= '2024-06-01'
                ORDER BY amount_rank
                LIMIT 20
            """,
            "description": "Should optimize window function, rankings MUST be identical"
        },
        {
            "name": "Subquery Test",
            "query": f"""
                SELECT customer_id, customer_name
                FROM `{project_id}.{dataset_id}.customers` c
                WHERE EXISTS (
                    SELECT 1 FROM `{project_id}.{dataset_id}.orders` o 
                    WHERE o.customer_id = c.customer_id 
                    AND o.order_date >= '2024-06-01'
                    AND o.status = 'completed'
                )
                ORDER BY customer_id
                LIMIT 10
            """,
            "description": "Should convert EXISTS to JOIN, customer list MUST be identical"
        }
    ]
    
    all_passed = True
    
    for i, test_case in enumerate(test_queries, 1):
        print(f"\n" + "="*100)
        print(f"🧪 TEST {i}: {test_case['name']}")
        print(f"📝 Description: {test_case['description']}")
        print(f"🎯 Requirement: Results MUST be 100% identical")
        print("="*100)
        
        try:
            # Run optimization with validation - this will show both query results
            result = optimizer.optimize_query(
                test_case['query'],
                validate_results=True,
                measure_performance=False,  # Focus on correctness
                sample_size=50,  # Small sample for testing
                show_result_comparison=True
            )
            
            # Check if results are identical
            if result.results_identical:
                print(f"\n✅ TEST {i} PASSED: Results are IDENTICAL!")
                print(f"   ✅ Business logic preserved")
                print(f"   ✅ Optimizations applied: {result.total_optimizations}")
                if result.optimizations_applied:
                    for opt in result.optimizations_applied:
                        print(f"      - {opt.pattern_name}: {opt.description}")
            else:
                print(f"\n🚨 TEST {i} FAILED: Results are NOT identical!")
                print(f"   🚨 Business logic COMPROMISED!")
                print(f"   🚨 Error: {result.validation_error}")
                all_passed = False
                
        except Exception as e:
            print(f"\n❌ TEST {i} ERROR: {str(e)}")
            all_passed = False
    
    print("\n" + "="*100)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Business logic preservation VERIFIED")
        print("✅ All optimized queries return IDENTICAL results")
        print("✅ The optimization system is working correctly")
    else:
        print("🚨 CRITICAL FAILURE: SOME TESTS FAILED!")
        print("❌ Business logic preservation VIOLATED")
        print("❌ Optimized queries returned DIFFERENT results")
        print("❌ The optimization system needs fixing")
    
    print("="*100)
    return all_passed


if __name__ == "__main__":
    success = test_query_validation()
    sys.exit(0 if success else 1)