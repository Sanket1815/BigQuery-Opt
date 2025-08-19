#!/usr/bin/env python3
"""
Debug script to check for invisible characters or encoding issues
"""

import re

def debug_invisible_chars():
    """Debug invisible characters or encoding issues"""
    
    query = "OR DER BY order_date DESC"
    print(f"Original: '{query}'")
    print(f"Length: {len(query)}")
    print(f"Bytes: {query.encode()}")
    print(f"Hex: {query.encode().hex()}")
    
    # Apply the first fix: OR DER BY → OR ORDER BY
    step1 = re.sub(r'\bOR\s+DER\s+BY\b', 'OR ORDER BY', query, flags=re.IGNORECASE)
    print(f"\nStep 1 (OR DER BY → OR ORDER BY): '{step1}'")
    print(f"Length: {len(step1)}")
    print(f"Bytes: {step1.encode()}")
    print(f"Hex: {step1.encode().hex()}")
    
    # Check each character individually
    print("\nCharacter by character analysis of step1:")
    for i, char in enumerate(step1):
        print(f"Position {i}: '{char}' (ord: {ord(char)}, hex: {char.encode().hex()})")
    
    # Check for "OR OR" using string search
    if 'OR OR' in step1:
        print("\n❌ Found 'OR OR' using string search")
        pos = step1.find('OR OR')
        print(f"Position: {pos}")
        print(f"Context: '{step1[max(0, pos-10):pos+20]}'")
        
        # Check the characters around the match
        start = max(0, pos-5)
        end = min(len(step1), pos+10)
        print(f"Characters around match:")
        for i in range(start, end):
            char = step1[i]
            print(f"  {i}: '{char}' (ord: {ord(char)}, hex: {char.encode().hex()})")
    else:
        print("\n✅ No 'OR OR' found using string search")
    
    # Check for "OR ORDER" using string search
    if 'OR ORDER' in step1:
        print("\n✅ Found 'OR ORDER' using string search")
        pos = step1.find('OR ORDER')
        print(f"Position: {pos}")
        print(f"Context: '{step1[max(0, pos-10):pos+20]}'")
        
        # Check the characters around the match
        start = max(0, pos-5)
        end = min(len(step1), pos+15)
        print(f"Characters around match:")
        for i in range(start, end):
            char = step1[i]
            print(f"  {i}: '{char}' (ord: {ord(char)}, hex: {char.encode().hex()})")
    else:
        print("\n❌ No 'OR ORDER' found using string search")
    
    # Check if there's a bug in my logic
    print(f"\nDebugging my logic:")
    print(f"step1 = '{step1}'")
    print(f"'OR OR' in step1 = {'OR OR' in step1}")
    print(f"'OR ORDER' in step1 = {'OR ORDER' in step1}")
    
    # Check the exact substring
    if len(step1) >= 5:
        substring = step1[0:5]
        print(f"First 5 characters: '{substring}'")
        print(f"substring == 'OR OR' = {substring == 'OR OR'}")
        print(f"substring == 'OR OR' = {substring == 'OR OR'}")
        print(f"substring == 'OR OR' = {substring == 'OR OR'}")

if __name__ == "__main__":
    debug_invisible_chars() 