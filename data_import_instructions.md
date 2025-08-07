# BigQuery Table Setup Instructions

## 1. Create Tables in Google Cloud Console

Go to your BigQuery console and create these 4 tables:

### Table 1: customers
```sql
CREATE TABLE `your-project-id.optimizer_test_dataset.customers` (
  customer_id INT64,
  customer_name STRING,
  customer_tier STRING,
  region STRING,
  signup_date DATE
);
```

### Table 2: products  
```sql
CREATE TABLE `your-project-id.optimizer_test_dataset.products` (
  product_id INT64,
  product_name STRING,
  category STRING,
  price FLOAT64
);
```

### Table 3: orders (partitioned by order_date)
```sql
CREATE TABLE `your-project-id.optimizer_test_dataset.orders` (
  order_id INT64,
  customer_id INT64,
  order_date DATE,
  total_amount FLOAT64,
  status STRING,
  product_id INT64
)
PARTITION BY order_date;
```

### Table 4: order_items (partitioned by order_date)
```sql
CREATE TABLE `your-project-id.optimizer_test_dataset.order_items` (
  item_id INT64,
  order_id INT64,
  product_id INT64,
  quantity INT64,
  unit_price FLOAT64,
  order_date DATE
)
PARTITION BY order_date;
```

## 2. Import Data

### Option A: Using BigQuery Console
1. Go to each table in BigQuery console
2. Click "Upload" 
3. Choose "Upload from file"
4. Select JSON format
5. Upload the corresponding data from `sample_data.json`

### Option B: Using bq command line
```bash
# Import customers
bq load --source_format=NEWLINE_DELIMITED_JSON \
  your-project-id:optimizer_test_dataset.customers \
  customers.json

# Import products  
bq load --source_format=NEWLINE_DELIMITED_JSON \
  your-project-id:optimizer_test_dataset.products \
  products.json

# Import orders
bq load --source_format=NEWLINE_DELIMITED_JSON \
  your-project-id:optimizer_test_dataset.orders \
  orders.json

# Import order_items
bq load --source_format=NEWLINE_DELIMITED_JSON \
  your-project-id:optimizer_test_dataset.order_items \
  order_items.json
```

### Option C: Split JSON into separate files
You can split the `sample_data.json` into 4 separate files:
- `customers.json` - just the customers array
- `products.json` - just the products array  
- `orders.json` - just the orders array
- `order_items.json` - just the order_items array

## 3. Test Queries

After importing, test with these queries:

```sql
-- Test customers table
SELECT COUNT(*) FROM `your-project-id.optimizer_test_dataset.customers`;

-- Test orders table  
SELECT COUNT(*) FROM `your-project-id.optimizer_test_dataset.orders`;

-- Test with date filter
SELECT * FROM `your-project-id.optimizer_test_dataset.orders` 
WHERE order_date >= '2024-06-01' 
LIMIT 10;

-- Test JOIN
SELECT c.customer_name, o.total_amount 
FROM `your-project-id.optimizer_test_dataset.customers` c
JOIN `your-project-id.optimizer_test_dataset.orders` o 
  ON c.customer_id = o.customer_id
WHERE o.order_date >= '2024-06-01'
LIMIT 10;
```

## 4. Update Project ID

Make sure to replace `your-project-id` with your actual Google Cloud project ID in:
1. The table creation SQL
2. The test queries
3. Your application configuration