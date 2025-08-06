#!/usr/bin/env python3
"""
Convenient script to run BigQuery Optimizer tests.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from tests.test_runner import main

if __name__ == "__main__":
    main()