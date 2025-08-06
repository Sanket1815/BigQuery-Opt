"""Comprehensive test runner for the test queries defined in comprehensive_test_queries.json."""

import json
import pytest
import time
from pathlib import Path
from typing import Dict, List, Any
from unittest.mock import patch

from src.optimizer.query_optimizer import BigQueryOptimizer
from src.optimizer.bigquery_client import BigQueryClient
from config.settings import get_settings


class TestComprehensiveQueries:
    """Test runner for comprehensive query optimization scenarios."""
    
    @classmethod
    def setup_class(cls):
        """Setup test environment."""
        cls.settings = get_settings()
        
        # Load test queries
        test_queries_file = Path(__file__).parent / "data" / "comprehensive_test_queries.json"
        with open(test_queries_file, 'r') as f:
            cls.test_data = json.load(f)
        
        # Initialize optimizer
        try:
            cls.optimizer = BigQueryOptimizer(validate_results=True)
            cls.bq_client = BigQueryClient()
        except Exception as e:
            pytest.skip(f"Failed to initialize BigQuery components: {str(e)}")
        
        # Replace placeholders in queries
        cls.project_id = cls.settings.google_cloud_project or "test-project"
        cls.dataset_id = "optimizer_test_dataset"
    
    def _replace_query_placeholders(self, query: str) -> str:
        """Replace placeholders in query with actual values."""
        return query.format(
            project=self.project_id,
            dataset=self.dataset_id
        )
    
    def _run_optimization_test(self, test_query: Dict[str, Any]) -> Dict[str, Any]:
        """Run optimization test for a single query."""
        
        print(f"\n🧪 Testing: {test_query['name']}")
        print(f"📝 Description: {test_query['description']}")
        print(f"🎯 Business Logic: {test_query['business_logic']}")
        
        # Replace placeholders
        original_query = self._replace_query_placeholders(test_query['original_query'])
        
        # Configure test parameters
        allow_approximate = test_query.get('allow_approximate', False)
        max_variance = test_query.get('max_variance_percent', 2.0)
        expected_min_improvement = test_query.get('expected_improvement_min', 0.15)
        
        start_time = time.time()
        
        # Run optimization with detailed results
        try:
            detailed_result = self.optimizer.optimize_query_with_detailed_results(
                original_query,
                validate_results=True,
                measure_performance=True,
                sample_size=100,  # Smaller sample for testing
                save_report=False
            )
            
            optimization_result = detailed_result["optimization_result"]
            
        except Exception as e:
            return {
                "test_id": test_query['id'],
                "success": False,
                "error": str(e),
                "execution_time": time.time() - start_time
            }
        
        # Analyze results
        test_result = {
            "test_id": test_query['id'],
            "test_name": test_query['name'],
            "success": True,
            "execution_time": time.time() - start_time,
            "optimizations_applied": optimization_result.total_optimizations,
            "results_identical": optimization_result.results_identical,
            "estimated_improvement": optimization_result.estimated_improvement,
            "actual_improvement": optimization_result.actual_improvement,
            "validation_error": optimization_result.validation_error,
            "expected_optimizations": test_query.get('expected_optimizations', []),
            "expected_min_improvement": expected_min_improvement,
            "allow_approximate": allow_approximate
        }
        
        # Check if expected optimizations were applied
        applied_patterns = [opt.pattern_id.lower() for opt in optimization_result.optimizations_applied]
        expected_patterns = [pattern.lower() for pattern in test_query.get('expected_optimizations', [])]
        
        patterns_found = []
        for expected in expected_patterns:
            if any(expected in applied for applied in applied_patterns):
                patterns_found.append(expected)
        
        test_result["patterns_found"] = patterns_found
        test_result["patterns_missing"] = [p for p in expected_patterns if p not in patterns_found]
        
        # Validate business logic preservation
        if not optimization_result.results_identical and not allow_approximate:
            test_result["success"] = False
            test_result["failure_reason"] = "Business logic changed - results not identical"
        
        # Check performance improvement
        if optimization_result.actual_improvement:
            meets_improvement_threshold = optimization_result.actual_improvement >= expected_min_improvement
            test_result["meets_improvement_threshold"] = meets_improvement_threshold
            if not meets_improvement_threshold:
                print(f"⚠️ Performance improvement {optimization_result.actual_improvement:.1%} below expected {expected_min_improvement:.1%}")
        
        # Display results
        if test_result["success"]:
            print(f"✅ Test passed: {optimization_result.total_optimizations} optimizations applied")
            if optimization_result.actual_improvement:
                print(f"📈 Performance improvement: {optimization_result.actual_improvement:.1%}")
            print(f"🔍 Results identical: {optimization_result.results_identical}")
        else:
            print(f"❌ Test failed: {test_result.get('failure_reason', 'Unknown error')}")
        
        return test_result
    
    @pytest.mark.parametrize("category", [
        "basic_optimizations",
        "join_optimizations", 
        "subquery_optimizations",
        "window_function_optimizations",
        "aggregation_optimizations",
        "complex_scenarios"
    ])
    def test_query_category(self, category: str):
        """Test all queries in a specific category."""
        
        if category not in self.test_data["test_categories"]:
            pytest.skip(f"Category {category} not found in test data")
        
        category_data = self.test_data["test_categories"][category]
        queries = category_data["queries"]
        
        print(f"\n🏷️ Testing category: {category}")
        print(f"📋 Description: {category_data['description']}")
        print(f"🔢 Number of queries: {len(queries)}")
        
        results = []
        
        for query in queries:
            result = self._run_optimization_test(query)
            results.append(result)
        
        # Analyze category results
        successful_tests = [r for r in results if r["success"]]
        failed_tests = [r for r in results if not r["success"]]
        
        print(f"\n📊 Category {category} Results:")
        print(f"   ✅ Passed: {len(successful_tests)}/{len(results)}")
        print(f"   ❌ Failed: {len(failed_tests)}/{len(results)}")
        
        if failed_tests:
            print("   Failed tests:")
            for failed in failed_tests:
                print(f"     - {failed['test_name']}: {failed.get('failure_reason', failed.get('error', 'Unknown'))}")
        
        # Assert that at least 80% of tests in category pass
        success_rate = len(successful_tests) / len(results)
        assert success_rate >= 0.8, f"Category {category} success rate {success_rate:.1%} below 80%"
    
    def test_business_logic_preservation(self):
        """Comprehensive test to ensure business logic is never changed."""
        
        print("\n🔒 Testing Business Logic Preservation")
        print("=" * 60)
        
        all_queries = []
        for category_data in self.test_data["test_categories"].values():
            all_queries.extend(category_data["queries"])
        
        failed_business_logic = []
        
        for query in all_queries:
            if query.get('allow_approximate', False):
                continue  # Skip approximate queries for strict business logic test
            
            result = self._run_optimization_test(query)
            
            if not result["results_identical"]:
                failed_business_logic.append({
                    "query_id": query["id"],
                    "query_name": query["name"],
                    "business_logic": query["business_logic"],
                    "error": result.get("validation_error", "Results not identical")
                })
        
        if failed_business_logic:
            print(f"\n❌ Business logic preservation failed for {len(failed_business_logic)} queries:")
            for failure in failed_business_logic:
                print(f"   - {failure['query_name']}: {failure['error']}")
        
        # Business logic preservation is critical - no failures allowed
        assert len(failed_business_logic) == 0, f"Business logic changed in {len(failed_business_logic)} queries"
        
        print(f"✅ Business logic preserved in all {len(all_queries)} test queries")
    
    def test_performance_improvements(self):
        """Test that optimizations provide meaningful performance improvements."""
        
        print("\n📈 Testing Performance Improvements")
        print("=" * 60)
        
        all_queries = []
        for category_data in self.test_data["test_categories"].values():
            all_queries.extend(category_data["queries"])
        
        performance_results = []
        
        for query in all_queries:
            result = self._run_optimization_test(query)
            
            if result["success"] and result["actual_improvement"] is not None:
                performance_results.append({
                    "query_name": query["name"],
                    "actual_improvement": result["actual_improvement"],
                    "expected_min": result["expected_min_improvement"],
                    "meets_threshold": result.get("meets_improvement_threshold", False)
                })
        
        if performance_results:
            avg_improvement = sum(r["actual_improvement"] for r in performance_results) / len(performance_results)
            threshold_met_count = sum(1 for r in performance_results if r["meets_threshold"])
            threshold_met_rate = threshold_met_count / len(performance_results)
            
            print(f"📊 Performance Results:")
            print(f"   Average improvement: {avg_improvement:.1%}")
            print(f"   Queries meeting threshold: {threshold_met_count}/{len(performance_results)} ({threshold_met_rate:.1%})")
            
            # At least 70% of queries should meet their improvement thresholds
            assert threshold_met_rate >= 0.7, f"Only {threshold_met_rate:.1%} of queries met improvement thresholds"
        else:
            print("⚠️ No performance measurements available")
    
    def test_optimization_pattern_coverage(self):
        """Test that all expected optimization patterns are being applied."""
        
        print("\n🎯 Testing Optimization Pattern Coverage")
        print("=" * 60)
        
        all_queries = []
        for category_data in self.test_data["test_categories"].values():
            all_queries.extend(category_data["queries"])
        
        pattern_coverage = {}
        
        for query in all_queries:
            result = self._run_optimization_test(query)
            
            if result["success"]:
                for expected_pattern in result["expected_optimizations"]:
                    if expected_pattern not in pattern_coverage:
                        pattern_coverage[expected_pattern] = {"expected": 0, "found": 0}
                    
                    pattern_coverage[expected_pattern]["expected"] += 1
                    
                    if expected_pattern.lower() in [p.lower() for p in result["patterns_found"]]:
                        pattern_coverage[expected_pattern]["found"] += 1
        
        print("📋 Pattern Coverage Results:")
        for pattern, stats in pattern_coverage.items():
            coverage_rate = stats["found"] / stats["expected"] if stats["expected"] > 0 else 0
            print(f"   {pattern}: {stats['found']}/{stats['expected']} ({coverage_rate:.1%})")
            
            # Each pattern should be found in at least 60% of expected cases
            assert coverage_rate >= 0.6, f"Pattern {pattern} coverage {coverage_rate:.1%} below 60%"


if __name__ == "__main__":
    # Run tests directly
    test_runner = TestComprehensiveQueries()
    test_runner.setup_class()
    
    print("🚀 Running Comprehensive Query Optimization Tests")
    print("=" * 80)
    
    # Test each category
    categories = [
        "basic_optimizations",
        "join_optimizations", 
        "subquery_optimizations",
        "window_function_optimizations",
        "aggregation_optimizations",
        "complex_scenarios"
    ]
    
    for category in categories:
        try:
            test_runner.test_query_category(category)
        except Exception as e:
            print(f"❌ Category {category} failed: {e}")
    
    # Run comprehensive tests
    try:
        test_runner.test_business_logic_preservation()
    except Exception as e:
        print(f"❌ Business logic preservation test failed: {e}")
    
    try:
        test_runner.test_performance_improvements()
    except Exception as e:
        print(f"❌ Performance improvement test failed: {e}")
    
    try:
        test_runner.test_optimization_pattern_coverage()
    except Exception as e:
        print(f"❌ Pattern coverage test failed: {e}")
    
    print("\n🎉 Comprehensive testing completed!")