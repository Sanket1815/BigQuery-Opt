# BigQuery Query Optimizer - Detailed Code Flow (Updated)

## Overview

This document traces the complete journey of a SQL query through our **enhanced MCP-integrated workflow with schema validation** from user input to optimized results.

---

## 🌐 Sample Query Journey

**Input Query**: `SELECT * FROM orders WHERE order_date >= '2024-01-01'`

**Expected Output**: Schema-validated optimized query with MCP-enhanced documentation references

---

## 📋 Complete Enhanced Code Flow

### 1. **Frontend User Interface** (`src/api/templates/index.html`)

#### **User Action**: User enters query and clicks "Optimize Query"

```javascript
// Function: optimizeQuery() - Line ~200
async function optimizeQuery() {
    const query = document.getElementById('sqlQuery').value.trim();
    // Gets: "SELECT * FROM orders WHERE order_date >= '2024-01-01'"
    
    const config = getRequestConfig();
    // Gets: { project_id: "user-project", validate: true, measure_performance: false }
    
    // Makes HTTP POST request to backend
    const response = await fetch('/api/v1/optimize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: safeQuery, ...config })
    });
}
```

**What happens**: 
- Extracts query from textarea
- Gets configuration (project ID, validation settings)
- Sends HTTP POST to `/api/v1/optimize` endpoint

---

### 2. **API Router** (`src/api/routes.py`)

#### **Function**: `optimize_query()` - Line 45

```python
@router.post("/optimize", response_model=OptimizationResult)
async def optimize_query(request: OptimizeRequest):
    # Receives: OptimizeRequest with query and config
    
    logger.logger.info(f"Optimizing query of length {len(request.query)}")
    # Logs: "Optimizing query of length 67"
    
    # Enhanced workflow with MCP server integration
    print(f"📡 Using MCP server for enhanced optimization workflow")
    
    # Creates the main optimizer instance
    optimizer = BigQueryOptimizer(
        project_id=request.project_id,
        validate_results=request.validate_results
    )
    
    # Test connection first
    if not optimizer.test_connection():
        raise HTTPException(status_code=503, detail="Failed to connect to required services")
    
    # Calls the main optimization function
    result = optimizer.optimize_query(
        request.query,
        validate_results=request.validate_results,
        measure_performance=request.measure_performance,
        sample_size=request.sample_size
    )
    
    return result  # Returns OptimizationResult object
```

**What happens**:
- Receives HTTP request with query and configuration
- Creates `BigQueryOptimizer` instance with MCP integration
- Tests connections to required services
- Calls main optimization method
- Returns structured optimization result

---

### 3. **Enhanced Query Optimizer** (`src/optimizer/query_optimizer.py`)

#### **Function**: `optimize_query()` - Line 45 (Enhanced)

```python
def optimize_query(self, query: str, validate_results: bool = True, ...):
    # Receives: "SELECT * FROM orders WHERE order_date >= '2024-01-01'"
    
    print(f"🚀 AI-POWERED BIGQUERY QUERY OPTIMIZER")
    print(f"📡 Enhanced with MCP Server Integration + Schema Validation")
    
    # STEP 1: Analyze the query structure
    analysis = self._analyze_query_structure(query)
    # Returns: QueryAnalysis with complexity, table count, issues, patterns
    
    # STEP 2: Extract table schema from BigQuery (NEW!)
    table_metadata = self._get_enhanced_table_metadata(query)
    # Returns: Dict with schema columns, partitioning, clustering details
    
    # STEP 3: Get MCP server optimization recommendations (NEW!)
    if self.mcp_handler:
        print(f"📡 Getting optimization recommendations from MCP server...")
        optimization_suggestions = self._get_mcp_optimization_suggestions_safe(query)
    else:
        optimization_suggestions = {}
    
    # STEP 4: Apply schema-aware AI optimization with MCP context
    optimization_result = self.ai_optimizer.optimize_with_best_practices(
        query, analysis, table_metadata, mcp_suggestions=optimization_suggestions
    )
    
    # STEP 5: Validate business logic preservation with schema validation
    if validate_results and self.validator:
        detailed_comparison = comparator.compare_query_results_detailed(
            query, optimization_result.optimized_query, sample_size=0
        )
        optimization_result.results_identical = detailed_comparison.results_identical
    
    return optimization_result
```

