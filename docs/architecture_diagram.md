# BigQuery Query Optimizer - Architecture Diagram

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        BigQuery Query Optimizer System                          │
│                     AI-Powered SQL Optimization Platform                        │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              USER INTERFACES                                    │
├─────────────────────┬─────────────────────┬─────────────────────┬──────────────┤
│   🌐 Web UI         │   💻 CLI Tool       │   🐍 Python API    │  📊 REST API │
│   (Port 8080)       │   (Terminal)        │   (Direct Import)  │  (HTTP/JSON) │
│                     │                     │                     │              │
│ • Query Input       │ • File Processing   │ • Programmatic     │ • Batch      │
│ • Real-time Results │ • Batch Operations  │   Integration      │   Processing │
│ • Visual Comparison │ • Automation        │ • Custom Workflows │ • Webhooks   │
└─────────────────────┴─────────────────────┴─────────────────────┴──────────────┘
                                           │
                                           ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           CORE OPTIMIZATION ENGINE                              │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────────────────┐  │
│  │  📊 Query       │    │  🤖 AI          │    │  ✅ Result                  │  │
│  │  Analyzer       │    │  Optimizer      │    │  Validator                  │  │
│  │                 │    │                 │    │                             │  │
│  │ • Parse SQL     │    │ • Gemini API    │    │ • Execute Both Queries      │  │
│  │ • Extract       │    │ • Apply 20+     │    │ • Compare Results           │  │
│  │   Patterns      │    │   Patterns      │    │ • Ensure 100% Accuracy      │  │
│  │ • Complexity    │    │ • Generate      │    │ • Performance Measurement   │  │
│  │   Assessment    │    │   Explanations  │    │ • Business Logic Check      │  │
│  └─────────────────┘    └─────────────────┘    └─────────────────────────────┘  │
│           │                       │                           │                  │
│           └───────────────────────┼───────────────────────────┘                  │
│                                   │                                              │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         KNOWLEDGE & DATA LAYER                                  │
├─────────────────────┬─────────────────────┬─────────────────────┬──────────────┤
│  📚 Documentation   │  🗄️ Vector Database │  🔍 Pattern         │  📈 BigQuery │
│  Crawler            │  (ChromaDB)         │  Matcher            │  Client      │
│                     │                     │                     │              │
│ • Web Scraping      │ • Semantic Search   │ • 20+ Patterns      │ • Query      │
│ • Content           │ • Embeddings        │ • Smart Matching    │   Execution  │
│   Processing        │ • Similarity        │ • Priority Scoring  │ • Performance│
│ • Pattern           │   Scoring           │ • Documentation     │   Metrics    │
│   Extraction        │ • Context           │   References        │ • Validation │
│                     │   Retrieval         │                     │ • Metadata   │
└─────────────────────┴─────────────────────┴─────────────────────┴──────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           EXTERNAL SERVICES                                     │
├─────────────────────┬─────────────────────┬─────────────────────┬──────────────┤
│  🤖 Google Gemini   │  ☁️ Google Cloud    │  📊 BigQuery        │  📚 Google   │
│  AI API             │  Platform           │  Service            │  Cloud Docs  │
│                     │                     │                     │              │
│ • Query             │ • Authentication    │ • Query Execution   │ • Best       │
│   Optimization      │ • Project           │ • Performance       │   Practices  │
│ • Pattern           │   Management        │   Metrics           │ • Official   │
│   Recognition       │ • IAM & Security    │ • Result Sets       │   Guidelines │
│ • Explanation       │ • Resource          │ • Table Metadata    │ • Updates    │
│   Generation        │   Management        │ • Cost Tracking     │ • Examples   │
└─────────────────────┴─────────────────────┴─────────────────────┴──────────────┘
```

## Detailed Component Architecture

### 1. User Interface Layer

#### 🌐 Web UI (`src/api/templates/index.html`)
- **Purpose**: Browser-based interface for interactive query optimization
- **Features**: 
  - Real-time query input with syntax highlighting
  - Side-by-side result comparison
  - Performance metrics visualization
  - Test query library
- **Technology**: HTML5, Tailwind CSS, JavaScript, Prism.js

#### 💻 CLI Tool (`src/optimizer/main.py`)
- **Purpose**: Command-line interface for automation and scripting
- **Features**:
  - Single query optimization
  - Batch processing
  - File input/output
  - JSON/text/table output formats
- **Technology**: Click, Rich (for formatting)

#### 🐍 Python API (`src/optimizer/query_optimizer.py`)
- **Purpose**: Direct programmatic access for integration
- **Features**:
  - Object-oriented interface
  - Async support
  - Custom configuration
  - Exception handling

#### 📊 REST API (`src/api/routes.py`)
- **Purpose**: HTTP API for web services and integrations
- **Features**:
  - RESTful endpoints
  - JSON request/response
  - Batch operations
  - Status monitoring
- **Technology**: FastAPI, Pydantic, Uvicorn

### 2. Core Optimization Engine

#### 📊 Query Analyzer (`src/mcp_server/handlers.py`)
- **Purpose**: Parse and analyze SQL query structure
- **Capabilities**:
  - SQL parsing using sqlparse
  - Complexity assessment (Simple/Moderate/Complex/Very Complex)
  - Pattern identification (20+ patterns)
  - Performance issue detection
- **Output**: QueryAnalysis object with detailed metrics

#### 🤖 AI Optimizer (`src/optimizer/ai_optimizer.py`)
- **Purpose**: Apply Google's BigQuery best practices using AI
- **Capabilities**:
  - Gemini API integration
  - Context-aware optimization
  - Multi-pattern application
  - Documentation-backed suggestions
- **Technology**: Google Generative AI, structured prompting

#### ✅ Result Validator (`src/optimizer/validator.py`)
- **Purpose**: Ensure 100% functional accuracy
- **Capabilities**:
  - Query result comparison
  - Row-by-row validation
  - Performance measurement
  - Business logic preservation
- **Critical Requirement**: Zero tolerance for result differences

### 3. Knowledge & Data Layer

#### 📚 Documentation Crawler (`src/crawler/bigquery_docs_crawler.py`)
- **Purpose**: Harvest BigQuery optimization knowledge
- **Process**:
  1. Crawl Google Cloud BigQuery documentation
  2. Extract optimization patterns and best practices
  3. Convert HTML to structured markdown
  4. Cache locally for offline access
- **Output**: Structured documentation sections

#### 🗄️ Vector Database (`src/crawler/documentation_processor.py`)
- **Purpose**: Semantic search over documentation
- **Technology**: ChromaDB, Sentence Transformers
- **Capabilities**:
  - Embedding generation (all-MiniLM-L6-v2)
  - Similarity search
  - Context retrieval
  - Pattern matching

#### 🔍 Pattern Matcher (`src/common/models.py`)
- **Purpose**: Match queries to applicable optimization patterns
- **Features**:
  - 20+ distinct patterns
  - Priority scoring
  - Condition-based matching
  - Documentation linking

#### 📈 BigQuery Client (`src/optimizer/bigquery_client.py`)
- **Purpose**: Interface with BigQuery service
- **Capabilities**:
  - Query execution and validation
  - Performance metrics collection
  - Table metadata retrieval
  - Connection management

## Data Flow Architecture

### Optimization Request Flow

```
1. User Input
   ├── Query: "SELECT * FROM orders WHERE date > '2024-01-01'"
   ├── Configuration: project_id, validation settings
   └── Options: performance measurement, sample size

