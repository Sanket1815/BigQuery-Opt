#!/usr/bin/env python3
"""
Test the new LLM cleanup functionality for syntax issues
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mcp_server.handlers import DirectSQLOptimizationHandler

def test_llm_cleanup():
    """Test the LLM cleanup functionality"""
    
    print("🧹 Testing LLM Cleanup Functionality")
    print("=" * 60)
    
    handler = DirectSQLOptimizationHandler()
    
    # Test case 1: Query with syntax issues
    problematic_query = """SELECT item_id, order_date, quantity, unit_price, ROW_NUMBER() OVER (w_desc) AS rn_global, SUM(quantity) OVER (w_asc) AS qty_running_global FROM `gen-lang-client-0064110488.optimizer_test_dataset.order_items` WHEREder_date >= '2024-02-01' WINDOW w_desc AS (OR DER BY order_date DESC), w_asc AS (OR DER BY order_date)"""
    
    print(f"Test Case 1: Query with syntax issues")
    print(f"Original: '{problematic_query}'")
    print()
    
    # Test the LLM cleanup directly
    validation_issues = [
        "Missing space after WHERE (WHEREder_date)",
        "Malformed OR DER BY (should be OR ORDER BY)",
        "Missing spaces around keywords"
    ]
    
    print("Sending to LLM for cleanup...")
    cleaned_query = handler._send_to_llm_for_cleanup(problematic_query, validation_issues)
    
    print(f"Cleaned query: '{cleaned_query}'")
    print()
    
    # Check if the issues were fixed
    issues_fixed = []
    
    if "WHEREder_date" not in cleaned_query and "WHERE der_date" in cleaned_query:
        issues_fixed.append("✅ WHEREder_date → WHERE der_date")
    else:
        issues_fixed.append("❌ WHEREder_date issue not fixed")
    
    if "OR DER BY" not in cleaned_query and "OR ORDER BY" in cleaned_query:
        issues_fixed.append("✅ OR DER BY → OR ORDER BY")
    else:
        issues_fixed.append("❌ OR DER BY issue not fixed")
    
    print("Issues fixed by LLM:")
    for issue in issues_fixed:
        print(f"  {issue}")
    
    print()
    
    # Test case 2: Query with NULL columns
    null_column_query = """SELECT NULL, NULL, NULL FROM `gen-lang-client-0064110488.optimizer_test_dataset.customers` AS c JOIN `gen-lang-client-0064110488.optimizer_test_dataset.orders` AS o ON c.customer_id = o.customer_id WHERE NULL >= '2024-01-01'"""
    
    print(f"Test Case 2: Query with NULL columns")
    print(f"Original: '{null_column_query}'")
    print()
    
    null_validation_issues = [
        "NULL columns in SELECT clause",
        "Invalid WHERE condition with NULL"
    ]
    
    print("Sending to LLM for cleanup...")
    cleaned_null_query = handler._send_to_llm_for_cleanup(null_column_query, null_validation_issues)
    
    print(f"Cleaned query: '{cleaned_null_query}'")
    print()
    
    # Check if NULL issues were fixed
    null_issues_fixed = []
    
    if "SELECT NULL, NULL, NULL" not in cleaned_null_query:
        null_issues_fixed.append("✅ NULL columns removed from SELECT")
    else:
        null_issues_fixed.append("❌ NULL columns still present in SELECT")
    
    if "WHERE NULL >=" not in cleaned_null_query:
        null_issues_fixed.append("✅ Invalid NULL WHERE condition fixed")
    else:
        null_issues_fixed.append("❌ Invalid NULL WHERE condition still present")
    
    print("NULL issues fixed by LLM:")
    for issue in null_issues_fixed:
        print(f"  {issue}")
    
    print()
    
    # Test case 3: Query with corrupted text
    corrupted_query = """SELECT * FROM orders WHERE quantity >= 2lectronics' LIMIT 100"""
    
    print(f"Test Case 3: Query with corrupted text")
    print(f"Original: '{corrupted_query}'")
    print()
    
    corrupted_validation_issues = [
        "Corrupted text in WHERE clause (2lectronics')",
        "Unbalanced quotes"
    ]
    
    print("Sending to LLM for cleanup...")
    cleaned_corrupted_query = handler._send_to_llm_for_cleanup(corrupted_query, corrupted_validation_issues)
    
    print(f"Cleaned query: '{cleaned_corrupted_query}'")
    print()
    
    # Check if corruption issues were fixed
    corruption_issues_fixed = []
    
    if "2lectronics'" not in cleaned_corrupted_query:
        corruption_issues_fixed.append("✅ Corrupted text fixed")
    else:
        corruption_issues_fixed.append("❌ Corrupted text still present")
    
    # Count quotes to check balance
    quote_count = cleaned_corrupted_query.count("'")
    if quote_count % 2 == 0:
        corruption_issues_fixed.append("✅ Quotes are balanced")
    else:
        corruption_issues_fixed.append("❌ Quotes are not balanced")
    
    print("Corruption issues fixed by LLM:")
    for issue in corruption_issues_fixed:
        print(f"  {issue}")
    
    return {
        "syntax_cleanup": cleaned_query,
        "null_cleanup": cleaned_null_query,
        "corruption_cleanup": cleaned_corrupted_query
    }

if __name__ == "__main__":
    test_llm_cleanup() 