# BigQuery Query Optimizer - Architecture Diagram (Updated)

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        BigQuery Query Optimizer System                          │
│                   AI-Powered SQL Optimization with MCP Integration              │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              USER INTERFACES                                    │
├─────────────────────┬─────────────────────┬─────────────────────┬──────────────┤
│   🌐 Web UI         │   💻 CLI Tool       │   🐍 Python API    │  📊 REST API │
│   (Port 8080)       │   (Terminal)        │   (Direct Import)  │  (HTTP/JSON) │
│                     │                     │                     │              │
│ • Query Input       │ • File Processing   │ • Programmatic     │ • Batch      │
│ • Schema Validation │ • Batch Operations  │   Integration      │   Processing │
│ • MCP Integration   │ • Automation        │ • Custom Workflows │ • API Access │
│ • Result Display    │ • Performance       │ • Error Handling   │ • Status     │
└─────────────────────┴─────────────────────┴─────────────────────┴──────────────┘
                                           │
                                           ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      ENHANCED OPTIMIZATION ENGINE                               │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────────────────┐  │
│  │  📊 Query       │    │  🔍 Schema      │    │  📡 MCP Server              │  │
│  │  Analyzer       │    │  Extractor      │    │  Integration                │  │
│  │                 │    │                 │    │  (Port 8001)                │  │
│  │ • Parse SQL     │    │ • Extract Table │    │ • Documentation Search      │  │
│  │ • Extract       │    │   Names         │    │ • Pattern Suggestions      │  │
│  │   Patterns      │    │ • Get Schema    │    │ • Context Enhancement      │  │
│  │ • Complexity    │    │   from BigQuery │    │ • Best Practice References │  │
│  │   Assessment    │    │ • Validate      │    │ • Semantic Search          │  │
│  │                 │    │   Columns       │    │                             │  │
│  └─────────────────┘    └─────────────────┘    └─────────────────────────────┘  │
│           │                       │                           │                  │
│           └───────────────────────┼───────────────────────────┘                  │
│                                   │                                              │
│  ┌─────────────────────────────────────────────────────────────────────────────┐  │
│  │                    🤖 Enhanced AI Optimizer                                 │  │
│  │                                                                             │  │
│  │ • Schema-Aware Optimization    • MCP Context Integration                   │  │
│  │ • Column Validation            • Documentation References                  │  │
│  │ • Google Best Practices        • Pattern Application                       │  │
│  │ • Error Prevention             • Performance Targeting                     │  │
│  └─────────────────────────────────────────────────────────────────────────────┘  │
│                                   │                                              │
│  ┌─────────────────────────────────────────────────────────────────────────────┐  │
│  │                    ✅ Result Validator & Comparator                        │  │
│  │                                                                             │  │
│  │ • Execute Both Queries         • Raw Result Display                        │  │
│  │ • Schema Validation            • Manual Validation                         │  │
│  │ • Business Logic Check         • Performance Measurement                   │  │
│  │ • 100% Accuracy Requirement    • Error Detection                           │  │
│  └─────────────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      KNOWLEDGE & DATA LAYER                                     │
├─────────────────────┬─────────────────────┬─────────────────────┬──────────────┤
│  📚 Documentation   │  🗄️ Vector Database │  🔍 Pattern         │  📈 BigQuery │
│  Crawler            │  (ChromaDB)         │  Matcher            │  Client      │
│                     │                     │                     │              │
│ • Web Scraping      │ • Semantic Search   │ • 22+ Patterns      │ • Schema     │
│ • Content           │ • Embeddings        │ • Smart Matching    │   Extraction │
│   Processing        │ • Similarity        │ • Priority Scoring  │ • Query      │
│ • Pattern           │   Scoring           │ • Documentation     │   Execution  │
│   Extraction        │ • Context           │   References        │ • Performance│
│                     │   Retrieval         │                     │   Metrics    │
└─────────────────────┴─────────────────────┴─────────────────────┴──────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           EXTERNAL SERVICES                                     │
├─────────────────────┬─────────────────────┬─────────────────────┬──────────────┤
│  🤖 Google Gemini   │  ☁️ Google Cloud    │  📊 BigQuery        │  📚 Google   │
│  AI API             │  Platform           │  Service            │  Cloud Docs  │
│                     │                     │                     │              │
│ • Schema-Aware      │ • Authentication    │ • Query Execution   │ • Best       │
│   Optimization      │ • Project           │ • Schema Metadata   │   Practices  │
│ • Pattern           │   Management        │ • Performance       │ • Official   │
│   Recognition       │ • IAM & Security    │   Metrics           │   Guidelines │
│ • MCP-Enhanced      │ • Resource          │ • Result Sets       │ • Updates    │
│   Context           │   Management        │ • Cost Tracking     │ • Examples   │
└─────────────────────┴─────────────────────┴─────────────────────┴──────────────┘
```

## Enhanced Workflow Integration

### 1. **Documentation Crawler → MCP Server → Schema-Aware Optimization**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        ENHANCED OPTIMIZATION WORKFLOW                           │
└─────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────┐
    │ 📚 Documentation│
    │ Crawler         │
    │                 │
    │ • Crawls Google │
    │   Cloud Docs    │
    │ • Extracts      │
    │   Patterns      │
    │ • Creates       │
    │   Knowledge Base│
    └─────────────────┘
            │
            │ Documentation Data
            ▼
    ┌─────────────────┐
    │ 📡 MCP Server   │
    │ (Port 8001)     │
    │                 │
    │ • Vector DB     │
    │ • Semantic      │
    │   Search        │
    │ • Pattern       │
    │   Matching      │
    │ • Context       │
    │   Serving       │
    └─────────────────┘
            │
            │ Optimization Suggestions
            ▼
    ┌─────────────────┐
    │ 🔍 Schema       │
    │ Extractor       │
    │                 │
    │ • Extract Table │
    │   Names         │
    │ • Get BigQuery  │
    │   Schema        │
    │ • Validate      │
    │   Columns       │
    └─────────────────┘
            │
            │ Schema + MCP Context
            ▼
    ┌─────────────────┐
    │ 🤖 Enhanced AI  │
    │ Optimizer       │
    │                 │
    │ • Schema-Aware  │
    │ • MCP-Enhanced  │
    │ • Column        │
    │   Validation    │
    │ • Google Best   │
    │   Practices     │
    └─────────────────┘
            │
            │ Validated Optimized Query
            ▼
    ┌─────────────────┐
    │ ✅ Result       │
    │ Validator       │
    │                 │
    │ • Execute Both  │
    │ • Compare       │
    │ • Display Raw   │
    │   Results       │
    │ • Manual        │
    │   Validation    │
    └─────────────────┘
```

## Port Configuration

- **Main API Server**: Port 8080 (Web UI + REST API)
- **MCP Server**: Port 8001 (Documentation Service)
- **No Port Conflicts**: Services run independently

## Key Enhancements

### 1. **Schema Validation**
- Extracts actual column names from BigQuery tables
- AI only uses existing columns in optimized queries
- Prevents "column not found" errors

### 2. **MCP Integration**
- Documentation-backed optimization suggestions
- Enhanced AI context with official BigQuery docs
- Better explanation quality with references

### 3. **Error Prevention**
- Column validation before query generation
- Graceful fallback if MCP server unavailable
- Robust async handling for all environments

This architecture ensures reliable, schema-aware optimization with proper MCP server integration!