2. Query Analysis
   ├── Parse SQL structure
   ├── Identify tables, JOINs, subqueries
   ├── Assess complexity level
   ├── Detect performance issues
   └── Find applicable patterns

3. Context Gathering
   ├── Search documentation for relevant patterns
   ├── Retrieve table metadata from BigQuery
   ├── Build optimization context
   └── Prioritize optimization opportunities

4. AI Optimization
   ├── Send structured prompt to Gemini
   ├── Include query + analysis + documentation
   ├── Apply 20+ optimization patterns
   ├── Generate optimized query
   └── Provide detailed explanations

5. Validation & Measurement
   ├── Execute both original and optimized queries
   ├── Compare results row-by-row
   ├── Measure performance improvement
   ├── Verify business logic preservation
   └── Generate comprehensive report

6. Response Delivery
   ├── Optimization results with explanations
   ├── Performance metrics and improvements
   ├── Validation status and any issues
   └── Documentation references
```

### Documentation Processing Flow

```
1. Documentation Crawling
   ├── Fetch BigQuery documentation pages
   ├── Extract optimization content
   ├── Convert HTML to markdown
   └── Cache locally

2. Content Processing
   ├── Split into semantic chunks
   ├── Extract optimization patterns
   ├── Generate embeddings
   └── Store in vector database

