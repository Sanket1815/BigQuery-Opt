#!/usr/bin/env python3
"""
Debug script to understand why word boundary pattern is not working
"""

import re

def debug_word_boundary_issue():
    """Debug word boundary pattern issue"""
    
    query = "OR DER BY order_date DESC"
    print(f"Original: '{query}'")
    
    # Test different patterns
    patterns = [
        (r'\bOR\s+DER\s+BY\b', 'OR ORDER BY', 'Word boundaries with spaces'),
        (r'OR\s+DER\s+BY', 'OR ORDER BY', 'No word boundaries'),
        (r'OR\s+DER\s+BY(?=\s)', 'OR ORDER BY', 'Positive lookahead'),
        (r'(?<=\s)OR\s+DER\s+BY(?=\s)', 'OR ORDER BY', 'Positive lookbehind and lookahead'),
        (r'\bOR\s+DER\s+BY(?=\s)', 'OR ORDER BY', 'Word boundary start + lookahead'),
    ]
    
    for pattern, replacement, description in patterns:
        print(f"\nTesting: {description}")
        print(f"Pattern: {pattern}")
        print(f"Replacement: {replacement}")
        
        # Check if pattern matches
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            print(f"✅ Pattern matches: '{match.group()}'")
            
            # Apply replacement
            result = re.sub(pattern, replacement, query, flags=re.IGNORECASE)
            print(f"Result: '{result}'")
            
            # Check if DER BY is still present
            if 'DER BY' in result:
                print("❌ DER BY still present")
            else:
                print("✅ DER BY replaced")
                
            # Check if OR ORDER BY is present
            if 'OR ORDER BY' in result:
                print("✅ OR ORDER BY present")
            else:
                print("❌ OR ORDER BY not present")
        else:
            print("❌ Pattern does not match")
    
    # Test with the actual problematic context
    print("\n" + "="*60)
    context_query = "WINDOW w_desc AS (OR DER BY order_date DESC)"
    print(f"Context query: '{context_query}'")
    
    # Test the best pattern from above
    best_pattern = r'\bOR\s+DER\s+BY(?=\s)'
    best_replacement = 'OR ORDER BY'
    
    print(f"\nTesting best pattern in context:")
    print(f"Pattern: {best_pattern}")
    print(f"Replacement: {best_replacement}")
    
    # Check if pattern matches
    match = re.search(best_pattern, context_query, re.IGNORECASE)
    if match:
        print(f"✅ Pattern matches: '{match.group()}'")
        
        # Apply replacement
        result = re.sub(best_pattern, best_replacement, context_query, flags=re.IGNORECASE)
        print(f"Result: '{result}'")
        
        # Check if DER BY is still present
        if 'DER BY' in result:
            print("❌ DER BY still present")
        else:
            print("✅ DER BY replaced")
            
        # Check if OR ORDER BY is present
        if 'OR ORDER BY' in result:
            print("✅ OR ORDER BY present")
        else:
            print("❌ OR ORDER BY not present")
    else:
        print("❌ Pattern does not match")

if __name__ == "__main__":
    debug_word_boundary_issue() 