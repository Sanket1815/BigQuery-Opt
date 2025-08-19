#!/usr/bin/env python3
"""
Debug script to understand why OR DER BY is being fixed to OR OR ORDER BY
"""

import re

def debug_double_fix():
    """Debug the double fix issue"""
    
    query = "OR DER BY order_date DESC"
    print(f"Original: '{query}'")
    
    # Test the patterns step by step
    print("\nStep 1: Fix OR DER BY → OR ORDER BY")
    step1 = re.sub(r'OR DER BY', 'OR ORDER BY', query, flags=re.IGNORECASE)
    print(f"After step 1: '{step1}'")
    
    print("\nStep 2: Fix DER BY → ORDER BY")
    step2 = re.sub(r'DER BY', 'ORDER BY', step1, flags=re.IGNORECASE)
    print(f"After step 2: '{step2}'")
    
    print("\nStep 3: Fix missing spaces after OR")
    step3 = re.sub(r'OR([a-zA-Z_])', r'OR \1', step2, re.IGNORECASE)
    print(f"After step 3: '{step3}'")
    
    print("\nStep 4: Fix missing spaces after ORDER")
    step4 = re.sub(r'ORDER([a-zA-Z_])', r'ORDER \1', step3, re.IGNORECASE)
    print(f"After step 4: '{step4}'")
    
    # Test the full sequence
    print("\nFull sequence test:")
    full_query = "OR DER BY order_date DESC"
    print(f"Original: '{full_query}'")
    
    # Apply all fixes in order
    corrected = full_query
    corrected = re.sub(r'OR DER BY', 'OR ORDER BY', corrected, flags=re.IGNORECASE)
    corrected = re.sub(r'DER BY', 'ORDER BY', corrected, flags=re.IGNORECASE)
    corrected = re.sub(r'OR([a-zA-Z_])', r'OR \1', corrected, re.IGNORECASE)
    corrected = re.sub(r'ORDER([a-zA-Z_])', r'ORDER \1', corrected, re.IGNORECASE)
    
    print(f"Final: '{corrected}'")
    
    # Check if there are any remaining issues
    if 'OR OR' in corrected:
        print("❌ Found 'OR OR' - this indicates double replacement")
    else:
        print("✅ No 'OR OR' found")

if __name__ == "__main__":
    debug_double_fix() 