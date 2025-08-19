#!/usr/bin/env python3
"""
Very careful debug script to understand the string replacement
"""

import re

def debug_very_careful():
    """Debug the string replacement very carefully"""
    
    query = "OR DER BY order_date DESC"
    print(f"Original: '{query}'")
    print(f"Length: {len(query)}")
    print(f"Bytes: {query.encode()}")
    
    # Apply the first fix: OR DER BY → OR ORDER BY
    step1 = re.sub(r'\bOR\s+DER\s+BY\b', 'OR ORDER BY', query, flags=re.IGNORECASE)
    print(f"\nStep 1 (OR DER BY → OR ORDER BY): '{step1}'")
    print(f"Length: {len(step1)}")
    print(f"Bytes: {step1.encode()}")
    
    # Check if there are any remaining DER BY patterns
    remaining_der = re.findall(r'\bDER\s+BY\b', step1, re.IGNORECASE)
    print(f"Remaining DER BY patterns: {remaining_der}")
    
    # Check if there are any OR patterns
    or_patterns = re.findall(r'\bOR\b', step1, re.IGNORECASE)
    print(f"OR patterns found: {or_patterns}")
    
    # Check if there are any ORDER patterns
    order_patterns = re.findall(r'\bORDER\b', step1, re.IGNORECASE)
    print(f"ORDER patterns found: {order_patterns}")
    
    # Check if there are any BY patterns
    by_patterns = re.findall(r'\bBY\b', step1, re.IGNORECASE)
    print(f"BY patterns found: {by_patterns}")
    
    # Check for "OR OR" specifically
    or_or_pattern = re.findall(r'\bOR\s+OR\b', step1, re.IGNORECASE)
    print(f"'OR OR' patterns found: {or_or_pattern}")
    
    # Check for "OR ORDER" specifically
    or_order_pattern = re.findall(r'\bOR\s+ORDER\b', step1, re.IGNORECASE)
    print(f"'OR ORDER' patterns found: {or_order_pattern}")
    
    # Apply the second fix: DER BY → ORDER BY (should not match anything now)
    step2 = re.sub(r'\bDER\s+BY\b', 'ORDER BY', step1, flags=re.IGNORECASE)
    print(f"\nStep 2 (DER BY → ORDER BY): '{step2}'")
    print(f"Length: {len(step2)}")
    print(f"Bytes: {step2.encode()}")
    
    # Check for "OR OR" in step2
    or_or_pattern2 = re.findall(r'\bOR\s+OR\b', step2, re.IGNORECASE)
    print(f"'OR OR' patterns in step2: {or_or_pattern2}")
    
    # Check for "OR ORDER" in step2
    or_order_pattern2 = re.findall(r'\bOR\s+ORDER\b', step2, re.IGNORECASE)
    print(f"'OR ORDER' patterns in step2: {or_order_pattern2}")
    
    # Check if the result contains "OR OR" using string search
    if 'OR OR' in step2:
        print("❌ Found 'OR OR' using string search")
        # Find the position
        pos = step2.find('OR OR')
        print(f"Position: {pos}")
        print(f"Context: '{step2[max(0, pos-10):pos+20]}'")
    else:
        print("✅ No 'OR OR' found using string search")
    
    # Check if the result contains "OR ORDER" using string search
    if 'OR ORDER' in step2:
        print("✅ Found 'OR ORDER' using string search")
        # Find the position
        pos = step2.find('OR ORDER')
        print(f"Position: {pos}")
        print(f"Context: '{step2[max(0, pos-10):pos+20]}'")
    else:
        print("❌ No 'OR ORDER' found using string search")

if __name__ == "__main__":
    debug_very_careful() 