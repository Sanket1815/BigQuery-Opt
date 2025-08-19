#!/usr/bin/env python3
"""
Debug script to understand why OR DER BY pattern is not being fixed
"""

import re

def debug_pattern_fix():
    """Debug the pattern replacement"""
    
    query = "OR DER BY order_date DESC"
    print(f"Original: '{query}'")
    
    # Test the pattern
    pattern = r'OR DER BY'
    replacement = 'OR ORDER BY'
    
    print(f"Pattern: {pattern}")
    print(f"Replacement: {replacement}")
    
    # Apply the fix
    fixed = re.sub(pattern, replacement, query, flags=re.IGNORECASE)
    print(f"After fix: '{fixed}'")
    
    # Test with the full query
    full_query = "WINDOW w_desc AS (OR DER BY order_date DESC), w_asc AS (OR DER BY order_date)"
    print(f"\nFull query: '{full_query}'")
    
    # Apply the fix
    fixed_full = re.sub(pattern, replacement, full_query, flags=re.IGNORECASE)
    print(f"After fix: '{fixed_full}'")
    
    # Test if there are any other patterns interfering
    print(f"\nChecking for other patterns that might interfere:")
    
    # Check if there are any other DER patterns
    der_patterns = re.findall(r'DER\s+BY', full_query, re.IGNORECASE)
    print(f"DER BY patterns found: {der_patterns}")
    
    # Check if there are any OR patterns
    or_patterns = re.findall(r'OR\s+DER', full_query, re.IGNORECASE)
    print(f"OR DER patterns found: {or_patterns}")

if __name__ == "__main__":
    debug_pattern_fix() 