**What happens**:
- **Enhanced**: Now includes MCP server consultation
- **Enhanced**: Schema extraction and validation
- **Enhanced**: AI optimization with schema awareness
- **Enhanced**: Better error prevention and handling

---

### 4. **Schema Extraction** (`src/optimizer/query_optimizer.py`)

#### **Function**: `_get_enhanced_table_metadata()` - Line 250 (Enhanced)

```python
def _get_enhanced_table_metadata(self, query: str) -> Dict[str, Any]:
    # Receives: "SELECT * FROM orders WHERE order_date >= '2024-01-01'"
    
    table_names = self._extract_table_names(query)  # Returns: ["orders"]
    metadata = {}
    
    for table_name in table_names:
        # Construct full table name
        full_table_name = f"{self.bq_client.project_id}.optimizer_test_dataset.{table_name}"
        
        # Get table info from BigQuery (including schema!)
        table_info = self.bq_client.get_table_info(full_table_name)
        
        # Extract actual column names from schema (NEW!)
        schema_columns = []
        if "schema" in table_info:
            schema_columns = [field["name"] for field in table_info["schema"]]
        print(f"    📋 Available columns: {', '.join(schema_columns[:5])}...")
        
        metadata[full_table_name] = {
            "is_partitioned": table_info.get("partitioning", {}).get("type") is not None,
            "partition_field": table_info.get("partitioning", {}).get("field"),
            "num_rows": table_info.get("num_rows", 0),
            "clustering_fields": table_info.get("clustering", {}).get("fields", []),
            "schema_columns": schema_columns,  # NEW: Actual column names
            "table_name_simple": table_name
        }
    
    return metadata
```

**What happens**:
- **NEW**: Extracts actual column names from BigQuery table schema
- **NEW**: Validates table structure and available columns
- **Enhanced**: More comprehensive table metadata
- **Enhanced**: Better error handling for missing tables

---

### 5. **MCP Server Consultation** (`src/optimizer/query_optimizer.py`)

#### **Function**: `_get_mcp_optimization_suggestions_safe()` - Line 400 (NEW)

```python
def _get_mcp_optimization_suggestions_safe(self, query: str) -> Dict[str, Any]:
    # Receives: "SELECT * FROM orders WHERE order_date >= '2024-01-01'"
    
    try:
        if not self.mcp_handler:
            return {}
        
        # Use safe async runner to handle event loop issues
        suggestions = self._run_async_safely(
            self.mcp_handler.get_optimization_suggestions(query)
        )
        
        print(f"📋 MCP server provided {len(suggestions.get('specific_suggestions', []))} optimization suggestions")
        
        return suggestions
        # Returns: {
        #   "priority_optimizations": ["column_pruning"],
        #   "specific_suggestions": [...],
        #   "documentation_references": [...]
        # }
        
    except Exception as e:
        print(f"⚠️ MCP server request failed: {e}")
        return {}
```

**What happens**:
- **NEW**: Consults MCP server for documentation-backed suggestions
- **NEW**: Gets priority optimizations and specific advice
- **NEW**: Retrieves relevant documentation context
- **Enhanced**: Safe async handling for all environments

---

### 6. **Enhanced AI Optimizer** (`src/optimizer/ai_optimizer.py`)

#### **Function**: `optimize_with_best_practices()` - Line 35 (Enhanced)

```python
def optimize_with_best_practices(
    self, 
    query: str, 
    analysis: QueryAnalysis,
    table_metadata: Dict[str, Any],
    mcp_suggestions: Optional[Dict[str, Any]] = None  # NEW parameter
) -> OptimizationResult:
    
    # Build enhanced prompt with schema and MCP context
    prompt = self._build_comprehensive_optimization_prompt(
        query, analysis, table_metadata, mcp_suggestions
    )
    
    # Generate optimization using Gemini with enhanced context
    response = self.model.generate_content(prompt)
    
    # Parse and validate the AI response
    optimization_data = self._parse_ai_response(response.text)
    
    # Create schema-validated optimization result
    result = self._create_optimization_result(query, analysis, optimization_data, start_time)
    
    return result
```

