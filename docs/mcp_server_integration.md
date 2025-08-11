# MCP Server Integration - Current Status and Usage

## 🚨 Current Status: MCP Server is NOT in Main Flow

The MCP (Model Context Protocol) server files exist in the project but are **NOT currently integrated** into the main optimization workflow that you use through the web UI.

## 📊 Two Separate Systems

### **Main Optimization System** (What you're using):
```
Web UI → FastAPI Routes → Query Optimizer → AI Optimizer → BigQuery → Results
```
**Files involved**: `index.html` → `routes.py` → `query_optimizer.py` → `ai_optimizer.py` → `bigquery_client.py`

### **MCP Server System** (Standalone):
```
MCP Client → MCP Server → Documentation Handler → Optimization Handler → Results
```
**Files involved**: `server.py` → `handlers.py` → `documentation_processor.py`

---

## 🔄 Where MCP Server Functions Would Fit (If Integrated)

If the MCP server were integrated into the main flow, it would work like this:

### **Current Flow** (What happens now):
```
4. _analyze_query_structure() [query_optimizer.py:200]
   ↓ Direct analysis using regex and sqlparse
   ↓ Returns QueryAnalysis

7. optimize_with_best_practices() [ai_optimizer.py:35]
   ↓ Direct AI optimization
   ↓ Calls Gemini API directly
```

### **Potential MCP Integration** (Not implemented):
```
4. _analyze_query_structure() [query_optimizer.py:200]
   ↓ Could call MCP server for analysis
   ↓ POST /analyze to MCP server
   ↓ OptimizationHandler.analyze_query() [handlers.py:50]
   ↓ Returns enhanced QueryAnalysis

7. optimize_with_best_practices() [ai_optimizer.py:35]
   ↓ Could call MCP server for suggestions
   ↓ POST /optimize to MCP server
   ↓ OptimizationHandler.get_optimization_suggestions() [handlers.py:120]
   ↓ Returns optimization suggestions
```

---

## 🛠️ MCP Server Functions (Available but Unused)

### **`src/mcp_server/server.py`**:
- **`BigQueryMCPServer`**: Standalone FastAPI server on port 8000
- **`/search`**: Search documentation semantically
- **`/patterns`**: Get optimization patterns for query
- **`/analyze`**: Analyze query structure
- **`/optimize`**: Get optimization suggestions

### **`src/mcp_server/handlers.py`**:
- **`DocumentationHandler.search_documentation()`**: Semantic search in docs
- **`OptimizationHandler.analyze_query()`**: Alternative query analysis
- **`OptimizationHandler.get_patterns_for_query()`**: Pattern identification
- **`OptimizationHandler.get_optimization_suggestions()`**: Suggestion generation

---

## 🚀 How to Use MCP Server (Separately)

### **Start MCP Server**:
```bash
python -m src.mcp_server.server
# Runs on http://localhost:8000
```

### **Use MCP Endpoints**:
```bash
# Analyze a query
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT * FROM orders", "request_type": "analyze"}'

# Get optimization patterns
curl -X POST http://localhost:8000/patterns \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT * FROM orders", "request_type": "patterns"}'

# Search documentation
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "JOIN optimization", "request_type": "search"}'
```

---

## 🎯 Why MCP Server Exists

1. **Alternative Interface**: Provides MCP protocol access to optimization
2. **Modular Design**: Separates documentation handling from main optimization
3. **Future Integration**: Ready for MCP-based optimization workflows
4. **Standalone Testing**: Can test optimization logic independently

---

## 🔧 Current Architecture Decision

**Your current system uses**:
- **Direct AI Integration**: Query Optimizer → AI Optimizer → Gemini API
- **Embedded Analysis**: Built-in query analysis in `query_optimizer.py`
- **Simple Flow**: Fewer components, faster execution

**MCP server provides**:
- **Modular Architecture**: Separate services for different functions
- **Protocol Compliance**: Standard MCP interface
- **Enhanced Documentation**: Better semantic search capabilities

The MCP server is built and ready but not currently used in your main optimization workflow. It's there for future enhancements or alternative integration approaches.