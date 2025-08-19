#!/usr/bin/env python3
"""
Debug script to test word boundaries and pattern replacement
"""

import re

def debug_word_boundaries():
    """Debug word boundaries and pattern replacement"""
    
    query = "OR DER BY order_date DESC"
    print(f"Original: '{query}'")
    
    # Test with word boundaries
    print("\nTesting with word boundaries:")
    pattern1 = r'\bOR\s+DER\s+BY\b'
    replacement1 = 'OR ORDER BY'
    
    print(f"Pattern 1: {pattern1}")
    print(f"Replacement 1: {replacement1}")
    
    # Check if pattern matches
    match1 = re.search(pattern1, query, re.IGNORECASE)
    if match1:
        print(f"✅ Pattern 1 matches: '{match1.group()}'")
    else:
        print("❌ Pattern 1 does not match")
    
    # Apply replacement
    result1 = re.sub(pattern1, replacement1, query, flags=re.IGNORECASE)
    print(f"After replacement 1: '{result1}'")
    
    # Test the second pattern
    print("\nTesting second pattern:")
    pattern2 = r'\bDER\s+BY\b'
    replacement2 = 'ORDER BY'
    
    print(f"Pattern 2: {pattern2}")
    print(f"Replacement 2: {replacement2}")
    
    # Check if pattern matches the original
    match2_orig = re.search(pattern2, query, re.IGNORECASE)
    if match2_orig:
        print(f"✅ Pattern 2 matches original: '{match2_orig.group()}'")
    else:
        print("❌ Pattern 2 does not match original")
    
    # Check if pattern matches the result from first replacement
    match2_result = re.search(pattern2, result1, re.IGNORECASE)
    if match2_result:
        print(f"✅ Pattern 2 matches result: '{match2_result.group()}'")
    else:
        print("❌ Pattern 2 does not match result")
    
    # Apply second replacement
    result2 = re.sub(pattern2, replacement2, result1, flags=re.IGNORECASE)
    print(f"After replacement 2: '{result2}'")
    
    # Test the actual method call
    print("\nTesting the actual method:")
    try:
        from mcp_server.handlers import DirectSQLOptimizationHandler
        handler = DirectSQLOptimizationHandler()
        
        # Test with just the problematic part
        test_query = "OR DER BY order_date DESC"
        corrected = handler._validate_and_fix_syntax(test_query)
        print(f"Method result: '{corrected}'")
        
    except Exception as e:
        print(f"Error calling method: {e}")

if __name__ == "__main__":
    debug_word_boundaries() 