**What happens**:
- **Enhanced**: Now receives MCP suggestions as input
- **Enhanced**: Builds prompts with schema and documentation context
- **Enhanced**: Better AI optimization with more context
- **Enhanced**: Schema-validated results

---

### 7. **Enhanced AI Prompt Building** (`src/optimizer/ai_optimizer.py`)

#### **Function**: `_build_comprehensive_optimization_prompt()` - Line 100 (Enhanced)

```python
def _build_comprehensive_optimization_prompt(self, query, analysis, table_metadata, mcp_suggestions):
    
    # Create detailed table metadata with schema (ENHANCED)
    table_info = ""
    for table_name, metadata in table_metadata.items():
        schema_columns = metadata.get('schema_columns', [])
        table_info += f"""
- {table_name}:
  Available columns: {schema_columns}  # NEW: Actual column names
  Partitioned: {metadata.get('is_partitioned', False)}
  Row count: {metadata.get('num_rows', 0):,}
  🚨 CRITICAL: ONLY use columns from 'Available columns' list!
"""
    
    # Add MCP server suggestions (NEW)
    mcp_context = ""
    if mcp_suggestions:
        mcp_context = f"""

📡 MCP SERVER OPTIMIZATION RECOMMENDATIONS:

PRIORITY OPTIMIZATIONS: {', '.join(mcp_suggestions.get('priority_optimizations', []))}

SPECIFIC SUGGESTIONS FROM DOCUMENTATION:
"""
        for suggestion in mcp_suggestions.get('specific_suggestions', []):
            mcp_context += f"""
• {suggestion.get('pattern_name', 'Unknown')}: {suggestion.get('description', '')}
  Expected improvement: {suggestion.get('expected_improvement', 0):.1%}
  Documentation: {suggestion.get('documentation_reference', 'N/A')}
"""
    
    # Build comprehensive prompt with schema validation
    prompt = f"""
🚨 CRITICAL SCHEMA VALIDATION REQUIREMENT 🚨
- ONLY use columns that ACTUALLY exist in the table schema
- NEVER generate non-existent column names
- When replacing SELECT *, use ONLY the columns listed in "Available columns"
- If unsure about column names, keep the original SELECT clause

TABLE METADATA WITH ACTUAL SCHEMA:
{table_info}

{mcp_context}

UNDERPERFORMING QUERY TO OPTIMIZE:
```sql
{query}
```

🎯 OPTIMIZATION REQUIREMENTS:
1. CRITICAL: Use ONLY existing columns from schema
2. Apply MCP server suggestions where applicable
3. Include documentation references
4. Ensure identical results
5. Target 30-50% performance improvement

Return optimized query using ONLY existing schema columns.
"""
    
    return prompt
```

**What happens**:
- **NEW**: Includes actual table schema columns in prompt
- **NEW**: Adds MCP server suggestions and documentation context
- **Enhanced**: Clear instructions about column validation
- **Enhanced**: Better context for AI optimization decisions

---

### 8. **Schema-Validated Result Creation** (`src/optimizer/ai_optimizer.py`)

#### **Function**: `_create_optimization_result()` - Line 200 (Enhanced)

