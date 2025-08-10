"""
BigQuery Emulator for comprehensive testing without requiring actual BigQuery connection.
Provides realistic query execution simulation for all optimization patterns.
"""

import re
import json
import time
import hashlib
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import pandas as pd


@dataclass
class MockTable:
    """Mock table metadata for emulator."""
    name: str
    rows: int
    size_bytes: int
    partitioned: bool
    partition_field: Optional[str]
    clustered_fields: List[str]
    schema: List[Dict[str, str]]


@dataclass
class MockQueryResult:
    """Mock query execution result."""
    success: bool
    results: List[Dict[str, Any]]
    row_count: int
    execution_time_ms: int
    bytes_processed: int
    error: Optional[str] = None


class BigQueryEmulator:
    """
    Comprehensive BigQuery emulator for testing optimization patterns.
    Simulates realistic BigQuery behavior without requiring actual connection.
    """
    
    def __init__(self):
        self.tables = self._initialize_mock_tables()
        self.sample_data = self._generate_sample_data()
    
    def _initialize_mock_tables(self) -> Dict[str, MockTable]:
        """Initialize mock table metadata."""
        return {
            "customers": MockTable(
                name="customers",
                rows=1000,
                size_bytes=50000,
                partitioned=False,
                partition_field=None,
                clustered_fields=["customer_id"],
                schema=[
                    {"name": "customer_id", "type": "INTEGER"},
                    {"name": "customer_name", "type": "STRING"},
                    {"name": "customer_tier", "type": "STRING"},
                    {"name": "region", "type": "STRING"},
                    {"name": "signup_date", "type": "DATE"}
                ]
            ),
            "orders": MockTable(
                name="orders",
                rows=50000,
                size_bytes=5000000,
                partitioned=True,
                partition_field="order_date",
                clustered_fields=["customer_id", "status"],
                schema=[
                    {"name": "order_id", "type": "INTEGER"},
                    {"name": "customer_id", "type": "INTEGER"},
                    {"name": "order_date", "type": "DATE"},
                    {"name": "total_amount", "type": "FLOAT"},
                    {"name": "status", "type": "STRING"},
                    {"name": "product_id", "type": "INTEGER"}
                ]
            ),
            "products": MockTable(
                name="products",
                rows=50,
                size_bytes=5000,
                partitioned=False,
                partition_field=None,
                clustered_fields=[],
                schema=[
                    {"name": "product_id", "type": "INTEGER"},
                    {"name": "product_name", "type": "STRING"},
                    {"name": "category", "type": "STRING"},
                    {"name": "price", "type": "FLOAT"}
                ]
            ),
            "order_items": MockTable(
                name="order_items",
                rows=100000,
                size_bytes=10000000,
                partitioned=True,
                partition_field="order_date",
                clustered_fields=["order_id"],
                schema=[
                    {"name": "item_id", "type": "INTEGER"},
                    {"name": "order_id", "type": "INTEGER"},
                    {"name": "product_id", "type": "INTEGER"},
                    {"name": "quantity", "type": "INTEGER"},
                    {"name": "unit_price", "type": "FLOAT"},
                    {"name": "order_date", "type": "DATE"}
                ]
            ),
            "large_table": MockTable(
                name="large_table",
                rows=10000000,
                size_bytes=1000000000,
                partitioned=True,
                partition_field="date_column",
                clustered_fields=["id", "category"],
                schema=[
                    {"name": "id", "type": "INTEGER"},
                    {"name": "name", "type": "STRING"},
                    {"name": "value", "type": "FLOAT"},
                    {"name": "date_column", "type": "DATE"},
                    {"name": "category", "type": "STRING"}
                ]
            ),
            "small_table": MockTable(
                name="small_table",
                rows=100,
                size_bytes=1000,
                partitioned=False,
                partition_field=None,
                clustered_fields=["id"],
                schema=[
                    {"name": "id", "type": "INTEGER"},
                    {"name": "name", "type": "STRING"},
                    {"name": "value", "type": "FLOAT"}
                ]
            )
        }
    
    def _generate_sample_data(self) -> Dict[str, List[Dict]]:
        """Generate realistic sample data for each table."""
        return {
            "customers": [
                {"customer_id": 1, "customer_name": "Customer_1", "customer_tier": "Gold", "region": "US-East", "signup_date": "2020-01-01"},
                {"customer_id": 2, "customer_name": "Customer_2", "customer_tier": "Silver", "region": "US-West", "signup_date": "2020-01-02"},
                {"customer_id": 3, "customer_name": "Customer_3", "customer_tier": "Bronze", "region": "Europe", "signup_date": "2020-01-03"},
                {"customer_id": 4, "customer_name": "Customer_4", "customer_tier": "Premium", "region": "Asia", "signup_date": "2020-01-04"},
                {"customer_id": 5, "customer_name": "Customer_5", "customer_tier": "Gold", "region": "US-East", "signup_date": "2020-01-05"}
            ],
            "orders": [
                {"order_id": 1, "customer_id": 1, "order_date": "2024-01-01", "total_amount": 150.75, "status": "completed", "product_id": 1},
                {"order_id": 2, "customer_id": 2, "order_date": "2024-01-02", "total_amount": 89.50, "status": "processing", "product_id": 2},
                {"order_id": 3, "customer_id": 3, "order_date": "2024-01-03", "total_amount": 234.99, "status": "completed", "product_id": 3},
                {"order_id": 4, "customer_id": 1, "order_date": "2024-02-01", "total_amount": 445.00, "status": "completed", "product_id": 4},
                {"order_id": 5, "customer_id": 2, "order_date": "2024-02-02", "total_amount": 125.25, "status": "pending", "product_id": 5}
            ],
            "products": [
                {"product_id": 1, "product_name": "Product_1", "category": "Electronics", "price": 125.50},
                {"product_id": 2, "product_name": "Product_2", "category": "Books", "price": 89.25},
                {"product_id": 3, "product_name": "Product_3", "category": "Home", "price": 234.75},
                {"product_id": 4, "product_name": "Product_4", "category": "Sports", "price": 156.00},
                {"product_id": 5, "product_name": "Product_5", "category": "Clothing", "price": 445.99}
            ],
            "order_items": [
                {"item_id": 1, "order_id": 1, "product_id": 1, "quantity": 2, "unit_price": 75.38, "order_date": "2024-01-01"},
                {"item_id": 2, "order_id": 1, "product_id": 2, "quantity": 1, "unit_price": 89.25, "order_date": "2024-01-01"},
                {"item_id": 3, "order_id": 2, "product_id": 3, "quantity": 1, "unit_price": 89.50, "order_date": "2024-01-02"},
                {"item_id": 4, "order_id": 3, "product_id": 4, "quantity": 3, "unit_price": 52.00, "order_date": "2024-01-03"},
                {"item_id": 5, "order_id": 4, "product_id": 5, "quantity": 1, "unit_price": 234.99, "order_date": "2024-02-01"}
            ]
        }
    
    def execute_query(self, query: str, dry_run: bool = False) -> MockQueryResult:
        """Execute query with realistic simulation."""
        start_time = time.time()
        
        try:
            # Calculate execution time based on query complexity
            execution_time = self._calculate_execution_time(query)
            bytes_processed = self._calculate_bytes_processed(query)
            
            if dry_run:
                return MockQueryResult(
                    success=True,
                    results=[],
                    row_count=0,
                    execution_time_ms=execution_time,
                    bytes_processed=bytes_processed
                )
            
            # Generate realistic results
            results = self._generate_query_results(query)
            
            return MockQueryResult(
                success=True,
                results=results,
                row_count=len(results),
                execution_time_ms=execution_time,
                bytes_processed=bytes_processed
            )
            
        except Exception as e:
            return MockQueryResult(
                success=False,
                results=[],
                row_count=0,
                execution_time_ms=0,
                bytes_processed=0,
                error=str(e)
            )
    
    def _calculate_execution_time(self, query: str) -> int:
        """Calculate realistic execution time based on query complexity."""
        base_time = 500  # Base 500ms
        query_upper = query.upper()
        
        # Add time for different operations
        if "SELECT *" in query_upper:
            base_time += 300  # Extra time for full column scan
        
        join_count = len(re.findall(r'\bJOIN\b', query_upper))
        base_time += join_count * 400  # 400ms per JOIN
        
        if "COUNT(DISTINCT" in query_upper:
            base_time += 1500  # COUNT DISTINCT is expensive
        
        if "GROUP BY" in query_upper:
            base_time += 600  # Aggregation overhead
        
        if "ORDER BY" in query_upper:
            base_time += 400  # Sorting overhead
        
        if "OVER (" in query_upper:
            base_time += 300  # Window function overhead
        
        # Table size impact
        tables = self._extract_table_names(query)
        for table in tables:
            if table in self.tables:
                rows = self.tables[table].rows
                if rows > 1000000:
                    base_time += 800
                elif rows > 10000:
                    base_time += 300
        
        return base_time
    
    def _calculate_bytes_processed(self, query: str) -> int:
        """Calculate bytes processed based on tables and operations."""
        total_bytes = 0
        tables = self._extract_table_names(query)
        
        for table in tables:
            if table in self.tables:
                table_bytes = self.tables[table].size_bytes
                
                # Column pruning reduces bytes
                if "SELECT *" not in query.upper():
                    table_bytes = int(table_bytes * 0.6)
                
                total_bytes += table_bytes
        
        return total_bytes or 1000000
    
    def _generate_query_results(self, query: str) -> List[Dict[str, Any]]:
        """Generate realistic query results based on query type."""
        query_upper = query.upper()
        
        # COUNT queries
        if "COUNT(" in query_upper:
            if "COUNT(DISTINCT" in query_upper:
                return [{"count_distinct": 1500}]
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
            elif "category" in query.lower():
                return [
                    {"category": "Electronics", "total": 25000, "count": 800},
                    {"category": "Books", "total": 8000, "count": 200},
                    {"category": "Home", "total": 15000, "count": 400}
                ]
            else:
                return [
                    {"group_key": "Group1", "total": 1000, "count": 50},
                    {"group_key": "Group2", "total": 1500, "count": 75}
                ]
        
        # JOIN queries
        if "JOIN" in query_upper:
            return [
                {"customer_name": "Customer_1", "order_total": 150.50, "product_name": "Product_A"},
                {"customer_name": "Customer_2", "order_total": 275.25, "product_name": "Product_B"},
                {"customer_name": "Customer_3", "order_total": 89.75, "product_name": "Product_C"}
            ]
        
        # Window function queries
        if "OVER (" in query_upper:
            return [
                {"customer_id": 1, "order_date": "2024-01-01", "total_amount": 150.75, "rank": 1},
                {"customer_id": 2, "order_date": "2024-01-02", "total_amount": 275.25, "rank": 2},
                {"customer_id": 3, "order_date": "2024-01-03", "total_amount": 89.75, "rank": 3}
            ]
        
        # EXISTS/IN subquery results
        if "EXISTS" in query_upper or "IN (" in query_upper:
            return [
                {"customer_id": 1, "customer_name": "Customer_1"},
                {"customer_id": 2, "customer_name": "Customer_2"}
            ]
        
        # Simple SELECT queries
        primary_table = self._extract_primary_table(query)
        if primary_table and primary_table in self.sample_data:
            return self.sample_data[primary_table][:3]
        
        # Default result
        return [
            {"id": 1, "name": "Item1", "value": 100},
            {"id": 2, "name": "Item2", "value": 200},
            {"id": 3, "name": "Item3", "value": 300}
        ]
    
    def _extract_table_names(self, query: str) -> List[str]:
        """Extract table names from query."""
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
        """Extract primary table from FROM clause."""
        match = re.search(r'FROM\s+(\w+)', query, re.IGNORECASE)
        return match.group(1) if match else None
    
    def get_table_info(self, table_id: str) -> Dict[str, Any]:
        """Get mock table metadata."""
        table_name = table_id.split('.')[-1]
        
        if table_name in self.tables:
            table = self.tables[table_name]
            return {
                "table_id": table_name,
                "num_rows": table.rows,
                "num_bytes": table.size_bytes,
                "partitioning": {
                    "type": "DAY" if table.partitioned else None,
                    "field": table.partition_field
                },
                "clustering": {
                    "fields": table.clustered_fields
                },
                "schema": table.schema
            }
        
        return {"error": f"Table {table_name} not found"}
    
    def validate_query(self, query: str) -> Dict[str, Any]:
        """Validate query syntax."""
        query_upper = query.upper().strip()
        
        if not query_upper.startswith('SELECT'):
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
    
    def compare_query_performance(self, original_query: str, optimized_query: str, iterations: int = 3) -> Dict[str, Any]:
        """Compare performance between queries."""
        original_time = self._calculate_execution_time(original_query)
        optimized_time = self._calculate_execution_time(optimized_query)
        
        # Simulate improvement based on optimizations
        improvement = (original_time - optimized_time) / original_time
        
        return {
            "success": True,
            "original_avg_ms": original_time,
            "optimized_avg_ms": optimized_time,
            "improvement_percentage": improvement,
            "original_times": [original_time] * iterations,
            "optimized_times": [optimized_time] * iterations,
            "iterations": iterations
        }