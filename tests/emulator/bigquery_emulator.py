"""
BigQuery emulator for testing optimization patterns without real BigQuery connection.
Provides realistic query execution simulation for comprehensive testing.
"""

import re
import time
import hashlib
from typing import Dict, List, Any, Optional
from unittest.mock import Mock


class BigQueryEmulator:
    """
    Mock BigQuery emulator that simulates realistic query execution
    for testing optimization patterns without requiring actual BigQuery connection.
    """
    
    def __init__(self):
        # Define mock table schemas and metadata
        self.tables = {
            "customers": {
                "schema": ["customer_id", "customer_name", "customer_tier", "region", "signup_date"],
                "rows": 1000,
                "partitioned": False,
                "partition_field": None,
                "clustered": ["customer_id"],
                "size_bytes": 50000
            },
            "orders": {
                "schema": ["order_id", "customer_id", "order_date", "total_amount", "status", "product_id"],
                "rows": 50000,
                "partitioned": True,
                "partition_field": "order_date",
                "clustered": ["customer_id", "status"],
                "size_bytes": 5000000
            },
            "products": {
                "schema": ["product_id", "product_name", "category", "price"],
                "rows": 50,
                "partitioned": False,
                "partition_field": None,
                "clustered": [],
                "size_bytes": 5000
            },
            "order_items": {
                "schema": ["item_id", "order_id", "product_id", "quantity", "unit_price", "order_date"],
                "rows": 100000,
                "partitioned": True,
                "partition_field": "order_date",
                "clustered": ["order_id"],
                "size_bytes": 10000000
            },
            "large_table": {
                "schema": ["id", "name", "value", "date_column", "category"],
                "rows": 10000000,
                "partitioned": True,
                "partition_field": "date_column",
                "clustered": ["id", "category"],
                "size_bytes": 1000000000
            },
            "small_table": {
                "schema": ["id", "name", "value"],
                "rows": 100,
                "partitioned": False,
                "partition_field": None,
                "clustered": ["id"],
                "size_bytes": 1000
            }
        }
        
        # Sample data for different query types
        self.sample_data = {
            "customers": [
                {"customer_id": 1, "customer_name": "Customer_1", "customer_tier": "Gold", "region": "US-East", "signup_date": "2020-01-02"},
                {"customer_id": 2, "customer_name": "Customer_2", "customer_tier": "Silver", "region": "US-West", "signup_date": "2020-01-03"},
                {"customer_id": 3, "customer_name": "Customer_3", "customer_tier": "Bronze", "region": "Europe", "signup_date": "2020-01-04"}
            ],
            "orders": [
                {"order_id": 1, "customer_id": 1, "order_date": "2024-01-01", "total_amount": 150.75, "status": "completed", "product_id": 1},
                {"order_id": 2, "customer_id": 2, "order_date": "2024-01-02", "total_amount": 89.50, "status": "processing", "product_id": 2},
                {"order_id": 3, "customer_id": 3, "order_date": "2024-01-03", "total_amount": 234.99, "status": "completed", "product_id": 3}
            ],
            "products": [
                {"product_id": 1, "product_name": "Product_1", "category": "Electronics", "price": 125.50},
                {"product_id": 2, "product_name": "Product_2", "category": "Books", "price": 89.25},
                {"product_id": 3, "product_name": "Product_3", "category": "Home", "price": 234.75}
            ],
            "order_items": [
                {"item_id": 1, "order_id": 1, "product_id": 1, "quantity": 2, "unit_price": 75.38, "order_date": "2024-01-01"},
                {"item_id": 2, "order_id": 2, "product_id": 2, "quantity": 1, "unit_price": 89.25, "order_date": "2024-01-02"},
                {"item_id": 3, "order_id": 3, "product_id": 3, "quantity": 1, "unit_price": 234.99, "order_date": "2024-01-03"}
            ]
        }
    
    def execute_query(self, query: str, dry_run: bool = False) -> Dict[str, Any]:
        """Simulate BigQuery query execution with realistic results."""
        
        # Simulate execution time based on query complexity
        execution_time = self._calculate_execution_time(query)
        bytes_processed = self._calculate_bytes_processed(query)
        
        if dry_run:
            return {
                "success": True,
                "dry_run": True,
                "performance": Mock(
                    execution_time_ms=execution_time,
                    bytes_processed=bytes_processed,
                    cache_hit=False
                ),
                "results": None,
                "row_count": None
            }
        
        # Generate realistic results based on query type
        results = self._generate_query_results(query)
        
        return {
            "success": True,
            "dry_run": False,
            "performance": Mock(
                execution_time_ms=execution_time,
                bytes_processed=bytes_processed,
                cache_hit=False
            ),
            "results": results,
            "row_count": len(results)
        }
    
    def get_table_info(self, table_id: str) -> Dict[str, Any]:
        """Get mock table metadata."""
        table_name = table_id.split('.')[-1]
        
        if table_name in self.tables:
            table_data = self.tables[table_name]
            return {
                "table_id": table_name,
                "num_rows": table_data["rows"],
                "num_bytes": table_data["size_bytes"],
                "partitioning": {
                    "type": "DAY" if table_data["partitioned"] else None,
                    "field": table_data["partition_field"]
                },
                "clustering": {
                    "fields": table_data["clustered"]
                },
                "schema": [
                    {"name": col, "type": "STRING", "mode": "NULLABLE"}
                    for col in table_data["schema"]
                ]
            }
        
        return {"error": f"Table {table_name} not found"}
    
    def validate_query(self, query: str) -> Dict[str, Any]:
        """Validate query syntax."""
        # Simple validation - check for basic SQL keywords
        query_upper = query.upper()
        
        if not query_upper.strip().startswith('SELECT'):
            return {
                "valid": False,
                "error": "Query must start with SELECT",
                "bytes_processed": None
            }
        
        if 'FROM' not in query_upper:
            return {
                "valid": False,
                "error": "Query must include FROM clause",
                "bytes_processed": None
            }
        
        return {
            "valid": True,
            "bytes_processed": self._calculate_bytes_processed(query),
            "estimated_cost": 0.005,
            "error": None
        }
    
    def test_connection(self) -> bool:
        """Mock connection test."""
        return True
    
    def _calculate_execution_time(self, query: str) -> int:
        """Calculate realistic execution time based on query complexity."""
        base_time = 500  # Base 500ms
        
        # Add time for different operations
        query_upper = query.upper()
        
        if "SELECT *" in query_upper:
            base_time += 200  # Extra time for full table scan
        
        join_count = len(re.findall(r'\bJOIN\b', query_upper))
        base_time += join_count * 300  # 300ms per JOIN
        
        if "COUNT(DISTINCT" in query_upper:
            base_time += 1000  # COUNT DISTINCT is expensive
        
        if "GROUP BY" in query_upper:
            base_time += 400  # Aggregation overhead
        
        if "ORDER BY" in query_upper:
            base_time += 300  # Sorting overhead
        
        # Simulate table size impact
        tables_referenced = self._extract_table_names(query)
        for table in tables_referenced:
            if table in self.tables:
                table_size = self.tables[table]["rows"]
                if table_size > 1000000:  # Large table
                    base_time += 500
                elif table_size > 10000:  # Medium table
                    base_time += 200
        
        return base_time
    
    def _calculate_bytes_processed(self, query: str) -> int:
        """Calculate bytes processed based on query and tables."""
        total_bytes = 0
        
        tables_referenced = self._extract_table_names(query)
        for table in tables_referenced:
            if table in self.tables:
                table_bytes = self.tables[table]["size_bytes"]
                
                # Reduce bytes if specific columns selected
                if "SELECT *" not in query.upper():
                    table_bytes = int(table_bytes * 0.6)  # Assume 40% reduction
                
                total_bytes += table_bytes
        
        return total_bytes or 1000000  # Default 1MB
    
    def _generate_query_results(self, query: str) -> List[Dict[str, Any]]:
        """Generate realistic query results based on query type."""
        query_upper = query.upper()
        
        # COUNT queries
        if "COUNT(" in query_upper:
            if "COUNT(DISTINCT" in query_upper:
                return [{"count": 1500}]
            else:
                return [{"count": 5000}]
        
        # Aggregation queries
        if "GROUP BY" in query_upper:
            if "region" in query.lower():
                return [
                    {"region": "US-East", "total": 15000, "count": 500},
                    {"region": "US-West", "total": 12000, "count": 400},
                    {"region": "Europe", "total": 8000, "count": 300}
                ]
            elif "customer_tier" in query.lower():
                return [
                    {"customer_tier": "Premium", "total": 25000, "count": 200},
                    {"customer_tier": "Gold", "total": 18000, "count": 300},
                    {"customer_tier": "Silver", "total": 12000, "count": 350}
                ]
            else:
                return [
                    {"group_key": "Group1", "total": 1000},
                    {"group_key": "Group2", "total": 1500}
                ]
        
        # JOIN queries
        if "JOIN" in query_upper:
            return [
                {"customer_name": "Customer_1", "order_id": 1, "total_amount": 150.50, "product_name": "Product_A"},
                {"customer_name": "Customer_2", "order_id": 2, "total_amount": 275.25, "product_name": "Product_B"},
                {"customer_name": "Customer_3", "order_id": 3, "total_amount": 89.75, "product_name": "Product_C"}
            ]
        
        # Window function queries
        if "OVER (" in query_upper:
            return [
                {"customer_id": 1, "order_date": "2024-01-01", "total_amount": 150.75, "rank": 1},
                {"customer_id": 2, "order_date": "2024-01-02", "total_amount": 275.25, "rank": 2},
                {"customer_id": 3, "order_date": "2024-01-03", "total_amount": 89.75, "rank": 3}
            ]
        
        # Simple SELECT queries
        table_name = self._extract_primary_table(query)
        if table_name and table_name in self.sample_data:
            return self.sample_data[table_name][:3]  # Return first 3 rows
        
        # Default result
        return [
            {"id": 1, "name": "Item1", "value": 100},
            {"id": 2, "name": "Item2", "value": 200},
            {"id": 3, "name": "Item3", "value": 300}
        ]
    
    def _extract_table_names(self, query: str) -> List[str]:
        """Extract table names from query."""
        # Simple regex to find table names
        patterns = [
            r'FROM\s+(\w+)',
            r'JOIN\s+(\w+)',
            r'FROM\s+`[^`]*\.([^`]+)`',
            r'JOIN\s+`[^`]*\.([^`]+)`'
        ]
        
        tables = set()
        for pattern in patterns:
            matches = re.findall(pattern, query, re.IGNORECASE)
            tables.update(matches)
        
        return list(tables)
    
    def _extract_primary_table(self, query: str) -> Optional[str]:
        """Extract the primary table from FROM clause."""
        match = re.search(r'FROM\s+(\w+)', query, re.IGNORECASE)
        if match:
            return match.group(1)
        return None