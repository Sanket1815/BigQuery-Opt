# Unified SQL Optimization Workflow

## 🎯 **Overview**

The BigQuery Query Optimizer now features a **single unified optimization workflow** that combines AI-powered optimization, schema validation, and result comparison into one seamless process.

## 🚀 **Single "Optimize Query" Button**

Instead of separate buttons, there's now **one unified button** that handles the complete workflow:

### **What It Does:**
1. **📡 Raw SQL → MCP Server**: Sends your SQL directly to the MCP server
2. **📚 Load All MD Files**: Automatically loads all documentation from `data/optimization_docs_md/`
3. **🤖 Gemini AI Optimization**: Sends SQL + docs to Gemini API for intelligent optimization
4. **🔍 Schema Validation**: Validates table references and schemas
5. **⚡ Query Execution**: Runs both queries (if BigQuery credentials available)
6. **🔐 Hash Comparison**: Compares results using MD5 hashing for validation
7. **📊 Unified Display**: Shows everything in one comprehensive interface

## 🏗️ **Architecture**

```
User Input → Single Button → Unified Workflow
                                    ↓
                    ┌─────────────────────────────────────┐
                    │  MCP Server + Gemini Integration   │
                    │  • Load all MD documentation       │
                    │  • Send to Gemini API              │
                    │  • Get optimized query             │
                    └─────────────────────────────────────┘
                                    ↓
                    ┌─────────────────────────────────────┐
                    │  Validation & Execution Pipeline   │
                    │  • Schema validation               │
                    │  • Query execution                 │
                    │  • Hash-based comparison           │
                    └─────────────────────────────────────┘
                                    ↓
                    ┌─────────────────────────────────────┐
                    │  Unified Results Display           │
                    │  • Workflow steps                  │
                    │  • Optimization details            │
                    │  • Validation results              │
                    │  • Performance metrics             │
                    └─────────────────────────────────────┘
```

## 🔧 **API Endpoints**

### **Main Optimization Endpoint**
```http
POST /api/v1/optimize-gemini
```

**Request Body:**
```json
{
    "query": "SELECT * FROM table WHERE condition",
    "project_id": "your-project-id",
    "validate_results": true,
    "measure_performance": false,
    "sample_size": 1000
}
```

### **Schema Validation Endpoint**
```http
POST /api/v1/validate-schemas
```

**Request Body:**
```json
{
    "original_query": "SELECT * FROM table1",
    "optimized_query": "SELECT * FROM table1 WHERE condition",
    "project_id": "your-project-id"
}
```

### **Query Execution & Comparison Endpoint**
```http
POST /api/v1/execute-and-compare
```

**Request Body:**
```json
{
    "original_query": "SELECT * FROM table1",
    "optimized_query": "SELECT * FROM table1 WHERE condition",
    "project_id": "your-project-id",
    "sample_size": 1000
}
```

## 📱 **User Interface**

### **Single Button Interface**
- **🚀 Optimize Query**: Single button that triggers the complete workflow
- **📝 Load Example**: Loads sample queries for testing
- **⚙️ Configuration Options**: Sample size, validation settings

### **Unified Results Display**
- **🔄 Workflow Steps**: Shows completion status of each step
- **🔍 Schema Validation**: Table references and validation results
- **⚡ Execution Results**: Performance metrics and result comparison
- **📊 Hash Comparison**: MD5-based result validation
- **💡 AI Explanation**: Gemini's optimization reasoning

## 🧪 **Testing**

### **Run the Test Suite**
```bash
python test_unified_workflow.py
```

### **Test Individual Components**
```bash
# Test Gemini optimization
curl -X POST "http://localhost:8000/api/v1/optimize-gemini" \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT * FROM test_table"}'

# Test schema validation
curl -X POST "http://localhost:8000/api/v1/validate-schemas" \
  -H "Content-Type: application/json" \
  -d '{"original_query": "SELECT * FROM table1", "optimized_query": "SELECT * FROM table1 WHERE x > 0"}'
```

## 🚀 **Getting Started**

### **1. Install Dependencies**
```bash
pip install -r requirements.txt
# or for minimal setup:
pip install -r requirements_minimal.txt
```

### **2. Set Environment Variables**
```bash
export GEMINI_API_KEY="your-gemini-api-key"
export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account.json"
```

### **3. Start the Server**
```bash
python run_api_server.py
```

### **4. Open the Web Interface**
Navigate to `http://localhost:8000` and use the single **🚀 Optimize Query** button!

## 🔍 **Workflow Details**

### **Step 1: MCP Server + Gemini**
- Loads all MD files from `data/optimization_docs_md/`
- Creates comprehensive system prompt with documentation
- Sends to Gemini API with optimized parameters
- Receives AI-generated optimized query

### **Step 2: Schema Validation**
- Extracts table references from both queries
- Validates schema consistency
- Identifies potential issues
- Provides detailed table mapping

### **Step 3: Query Execution & Comparison**
- Executes both queries in BigQuery (if credentials available)
- Captures performance metrics
- Generates MD5 hashes of results
- Compares for business logic preservation

### **Step 4: Unified Results**
- Displays complete workflow status
- Shows optimization details
- Presents validation results
- Provides performance comparison

## 🎨 **UI Features**

### **Workflow Progress Tracking**
- ✅ Step completion indicators
- 🔄 Real-time status updates
- 📊 Progress visualization

### **Result Comparison**
- 🔵 Original query results
- 🟢 Optimized query results
- 📈 Performance improvements
- 🔐 Hash validation status

### **Responsive Design**
- 📱 Mobile-friendly interface
- 🖥️ Desktop optimization
- 🎨 Modern UI components

## 🚨 **Troubleshooting**

### **Common Issues**

#### **Gemini API Not Working**
```bash
# Check API key
echo $GEMINI_API_KEY

# Verify package installation
pip show google-generativeai
```

#### **Schema Validation Fails**
- Ensure project ID is provided
- Check BigQuery permissions
- Verify table references exist

#### **Query Execution Errors**
- Set up BigQuery credentials
- Check project permissions
- Verify query syntax

### **Debug Mode**
Enable detailed logging:
```bash
export LOG_LEVEL=DEBUG
python run_api_server.py
```

## 🔮 **Future Enhancements**

- **🔄 Real-time Progress**: Live workflow status updates
- **📊 Advanced Analytics**: Detailed performance insights
- **🔗 Integration APIs**: Connect with other tools
- **📱 Mobile App**: Native mobile interface
- **🤖 AI Training**: Learn from user feedback

## 📚 **References**

- [BigQuery Documentation](https://cloud.google.com/bigquery/docs)
- [Gemini API Guide](https://ai.google.dev/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MCP Protocol](https://modelcontextprotocol.io/)

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests
5. Submit a pull request

## 📄 **License**

This project is licensed under the MIT License - see the LICENSE file for details.

---

**🎉 The unified workflow brings together the best of AI optimization, validation, and execution in one seamless experience!** 