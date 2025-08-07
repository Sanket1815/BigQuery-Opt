#!/usr/bin/env python3
"""
Test script for dynamic query optimization with actual result validation.
Users can input any SQL query and see both original and optimized results.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.optimizer.query_optimizer import BigQueryOptimizer
from config.settings import get_settings


def test_dynamic_optimization():
    """Test dynamic query optimization with user input."""
    
    print("🚀 DYNAMIC BIGQUERY QUERY OPTIMIZER TEST")
    print("=" * 80)
    print("🎯 TESTING: Dynamic optimization with IDENTICAL results requirement")
    print("📊 FEATURE: Shows actual results from both queries side-by-side")
    print("🔧 PATTERNS: All optimization patterns applied dynamically")
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
        
        print(f"✅ Connected to project: {project_id}")
        print(f"📊 Using dataset: {dataset_id}")
        
    except Exception as e:
        print(f"❌ Failed to initialize optimizer: {e}")
        return False
    
    # Example test queries that users can try
    example_queries = [
        {
            "name": "SELECT * Column Pruning",
            "query": f"SELECT * FROM `{project_id}.{dataset_id}.orders` WHERE order_date >= '2024-06-01' LIMIT 10",
            "expected": "Should replace SELECT * with specific columns"
        },
        {
            "name": "EXISTS Subquery to JOIN",
            "query": f"SELECT customer_name FROM `{project_id}.{dataset_id}.customers` c WHERE EXISTS (SELECT 1 FROM `{project_id}.{dataset_id}.orders` o WHERE o.customer_id = c.customer_id AND o.order_date >= '2024-06-01') LIMIT 10",
            "expected": "Should convert EXISTS to INNER JOIN"
        },
        {
            "name": "COUNT DISTINCT to Approximate",
            "query": f"SELECT DATE(order_date) as day, COUNT(DISTINCT customer_id) as unique_customers FROM `{project_id}.{dataset_id}.orders` WHERE order_date >= '2024-06-01' GROUP BY DATE(order_date) LIMIT 10",
            "expected": "Should use APPROX_COUNT_DISTINCT for better performance"
        },
        {
            "name": "JOIN Order Optimization",
            "query": f"SELECT c.customer_name, p.product_name FROM `{project_id}.{dataset_id}.orders` o JOIN `{project_id}.{dataset_id}.customers` c ON o.customer_id = c.customer_id JOIN `{project_id}.{dataset_id}.products` p ON o.product_id = p.product_id WHERE o.order_date >= '2024-06-01' LIMIT 10",
            "expected": "Should reorder JOINs for better performance"
        },
        {
            "name": "Correlated Subquery to Window Function",
            "query": f"SELECT customer_id, order_date, (SELECT COUNT(*) FROM `{project_id}.{dataset_id}.orders` o2 WHERE o2.customer_id = o1.customer_id AND o2.order_date <= o1.order_date) as order_sequence FROM `{project_id}.{dataset_id}.orders` o1 WHERE order_date >= '2024-06-01' LIMIT 10",
            "expected": "Should convert to ROW_NUMBER() window function"
        }
    ]
    
    print(f"\n📋 EXAMPLE QUERIES TO TEST:")
    for i, example in enumerate(example_queries, 1):
        print(f"\n{i}. {example['name']}")
        print(f"   Expected: {example['expected']}")
        print(f"   Query: {example['query']}")
    
    print(f"\n" + "=" * 80)
    print(f"🧪 INTERACTIVE TESTING")
    print(f"=" * 80)
    
    while True:
        print(f"\nOptions:")
        print(f"1. Test an example query (enter number 1-{len(example_queries)})")
        print(f"2. Enter your own SQL query")
        print(f"3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "3":
            print("👋 Goodbye!")
            break
        elif choice in [str(i) for i in range(1, len(example_queries) + 1)]:
            # Test example query
            example = example_queries[int(choice) - 1]
            print(f"\n🧪 Testing: {example['name']}")
            test_query = example['query']
        elif choice == "2":
            # Get user input
            print(f"\n📝 Enter your SQL query (press Enter twice to finish):")
            lines = []
            while True:
                line = input()
                if line.strip() == "" and lines:
                    break
                lines.append(line)
            test_query = "\n".join(lines).strip()
            
            if not test_query:
                print("❌ No query entered")
                continue
        else:
            print("❌ Invalid choice")
            continue
        
        # Run the optimization test
        print(f"\n" + "="*100)
        print(f"🚀 RUNNING DYNAMIC OPTIMIZATION TEST")
        print(f"="*100)
        
        try:
            # Run optimization with full validation and result display
            result = optimizer.optimize_query(
                test_query,
                validate_results=True,
                measure_performance=True,
                sample_size=50,  # Smaller sample for testing
                show_result_comparison=True,
                allow_approximate=True,  # Allow approximate functions
                max_variance_percent=2.0
            )
            
            # Display optimization summary
            print(f"\n📊 OPTIMIZATION SUMMARY:")
            print(f"   ✅ Optimizations applied: {result.total_optimizations}")
            
            if result.optimizations_applied:
                print(f"   🔧 Applied patterns:")
                for opt in result.optimizations_applied:
                    print(f"      - {opt.pattern_name}: {opt.description}")
            
            if result.estimated_improvement:
                print(f"   📈 Estimated improvement: {result.estimated_improvement:.1%}")
            
            if result.actual_improvement:
                print(f"   📊 Actual improvement: {result.actual_improvement:.1%}")
            
            # Show the optimized query
            print(f"\n🔧 OPTIMIZED QUERY:")
            print(f"```sql")
            print(result.optimized_query)
            print(f"```")
            
            # Validation status
            if result.results_identical:
                print(f"\n✅ VALIDATION: PASSED - Results are IDENTICAL!")
            else:
                print(f"\n🚨 VALIDATION: FAILED - Results are DIFFERENT!")
                if result.validation_error:
                    print(f"   Error: {result.validation_error}")
                    
        except Exception as e:
            print(f"\n❌ OPTIMIZATION FAILED: {str(e)}")
        
        print(f"\n" + "="*100)
        
        # Ask if user wants to continue
        continue_choice = input("\nDo you want to test another query? (y/n): ").strip().lower()
        if continue_choice not in ['y', 'yes']:
            break
    
    return True


if __name__ == "__main__":
    success = test_dynamic_optimization()
    sys.exit(0 if success else 1)