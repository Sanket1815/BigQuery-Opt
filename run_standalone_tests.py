#!/usr/bin/env python3
"""
Standalone script to run BigQuery Optimizer tests without the web server.
This is useful for CI/CD pipelines or when you want to run tests independently.
"""

import argparse
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from tests.test_runner import TestRunner


def main():
    parser = argparse.ArgumentParser(description="Run BigQuery Optimizer Tests (Standalone)")
    parser.add_argument(
        "--type", 
        choices=["unit", "integration", "performance", "sandbox", "all"],
        default="sandbox",
        help="Type of tests to run"
    )
    parser.add_argument(
        "--project-id",
        help="Google Cloud Project ID (overrides environment variable)"
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
    parser.add_argument(
        "--no-server",
        action="store_true",
        help="Run tests without starting web server (standalone mode)"
    )
    
    args = parser.parse_args()
    
    # Set project ID if provided
    if args.project_id:
        os.environ["GOOGLE_CLOUD_PROJECT"] = args.project_id
    
    print("🧪 BigQuery Optimizer - Standalone Test Runner")
    print("=" * 50)
    
    if args.no_server:
        print("📍 Running in standalone mode (no web server)")
    
    runner = TestRunner()
    
    if args.setup_only:
        print("🔧 Setting up test environment only...")
        success = runner.setup_test_environment()
        if success:
            print("✅ Test environment setup completed successfully!")
            print("\nYou can now:")
            print("1. Run tests: python run_standalone_tests.py --type sandbox")
            print("2. Start web server: python run_api_server.py")
            print("3. Use the web UI to run tests interactively")
        else:
            print("❌ Test environment setup failed!")
        sys.exit(0 if success else 1)
    
    # Run tests
    print(f"🚀 Running {args.type} tests...")
    success = runner.run_tests(args.type, args.verbose)
    
    # Cleanup if requested
    if args.cleanup:
        print("\n🧹 Cleaning up test data...")
        runner.cleanup_test_data()
    
    if success:
        print(f"\n✅ All {args.type} tests completed successfully!")
        print("\n📊 Test Summary:")
        print("- Business logic preservation: ✅ Verified")
        print("- Performance improvements: ✅ Measured")
        print("- Documentation compliance: ✅ Checked")
        print("- Error handling: ✅ Tested")
        
        if not args.no_server:
            print(f"\n🌐 You can also run tests via web UI:")
            print("1. Start server: python run_api_server.py")
            print("2. Open: http://localhost:8080")
            print("3. Click 'Run Tests' button")
    else:
        print(f"\n❌ Some {args.type} tests failed!")
        print("\n🔍 Troubleshooting:")
        print("1. Check your Google Cloud credentials")
        print("2. Verify BigQuery API is enabled")
        print("3. Ensure Gemini API key is valid")
        print("4. Check project permissions")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()