```python
def _create_optimization_result(self, original_query, analysis, optimization_data, start_time):
    
    # Parse applied optimizations with documentation references
    applied_optimizations = []
    for opt_data in optimization_data.get('optimizations_applied', []):
        optimization = AppliedOptimization(
            pattern_id=opt_data.get('pattern_id', 'unknown'),
            pattern_name=opt_data.get('pattern_name', 'Unknown Optimization'),
            description=opt_data.get('description', 'No description provided'),
            before_snippet=opt_data.get('before_snippet', ''),
            after_snippet=opt_data.get('after_snippet', ''),
            documentation_reference=opt_data.get('documentation_reference', ''),  # MCP-enhanced
            expected_improvement=opt_data.get('expected_improvement'),
            confidence_score=opt_data.get('confidence_score', 1.0)
        )
        applied_optimizations.append(optimization)
    
    # Get schema-validated optimized query
    optimized_query = optimization_data.get('optimized_query', original_query)
    
    # Validate that optimized query uses only existing columns
    validation_result = self._validate_optimized_query_schema(optimized_query, table_metadata)
    if not validation_result["valid"]:
        print(f"⚠️ Schema validation failed: {validation_result['error']}")
        # Fall back to original query if schema validation fails
        optimized_query = original_query
        applied_optimizations = []
    
    return OptimizationResult(
        original_query=original_query,
        query_analysis=analysis,
        optimized_query=optimized_query,
        optimizations_applied=applied_optimizations,
        total_optimizations=len(applied_optimizations),
        estimated_improvement=optimization_data.get('estimated_improvement'),
        processing_time_seconds=time.time() - start_time
    )
```

**What happens**:
- **NEW**: Schema validation of optimized query
- **Enhanced**: Documentation references from MCP server
- **Enhanced**: Better error handling and fallback
- **Enhanced**: Validation that only existing columns are used

---

## 🔄 Enhanced Data Flow

### **Input Data**:
```
User Query: "SELECT * FROM orders WHERE order_date >= '2024-01-01'"
Config: {project_id: "user-project", validate: true}
```

### **After Enhanced Analysis**:
```
QueryAnalysis: {
    complexity: "simple",
    table_count: 1,
    potential_issues: ["Using SELECT *", "Consider adding date filters"],
    applicable_patterns: ["column_pruning", "clustering_optimization"]
}
```

### **After Schema Extraction** (NEW):
```
Enhanced TableMetadata: {
    "user-project.optimizer_test_dataset.orders": {
        is_partitioned: true,
        partition_field: "order_date", 
        num_rows: 50000,
        clustering_fields: ["customer_id", "status"],
        schema_columns: ["order_id", "customer_id", "order_date", "total_amount", "status", "product_id"]  # NEW
    }
}
```

### **After MCP Server Consultation** (NEW):
```
MCP Suggestions: {
    priority_optimizations: ["column_pruning", "clustering_optimization"],
    specific_suggestions: [
        {
            pattern_name: "Column Pruning",
            description: "Replace SELECT * with specific columns to reduce data transfer",
            expected_improvement: 0.25,
            documentation_reference: "https://cloud.google.com/bigquery/docs/best-practices-performance-input",
            specific_advice: "Specify only the columns you need instead of using SELECT *"
        }
    ],
    documentation_references: [
        {
            title: "BigQuery Performance Best Practices",
            content: "Avoid SELECT * to reduce data transfer...",
            optimization_patterns: ["column_pruning"]
        }
    ]
}
```

### **After Enhanced AI Optimization**:
```
OptimizationResult: {
    optimized_query: "SELECT order_id, customer_id, order_date, total_amount, status FROM orders WHERE order_date >= '2024-01-01'",
    optimizations_applied: [
        {
            pattern_name: "Column Pruning",
            description: "Replaced SELECT * with existing table columns to reduce data transfer",
            expected_improvement: 0.25,
            documentation_reference: "https://cloud.google.com/bigquery/docs/best-practices-performance-input",
            before_snippet: "SELECT *",
            after_snippet: "SELECT order_id, customer_id, order_date, total_amount, status"
        }
    ],
    total_optimizations: 1,
    estimated_improvement: 0.25
}
```

### **After Schema Validation** (NEW):
```
Schema Validation: {
    valid: true,
    columns_used: ["order_id", "customer_id", "order_date", "total_amount", "status"],
    all_columns_exist: true,
    validation_message: "All columns exist in table schema"
}
```

