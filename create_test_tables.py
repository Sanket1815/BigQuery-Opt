#!/usr/bin/env python3
"""
Standalone script to create test tables in BigQuery for the Query Optimizer.
"""

import argparse
import os
import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from config.settings import get_settings
    from src.optimizer.bigquery_client import BigQueryClient
    from google.cloud import bigquery
    from google.cloud.exceptions import Conflict
except ImportError as e:
    print(f"❌ Missing dependencies: {e}")
    print("Please install requirements: pip install -r requirements.txt")
    sys.exit(1)


def create_test_dataset_and_tables(project_id=None):
    """Create test dataset and tables in BigQuery."""
    
    print("🚀 BigQuery Query Optimizer - Test Data Setup")
    print("=" * 50)
    
    # Setup configuration
    settings = get_settings()
    if project_id:
        settings.google_cloud_project = project_id
    
    if not settings.google_cloud_project:
        print("❌ Error: Google Cloud Project ID not configured")
        print("Please set GOOGLE_CLOUD_PROJECT environment variable or use --project-id")
        return False
    
    print(f"📍 Project: {settings.google_cloud_project}")
    print(f"🔑 Credentials: {settings.google_application_credentials}")
    
    try:
        # Initialize BigQuery client
        bq_client = BigQueryClient(project_id=settings.google_cloud_project)
        
        # Test connection
        if not bq_client.test_connection():
            print("❌ Failed to connect to BigQuery")
            return False
        
        print("✅ BigQuery connection successful")
        
    except Exception as e:
        print(f"❌ Failed to initialize BigQuery client: {e}")
        return False
    
    dataset_id = "optimizer_test_dataset"
    start_time = time.time()
    
    try:
        # Create dataset
        print(f"\n📁 Creating dataset: {settings.google_cloud_project}.{dataset_id}")
        
        try:
            dataset_full_id = f"{settings.google_cloud_project}.{dataset_id}"
            dataset = bigquery.Dataset(dataset_full_id)
            dataset.location = "US"
            dataset.description = "Test dataset for BigQuery Query Optimizer"
            
            dataset = bq_client.client.create_dataset(dataset, exists_ok=True)
            print(f"✅ Dataset {dataset.dataset_id} created successfully")
        except Exception as e:
            print(f"⚠️ Dataset creation warning: {e}")
            # Continue anyway - dataset might already exist
        
        # Wait for dataset to be ready
        time.sleep(2)
        
        print("\n📊 Creating test tables with sample data...")
        
        # Create customers table (1,000 rows)
        print("1️⃣ Creating customers table...")
        customers_sql = f"""
        CREATE OR REPLACE TABLE `{settings.google_cloud_project}.{dataset_id}.customers` AS
        SELECT 
            customer_id,
            CONCAT('Customer_', CAST(customer_id AS STRING)) as customer_name,
            CASE 
                WHEN MOD(customer_id, 4) = 0 THEN 'Premium'
                WHEN MOD(customer_id, 4) = 1 THEN 'Gold'
                WHEN MOD(customer_id, 4) = 2 THEN 'Silver'
                ELSE 'Bronze'
            END as customer_tier,
            CASE 
                WHEN MOD(customer_id, 5) = 0 THEN 'US-West'
                WHEN MOD(customer_id, 5) = 1 THEN 'US-East'
                WHEN MOD(customer_id, 5) = 2 THEN 'Europe'
                WHEN MOD(customer_id, 5) = 3 THEN 'Asia'
                ELSE 'Other'
            END as region,
            DATE_ADD('2020-01-01', INTERVAL MOD(customer_id, 1000) DAY) as signup_date
        FROM UNNEST(GENERATE_ARRAY(1, 1000)) as customer_id
        """
        
        result = bq_client.execute_query(customers_sql, dry_run=False)
        if not result["success"]:
            raise Exception(f"Failed to create customers table: {result['error']}")
        print("✅ Customers table created (1,000 rows)")
        
        # Create orders table (50,000 rows, partitioned)
        print("2️⃣ Creating orders table (partitioned)...")
        orders_sql = f"""
        CREATE OR REPLACE TABLE `{settings.google_cloud_project}.{dataset_id}.orders` 
        PARTITION BY order_date
        CLUSTER BY customer_id, status
        AS
        SELECT 
            order_id,
            MOD(order_id, 1000) + 1 as customer_id,
            DATE_ADD(DATE('2024-01-01'), INTERVAL MOD(order_id, 365) DAY) as order_date,
            ROUND(RAND() * 1000 + 50, 2) as total_amount,
            CASE 
                WHEN MOD(order_id, 10) = 0 THEN 'cancelled'
                WHEN MOD(order_id, 10) = 1 THEN 'pending'
                WHEN MOD(order_id, 10) = 2 THEN 'processing'
                ELSE 'completed'
            END as status,
            MOD(order_id, 50) + 1 as product_id
        FROM UNNEST(GENERATE_ARRAY(1, 50000)) as order_id
        """
        
        result = bq_client.execute_query(orders_sql, dry_run=False)
        if not result["success"]:
            raise Exception(f"Failed to create orders table: {result['error']}")
        print("✅ Orders table created (50,000 rows, partitioned by order_date with _PARTITIONDATE)")
        
        # Create products table (50 rows)
        print("3️⃣ Creating products table...")
        products_sql = f"""
        CREATE OR REPLACE TABLE `{settings.google_cloud_project}.{dataset_id}.products` AS
        SELECT 
            product_id,
            CONCAT('Product_', CAST(product_id AS STRING)) as product_name,
            CASE 
                WHEN MOD(product_id, 5) = 0 THEN 'Electronics'
                WHEN MOD(product_id, 5) = 1 THEN 'Clothing'
                WHEN MOD(product_id, 5) = 2 THEN 'Books'
                WHEN MOD(product_id, 5) = 3 THEN 'Home'
                ELSE 'Sports'
            END as category,
            ROUND(RAND() * 500 + 10, 2) as price
        FROM UNNEST(GENERATE_ARRAY(1, 50)) as product_id
        """
        
        result = bq_client.execute_query(products_sql, dry_run=False)
        if not result["success"]:
            raise Exception(f"Failed to create products table: {result['error']}")
        print("✅ Products table created (50 rows)")
        
        # Create order_items table (50,000 rows, partitioned)
        print("4️⃣ Creating order_items table (partitioned)...")
        order_items_sql = f"""
        CREATE OR REPLACE TABLE `{settings.google_cloud_project}.{dataset_id}.order_items`
        PARTITION BY order_date
        CLUSTER BY order_id
        AS
        SELECT 
            (order_id - 1) * 2 + item_seq as item_id,
            order_id,
            MOD((order_id - 1) * 2 + item_seq, 50) + 1 as product_id,
            CAST(RAND() * 5 + 1 AS INT64) as quantity,
            ROUND(RAND() * 100 + 10, 2) as unit_price,
            DATE_ADD(DATE('2024-01-01'), INTERVAL MOD(order_id, 365) DAY) as order_date
        FROM UNNEST(GENERATE_ARRAY(1, 25000)) as order_id,
        UNNEST(GENERATE_ARRAY(1, 2)) as item_seq
        """
        
        result = bq_client.execute_query(order_items_sql, dry_run=False)
        if not result["success"]:
            raise Exception(f"Failed to create order_items table: {result['error']}")
        print("✅ Order_items table created (50,000 rows, partitioned by order_date with _PARTITIONDATE)")
        
        # Verify all tables and show row counts
        print("\n📋 Verifying created tables:")
        tables = ["customers", "orders", "products", "order_items"]
        
        for table_name in tables:
            verify_sql = f"SELECT COUNT(*) as row_count FROM `{settings.google_cloud_project}.{dataset_id}.{table_name}`"
            verify_result = bq_client.execute_query(verify_sql, dry_run=False)
            
            if verify_result["success"] and verify_result["results"]:
                row_count = verify_result["results"][0]["row_count"]
                print(f"  📊 {table_name}: {row_count:,} rows")
            else:
                print(f"  ⚠️ Could not verify {table_name}")
        
        execution_time = time.time() - start_time
        
        print(f"\n🎉 Test data setup completed successfully!")
        print(f"⏱️ Total execution time: {execution_time:.1f} seconds")
        print(f"📍 Dataset: {settings.google_cloud_project}.{dataset_id}")
        print(f"🔗 View in BigQuery Console: https://console.cloud.google.com/bigquery?project={settings.google_cloud_project}")
        
        print(f"\n📝 You can now test queries like:")
        print(f"   SELECT * FROM `{settings.google_cloud_project}.{dataset_id}.orders` WHERE order_date >= '2024-06-01' LIMIT 10")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating test data: {e}")
        return False


