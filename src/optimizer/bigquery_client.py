"""BigQuery client wrapper for query execution and performance measurement."""

import time
from typing import Optional, Dict, Any, List
from google.cloud import bigquery
from google.cloud.exceptions import GoogleCloudError
from google.oauth2 import service_account 

from config.settings import get_settings
from src.common.exceptions import BigQueryConnectionError
from src.common.logger import QueryOptimizerLogger
from src.common.models import PerformanceMetrics


class BigQueryClient:
    """Wrapper for BigQuery client with performance measurement capabilities."""
    
    def __init__(self, project_id: Optional[str] = None):
        self.settings = get_settings()
        self.logger = QueryOptimizerLogger(__name__)
        
        # Use provided project_id or fall back to settings
        self.project_id = project_id or self.settings.google_cloud_project
        
        if not self.project_id:
            raise BigQueryConnectionError("Google Cloud project ID not configured")
        
        try:
            credentials = service_account.Credentials.from_service_account_file(
                self.settings.google_application_credentials
            )
            print("✅ Using credentials from:", credentials.service_account_email)

            self.client = bigquery.Client(
                project=self.project_id,
                location=self.settings.default_location,
                credentials=credentials
            )
            self.logger.logger.info(f"Connected to BigQuery project: {self.project_id}")
        except Exception as e:
            raise BigQueryConnectionError(f"Failed to connect to BigQuery: {str(e)}", self.project_id)
    
    def execute_query(
        self, 
        query: str, 
        dry_run: bool = None,
        timeout: int = 300
    ) -> Dict[str, Any]:
        """Execute a query and return results with performance metrics."""
        if dry_run is None:
            dry_run = self.settings.dry_run
        
        try:
            start_time = time.time()
            
            # Configure job
            job_config = bigquery.QueryJobConfig(
                dry_run=dry_run,
                use_query_cache=False,  # Get fresh performance metrics
                # location=self.settings.default_location
            )
            
            # Submit query
            query_job = self.client.query(query, job_config=job_config)
            
            if dry_run:
                # For dry run, we get job statistics without execution
                execution_time_ms = int((time.time() - start_time) * 1000)
                
                performance = PerformanceMetrics(
                    execution_time_ms=execution_time_ms,
                    bytes_processed=query_job.total_bytes_processed,
                    bytes_billed=query_job.total_bytes_billed,
                    cache_hit=False
                )
                
                return {
                    "success": True,
                    "dry_run": True,
                    "performance": performance,
                    "results": None,
                    "row_count": None
                }
            else:
                # Wait for query to complete
                results = query_job.result(timeout=timeout)
                execution_time_ms = int((time.time() - start_time) * 1000)
                
                # Extract performance metrics
                performance = PerformanceMetrics(
                    execution_time_ms=execution_time_ms,
                    bytes_processed=query_job.total_bytes_processed,
                    bytes_billed=query_job.total_bytes_billed,
                    slot_time_ms=query_job.slot_millis,
                    total_slots=query_job.num_dml_affected_rows,  # This might not be accurate
                    cache_hit=query_job.cache_hit
                )
                
                # Convert results to list of dictionaries
                result_rows = []
                row_count = 0
                
                for row in results:
                    result_rows.append(dict(row))
                    row_count += 1
                
                return {
                    "success": True,
                    "dry_run": False,
                    "performance": performance,
                    "results": result_rows,
                    "row_count": row_count
                }
                
        except GoogleCloudError as e:
            self.logger.log_error(e, {"operation": "execute_query", "query": query[:100]})
            return {
                "success": False,
                "error": str(e),
                "error_type": "GoogleCloudError",
                "performance": None,
                "results": None,
                "row_count": None
            }
        except Exception as e:
            self.logger.log_error(e, {"operation": "execute_query", "query": query[:100]})
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__,
                "performance": None,
                "results": None,
                "row_count": None
            }
    
    def validate_query(self, query: str) -> Dict[str, Any]:
        """Validate a query using dry run."""
        try:
            result = self.execute_query(query, dry_run=True)
            
            if result["success"]:
                return {
                    "valid": True,
                    "bytes_processed": result["performance"].bytes_processed,
                    "estimated_cost": self._estimate_cost(result["performance"].bytes_processed),
                    "error": None
                }
            else:
                return {
                    "valid": False,
                    "bytes_processed": None,
                    "estimated_cost": None,
                    "error": result["error"]
                }
                
        except Exception as e:
            self.logger.log_error(e, {"operation": "validate_query"})
            return {
                "valid": False,
                "bytes_processed": None,
                "estimated_cost": None,
                "error": str(e)
            }
    
    def get_table_info(self, table_id: str) -> Dict[str, Any]:
        """Get information about a table."""
        try:
            table = self.client.get_table(table_id)
            
            return {
                "table_id": table.table_id,
                "dataset_id": table.dataset_id,
                "project_id": table.project,
                "num_rows": table.num_rows,
                "num_bytes": table.num_bytes,
                "partitioning": {
                    "type": table.time_partitioning.type_ if table.time_partitioning else None,
                    "field": table.time_partitioning.field if table.time_partitioning else None
                },
                "clustering": {
                    "fields": table.clustering_fields if table.clustering_fields else []
                },
                "schema": [
                    {
                        "name": field.name,
                        "type": field.field_type,
                        "mode": field.mode
                    }
                    for field in table.schema
                ]
            }
            
        except Exception as e:
            self.logger.log_error(e, {"operation": "get_table_info", "table_id": table_id})
            return {"error": str(e)}
    
    def is_table_partitioned(self, table_id: str) -> bool:
        """Check if a table is partitioned by date/timestamp."""
        try:
            table = self.client.get_table(table_id)
            return table.time_partitioning is not None
        except Exception:
            return False
    
    def get_table_partition_info(self, table_id: str) -> Dict[str, Any]:
        """Get partition information for a table."""
        try:
            table = self.client.get_table(table_id)
            if table.time_partitioning:
                return {
                    "is_partitioned": True,
                    "partition_type": table.time_partitioning.type_,
                    "partition_field": table.time_partitioning.field
                }
            else:
                return {"is_partitioned": False}
        except Exception as e:
            return {"is_partitioned": False, "error": str(e)}
    
    def get_query_plan(self, query: str) -> Dict[str, Any]:
        """Get query execution plan."""
        try:
            job_config = bigquery.QueryJobConfig(
                dry_run=False,
                use_query_cache=False
            )
            
            query_job = self.client.query(query, job_config=job_config)
            query_job.result()  # Wait for completion
            
            # Get query plan stages
            stages = []
            if hasattr(query_job, 'query_plan') and query_job.query_plan:
                for stage in query_job.query_plan:
                    stage_info = {
                        "name": stage.name,
                        "id": stage.id,
                        "status": stage.status,
                        "start_ms": stage.start_ms,
                        "end_ms": stage.end_ms,
                        "input_stages": stage.input_stages,
                        "parallel_inputs": stage.parallel_inputs,
                        "completed_parallel_inputs": stage.completed_parallel_inputs,
                        "records_read": stage.records_read,
                        "records_written": stage.records_written,
                        "shuffle_output_bytes": stage.shuffle_output_bytes,
                        "shuffle_output_bytes_spilled": stage.shuffle_output_bytes_spilled
                    }
                    stages.append(stage_info)
            
            return {
                "success": True,
                "stages": stages,
                "total_slot_ms": query_job.slot_millis,
                "total_bytes_processed": query_job.total_bytes_processed
            }
            
        except Exception as e:
            self.logger.log_error(e, {"operation": "get_query_plan"})
            return {
                "success": False,
                "error": str(e),
                "stages": []
            }
    
    def compare_query_performance(
        self, 
        original_query: str, 
        optimized_query: str,
        iterations: int = 3
    ) -> Dict[str, Any]:
        """Compare performance between original and optimized queries."""
        try:
            original_times = []
            optimized_times = []
            
            # Run multiple iterations for more accurate comparison
            for i in range(iterations):
                self.logger.logger.info(f"Performance comparison iteration {i+1}/{iterations}")
                
                # Test original query
                original_result = self.execute_query(original_query, dry_run=False)
                if original_result["success"]:
                    original_times.append(original_result["performance"].execution_time_ms)
                
                # Test optimized query
                optimized_result = self.execute_query(optimized_query, dry_run=False)
                if optimized_result["success"]:
                    optimized_times.append(optimized_result["performance"].execution_time_ms)
                
                # Small delay between iterations
                time.sleep(1)
            
            if not original_times or not optimized_times:
                return {
                    "success": False,
                    "error": "Failed to execute one or both queries"
                }
            
            # Calculate averages
            avg_original = sum(original_times) / len(original_times)
            avg_optimized = sum(optimized_times) / len(optimized_times)
            
            # Calculate improvement
            improvement = (avg_original - avg_optimized) / avg_original if avg_original > 0 else 0
            
            return {
                "success": True,
                "original_avg_ms": avg_original,
                "optimized_avg_ms": avg_optimized,
                "improvement_percentage": improvement,
                "original_times": original_times,
                "optimized_times": optimized_times,
                "iterations": iterations
            }
            
        except Exception as e:
            self.logger.log_error(e, {"operation": "compare_query_performance"})
            return {
                "success": False,
                "error": str(e)
            }
    
    def _estimate_cost(self, bytes_processed: Optional[int]) -> Optional[float]:
        """Estimate query cost based on bytes processed."""
        if not bytes_processed:
            return None
        
        # BigQuery pricing: $5 per TB processed (as of 2024)
        # This is a rough estimate and may vary by region
        cost_per_tb = 5.0
        tb_processed = bytes_processed / (1024 ** 4)  # Convert to TB
        
        return tb_processed * cost_per_tb
    
    def test_connection(self) -> bool:
        """Test BigQuery connection."""
        try:
            # Simple query to test connection
            test_query = "SELECT 1 as test"
            result = self.execute_query(test_query, dry_run=True)
            return result["success"]
        except Exception:
            return False