### **After Result Validation**:
```
QueryResultComparison: {
    original_results: [
        {order_id: 1, customer_id: 1, order_date: "2024-01-01", total_amount: 150.75, status: "completed", product_id: 1},
        {order_id: 2, customer_id: 2, order_date: "2024-01-02", total_amount: 89.50, status: "processing", product_id: 2}
    ],
    optimized_results: [
        {order_id: 1, customer_id: 1, order_date: "2024-01-01", total_amount: 150.75, status: "completed"},
        {order_id: 2, customer_id: 2, order_date: "2024-01-02", total_amount: 89.50, status: "processing"}
    ],
    original_row_count: 150,
    optimized_row_count: 150,
    results_identical: true,
    comparison_summary: "✅ Results are identical (150 rows)"
}
```

---

## 🎯 Enhanced Success Points

### 1. **Schema Awareness** (NEW)
- ✅ Extracts actual column names from BigQuery tables
- ✅ AI only uses existing columns in optimized queries
- ✅ Prevents "column not found" errors
- ✅ Schema validation before query execution

### 2. **MCP Server Integration** (NEW)
- ✅ Documentation-backed optimization suggestions
- ✅ Enhanced AI context with official BigQuery docs
- ✅ Better explanation quality with references
- ✅ Priority optimization recommendations

### 3. **Enhanced Error Prevention**
- ✅ Column validation prevents BigQuery errors
- ✅ Graceful fallback if MCP server unavailable
- ✅ Robust async handling for all environments
- ✅ Better logging and debugging

### 4. **Improved User Experience**
- ✅ More reliable optimizations
- ✅ Better explanations with documentation links
- ✅ Fewer errors and failures
- ✅ Enhanced result display

## 🔄 Complete Enhanced Function Call Chain

```
1. optimizeQuery() [JavaScript]
   ↓ HTTP POST /api/v1/optimize
   
2. optimize_query() [routes.py:45] - Enhanced with MCP logging
   ↓ Creates BigQueryOptimizer with MCP integration
   
3. optimize_query() [query_optimizer.py:45] - Enhanced workflow
   ↓ Calls _analyze_query_structure()
   
4. _analyze_query_structure() [query_optimizer.py:200]
   ↓ Returns QueryAnalysis
   
5. _get_enhanced_table_metadata() [query_optimizer.py:250] - NEW: Schema extraction
   ↓ Calls bq_client.get_table_info() + extracts schema
   
6. get_table_info() [bigquery_client.py:150] - Enhanced with schema
   ↓ Google Cloud BigQuery API call + schema extraction
   
7. _get_mcp_optimization_suggestions_safe() [query_optimizer.py:400] - NEW: MCP consultation
   ↓ Calls MCP server for documentation-backed suggestions
   
8. optimize_with_best_practices() [ai_optimizer.py:35] - Enhanced with MCP + schema
   ↓ Calls _build_comprehensive_optimization_prompt() with MCP context
   
9. _build_comprehensive_optimization_prompt() [ai_optimizer.py:100] - Enhanced prompt
   ↓ Returns structured prompt with schema + MCP suggestions
   
10. model.generate_content() [ai_optimizer.py:120] - Enhanced context
    ↓ Google Gemini AI API call with schema awareness
    
11. _parse_ai_response() [ai_optimizer.py:180] - Enhanced validation
    ↓ Returns optimization data + validates schema usage
    
12. compare_query_results_detailed() [result_comparator.py:25] - Enhanced comparison
    ↓ Executes both queries with schema validation
    
13. displayOptimizationResult() [JavaScript] - Enhanced display
    ↓ Shows MCP-enhanced results with documentation references
```

## 🎉 Enhanced Benefits

✅ **No Column Errors**: AI only uses existing table columns  
✅ **MCP Integration**: Documentation-backed optimization suggestions  
✅ **Better Context**: Enhanced AI optimization with official docs  
✅ **Error Prevention**: Schema validation prevents BigQuery failures  
✅ **Enhanced UX**: Better explanations and documentation references  

This enhanced workflow ensures reliable, schema-aware optimization with proper MCP server integration and comprehensive error prevention!