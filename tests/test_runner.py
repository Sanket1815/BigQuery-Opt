"""Test runner for BigQuery Optimizer with setup and teardown."""

import os
import sys
import pytest
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from config.settings import get_settings
from src.optimizer.bigquery_client import BigQueryClient


class TestRunner:
    """Test runner with BigQuery setup and teardown."""
    
    def __init__(self):
        self.settings = get_settings()
        self.bq_client = None
        
    def setup_test_environment(self):
        """Setup test environment and verify BigQuery connection."""
        print("🔧 Setting up test environment...")
        
        # Verify required environment variables
        required_vars = [
            'GOOGLE_CLOUD_PROJECT',
            'GOOGLE_APPLICATION_CREDENTIALS',
            'GEMINI_API_KEY'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
            print("\nPlease set the following environment variables:")
            print("export GOOGLE_CLOUD_PROJECT=your-project-id")
            print("export GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json")
            print("export GEMINI_API_KEY=your-gemini-api-key")
            return False
        
        # Test BigQuery connection
        try:
            self.bq_client = BigQueryClient()
            if not self.bq_client.test_connection():
                print("❌ Failed to connect to BigQuery")
                return False
            print("✅ BigQuery connection successful")
        except Exception as e:
            print(f"❌ BigQuery connection failed: {e}")
            return False
        
        print("✅ Test environment setup complete")
        return True
    
    def run_tests(self, test_type="all", verbose=False):
        """Run tests based on type."""
        
        if not self.setup_test_environment():
            return False
        
        # Define test commands
        test_commands = {
            "unit": [
                "tests/unit/",
                "-m", "unit",
                "-v" if verbose else ""
            ],
            "integration": [
                "tests/integration/",
                "-m", "integration",
                "-v" if verbose else "",
                "--tb=short"
            ],
            "performance": [
                "tests/integration/test_bigquery_sandbox.py::TestPerformanceBenchmarks",
                "-m", "performance",
                "-v" if verbose else "",
                "--tb=short"
            ],
            "sandbox": [
                "tests/integration/test_bigquery_sandbox.py::TestBigQuerySandboxIntegration",
                "-m", "requires_bigquery",
                "-v" if verbose else "",
                "--tb=short"
            ],
            "all": [
                "tests/",
                "-v" if verbose else "",
                "--tb=short"
            ]
        }
        
        if test_type not in test_commands:
            print(f"❌ Unknown test type: {test_type}")
            print(f"Available types: {', '.join(test_commands.keys())}")
            return False
        
        # Filter out empty strings
        cmd = [arg for arg in test_commands[test_type] if arg]
        
        print(f"🧪 Running {test_type} tests...")
        print(f"Command: pytest {' '.join(cmd)}")
        
        # Run pytest
        exit_code = pytest.main(cmd)
        
        if exit_code == 0:
            print(f"✅ All {test_type} tests passed!")
        else:
            print(f"❌ Some {test_type} tests failed (exit code: {exit_code})")
        
        return exit_code == 0
    
    def cleanup_test_data(self):
        """Clean up test data from BigQuery."""
        if not self.bq_client:
            return
        
        try:
            cleanup_sql = f"DROP SCHEMA IF EXISTS `{self.settings.google_cloud_project}.optimizer_test_dataset` CASCADE"
            result = self.bq_client.execute_query(cleanup_sql, dry_run=False)
            if result["success"]:
                print("🧹 Test data cleaned up successfully")
            else:
                print(f"⚠️ Failed to clean up test data: {result['error']}")
        except Exception as e:
            print(f"⚠️ Error during cleanup: {e}")


def main():
    """Main function for test runner."""
    parser = argparse.ArgumentParser(description="BigQuery Optimizer Test Runner")
    parser.add_argument(
        "--type", 
        choices=["unit", "integration", "performance", "sandbox", "all"],
        default="all",
        help="Type of tests to run"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--cleanup",
        action="store_true",
        help="Clean up test data after running tests"
    )
    parser.add_argument(
        "--setup-only",
        action="store_true",
        help="Only setup test environment, don't run tests"
    )
    
    args = parser.parse_args()
    
    runner = TestRunner()
    
    if args.setup_only:
        success = runner.setup_test_environment()
        sys.exit(0 if success else 1)
    
    # Run tests
    success = runner.run_tests(args.type, args.verbose)
    
    # Cleanup if requested
    if args.cleanup:
        runner.cleanup_test_data()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()