def cleanup_test_data(project_id=None):
    """Clean up test dataset and tables."""
    
    print("🧹 Cleaning up test data...")
    
    settings = get_settings()
    if project_id:
        settings.google_cloud_project = project_id
    
    try:
        bq_client = BigQueryClient(project_id=settings.google_cloud_project)
        dataset_id = "optimizer_test_dataset"
        
        cleanup_sql = f"DROP SCHEMA IF EXISTS `{settings.google_cloud_project}.{dataset_id}` CASCADE"
        result = bq_client.execute_query(cleanup_sql, dry_run=False)
        
        if result["success"]:
            print("✅ Test data cleaned up successfully")
            return True
        else:
            print(f"❌ Failed to clean up test data: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")
        return False


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Create test tables for BigQuery Query Optimizer")
    parser.add_argument(
        "--project-id", 
        help="Google Cloud Project ID (overrides environment variable)"
    )
    parser.add_argument(
        "--cleanup", 
        action="store_true",
        help="Clean up test data instead of creating it"
    )
    parser.add_argument(
        "--verify-only",
        action="store_true", 
        help="Only verify existing tables without creating new ones"
    )
    
    args = parser.parse_args()
    
    # Set project ID if provided
    if args.project_id:
        os.environ["GOOGLE_CLOUD_PROJECT"] = args.project_id
    
    if args.cleanup:
        success = cleanup_test_data(args.project_id)
    elif args.verify_only:
        # Just verify existing tables
        settings = get_settings()
        if args.project_id:
            settings.google_cloud_project = args.project_id
            
        try:
            bq_client = BigQueryClient(project_id=settings.google_cloud_project)
            dataset_id = "optimizer_test_dataset"
            
            print(f"🔍 Verifying tables in {settings.google_cloud_project}.{dataset_id}")
            
            tables = ["customers", "orders", "products", "order_items"]
            for table_name in tables:
                verify_sql = f"SELECT COUNT(*) as row_count FROM `{settings.google_cloud_project}.{dataset_id}.{table_name}`"
                verify_result = bq_client.execute_query(verify_sql, dry_run=False)
                
                if verify_result["success"] and verify_result["results"]:
                    row_count = verify_result["results"][0]["row_count"]
                    print(f"✅ {table_name}: {row_count:,} rows")
                else:
                    print(f"❌ {table_name}: Not found or error")
            
            success = True
        except Exception as e:
            print(f"❌ Verification failed: {e}")
            success = False
    else:
        success = create_test_dataset_and_tables(args.project_id)
    
    if success:
        print("\n🎯 Next steps:")
        print("1. Start the API server: python run_api_server.py")
        print("2. Open http://localhost:8080")
        print("3. Enter your project ID and test the optimizer!")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()