3. Pattern Recognition
   ├── Identify 20+ optimization patterns
   ├── Map to query characteristics
   ├── Create applicability rules
   └── Link to documentation

4. Semantic Search
   ├── Query embedding generation
   ├── Similarity search in vector DB
   ├── Context retrieval
   └── Relevance scoring
```

## Success Metrics Architecture

### 1. Functional Accuracy (100% Target)
```
┌─────────────────────────────────────────┐
│           Validation Pipeline           │
├─────────────────────────────────────────┤
│ 1. Execute Original Query               │
│ 2. Execute Optimized Query              │
│ 3. Compare Results Row-by-Row           │
│ 4. Verify Identical Business Logic     │
│ 5. Report Any Differences              │
│                                         │
│ ✅ PASS: Results 100% Identical         │
│ ❌ FAIL: Any Difference Found           │
└─────────────────────────────────────────┘
```

### 2. Performance Improvement (30-50% Target)
```
┌─────────────────────────────────────────┐
│        Performance Measurement         │
├─────────────────────────────────────────┤
│ 1. Measure Original Query Time         │
│ 2. Measure Optimized Query Time        │
│ 3. Calculate Improvement Percentage    │
│ 4. Track Bytes Processed Reduction     │
│ 5. Monitor Cost Savings                │
│                                         │
│ 🎯 TARGET: 30-50% Improvement          │
│ 📊 ACTUAL: Measured per Query          │
└─────────────────────────────────────────┘
```

### 3. Documentation Coverage (20+ Patterns)
```
┌─────────────────────────────────────────┐
│         Pattern Coverage Matrix        │
├─────────────────────────────────────────┤
│ ✅ Column Pruning                       │
│ ✅ JOIN Reordering                      │
│ ✅ Subquery to JOIN Conversion          │
│ ✅ Approximate Aggregation              │
│ ✅ Window Function Optimization         │
│ ✅ Predicate Pushdown                   │
│ ✅ Clustering Optimization              │
│ ✅ Materialized View Suggestions        │
│ ✅ LIMIT Optimization                   │
│ ✅ UNION Optimization                   │
│ ✅ CASE WHEN Optimization               │
│ ✅ String Function Optimization         │
│ ✅ Date Function Optimization           │
│ ✅ Array Optimization                   │
│ ✅ STRUCT Optimization                  │
│ ✅ JSON Optimization                    │
│ ✅ Regular Expression Optimization      │
│ ✅ CTE Optimization                     │
│ ✅ HAVING to WHERE Conversion           │
│ ✅ CROSS JOIN Elimination               │
│ ✅ NULL Handling Optimization           │
│ ✅ DISTINCT Optimization                │
│                                         │
│ 📊 TOTAL: 22+ Distinct Patterns        │
└─────────────────────────────────────────┘
```

## Technology Stack

### Backend Technologies
- **Python 3.8+**: Core application language
- **FastAPI**: REST API framework
- **Pydantic**: Data validation and serialization
- **SQLParse**: SQL query parsing and analysis
- **Pandas**: Data manipulation and comparison

### AI & Machine Learning
- **Google Gemini API**: AI-powered query optimization
- **Sentence Transformers**: Text embeddings for semantic search
- **ChromaDB**: Vector database for documentation storage
- **NumPy**: Numerical computations

### Google Cloud Integration
- **BigQuery Client**: Query execution and metadata
- **Google Cloud Authentication**: Secure API access
- **BigQuery API**: Performance metrics and validation

### Frontend Technologies
- **HTML5**: Modern web interface
- **Tailwind CSS**: Utility-first styling
- **JavaScript (ES6+)**: Interactive functionality
- **Prism.js**: SQL syntax highlighting

### Development & Testing
- **pytest**: Comprehensive testing framework
- **Mock/Patch**: Unit testing with isolation
- **Coverage.py**: Code coverage measurement
- **Black/isort**: Code formatting
- **MyPy**: Type checking

## Deployment Architecture

### Local Development
```
┌─────────────────────────────────────────┐
│         Developer Machine               │
├─────────────────────────────────────────┤
│ • Python Virtual Environment           │
│ • Local ChromaDB Storage               │
│ • Cached Documentation                 │
│ • Development Server (Port 8080)       │
│ • Google Cloud Credentials             │
└─────────────────────────────────────────┘
```

### Production Deployment
```
┌─────────────────────────────────────────┐
│           Cloud Infrastructure          │
├─────────────────────────────────────────┤
│ • Container Orchestration (K8s/Docker) │
│ • Load Balancer                         │
│ • Auto-scaling Groups                  │
│ • Persistent Vector Database           │
│ • Monitoring & Logging                 │
│ • Security & Authentication            │
└─────────────────────────────────────────┘
```

## Security Architecture

### Authentication & Authorization
```
┌─────────────────────────────────────────┐
│            Security Layer               │
├─────────────────────────────────────────┤
│ • Google Cloud IAM Integration         │
│ • Service Account Authentication       │
│ • API Key Management (Gemini)          │
│ • Role-Based Access Control            │
│ • Audit Logging                        │
│ • Data Privacy Protection              │
└─────────────────────────────────────────┘
```

### Data Protection
- **No Query Storage**: Queries processed in memory only
- **Secure Transmission**: HTTPS/TLS for all communications
- **Credential Management**: Secure handling of API keys
- **Access Control**: BigQuery IAM integration
- **Audit Trail**: Comprehensive logging

## Scalability Architecture

### Horizontal Scaling
```
┌─────────────────────────────────────────┐
│          Load Distribution              │
├─────────────────────────────────────────┤
│ • Multiple API Server Instances        │
│ • Shared Vector Database               │
│ • Distributed Caching                 │
│ • Queue-based Batch Processing        │
│ • Auto-scaling Based on Load          │
└─────────────────────────────────────────┘
```

### Performance Optimization
- **Caching Strategy**: Documentation and embeddings cached
- **Connection Pooling**: Efficient BigQuery connections
- **Async Processing**: Non-blocking operations
- **Batch Operations**: Concurrent query processing
- **Resource Management**: Memory and CPU optimization

## Monitoring & Observability

### System Health Monitoring
```
┌─────────────────────────────────────────┐
│           Health Dashboard              │
├─────────────────────────────────────────┤
│ • BigQuery Connection Status           │
│ • Gemini API Availability             │
│ • Documentation Freshness             │
│ • Vector Database Health               │
│ • Performance Metrics                 │
│ • Error Rates & Alerts                │
└─────────────────────────────────────────┘
```

### Key Performance Indicators
- **Optimization Success Rate**: % of queries successfully optimized
- **Average Performance Improvement**: Mean improvement across all queries
- **Functional Accuracy Rate**: % of optimizations preserving business logic
- **System Response Time**: End-to-end processing time
- **Documentation Coverage**: Number of patterns and references

This architecture ensures robust, scalable, and reliable query optimization while maintaining the critical requirements of functional accuracy and performance improvement.