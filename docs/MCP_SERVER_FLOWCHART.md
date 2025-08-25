# 🔄 MCP Server - Complete Workflow Flowchart

## 🎯 **What is the MCP Server?**

The **MCP (Model Context Protocol) Server** is the **core workflow orchestrator** that acts as a bridge between:
- **Frontend UI** (user interface)
- **Gemini AI API** (AI optimization)
- **BigQuery** (database execution)
- **Validation Engine** (syntax, schema, and LLM cleanup)

It's essentially the **"brain"** that coordinates the entire SQL optimization process.

## 🔄 **Complete MCP Server Workflow Flowchart**

```mermaid
flowchart TD
    %% Start
    START([🚀 User Submits SQL Query]) --> INIT[📥 MCP Server Receives Request]
    
    %% Initialization Phase
    INIT --> LOAD_ENV[🔑 Load Environment Variables<br/>GEMINI_API_KEY, Project Settings]
    LOAD_ENV --> INIT_HANDLER[⚙️ Initialize DirectSQLOptimizationHandler]
    INIT_HANDLER --> VALIDATE_INPUT[✅ Validate Input Parameters<br/>SQL Query, Project ID, Flags]
    
    %% AI Optimization Phase
    VALIDATE_INPUT --> LOAD_DOCS[📚 Load Markdown Documentation<br/>From optimization_docs_md/ folder]
    LOAD_DOCS --> CHECK_TOKENS{🔍 Check Token Count<br/>Documentation + Query}
    
    %% Token Management Branch
    CHECK_TOKENS -->|Token Count > Limit| TRIM_DOCS[✂️ Apply Token Reduction Strategy<br/>1. Intelligent Selection<br/>2. Minimal Mode<br/>3. Ultra-Minimal Mode]
    CHECK_TOKENS -->|Token Count OK| PREPARE_PROMPT[📝 Prepare Gemini Prompts]
    TRIM_DOCS --> PREPARE_PROMPT
    
    %% Gemini API Interaction
    PREPARE_PROMPT --> SEND_TO_GEMINI[🤖 Send to Gemini 2.5 Pro API<br/>System Prompt + User Prompt + Docs]
    SEND_TO_GEMINI --> GEMINI_RESPONSE{🔄 Gemini Response Status}
    
    %% Gemini Response Handling
    GEMINI_RESPONSE -->|Success| EXTRACT_QUERY[📤 Extract Optimized Query<br/>Parse Gemini Response]
    GEMINI_RESPONSE -->|Failure| GEMINI_FALLBACK[⚠️ Apply Fallback Strategy<br/>Return Original Query + Error]
    GEMINI_FALLBACK --> VALIDATION_PIPELINE
    
    %% Multi-Stage Validation Pipeline
    EXTRACT_QUERY --> VALIDATION_PIPELINE[🔍 Start Multi-Stage Validation]
    
    %% Step 3: Regex Syntax Fixes
    VALIDATION_PIPELINE --> REGEX_FIX[🔧 Step 3: Regex Syntax Fixes]
    REGEX_FIX --> FIX_SPACES[📝 Fix Missing Spaces<br/>WHEREder_date → WHERE der_date]
    REGEX_FIX --> FIX_KEYWORDS[🔑 Fix Corrupted Keywords<br/>OR DER BY → ORDER BY]
    REGEX_FIX --> FIX_QUOTES[💬 Fix Unbalanced Quotes<br/>Add missing closing quotes]
    REGEX_FIX --> FIX_COMPARISONS[⚖️ Fix Malformed Comparisons<br/>>= abc → >= 1]
    
    %% Combine Regex Fixes
    FIX_SPACES --> COMBINE_REGEX_FIXES[🔄 Combine All Regex Fixes]
    FIX_KEYWORDS --> COMBINE_REGEX_FIXES
    FIX_QUOTES --> COMBINE_REGEX_FIXES
    FIX_COMPARISONS --> COMBINE_REGEX_FIXES
    
    %% Step 4: First LLM Cleanup
    COMBINE_REGEX_FIXES --> LLM_CLEANUP_1[🧠 Step 4: LLM Cleanup #1]
    LLM_CLEANUP_1 --> SEND_TO_LLM_1[📤 Send to Gemini for Cleanup<br/>Fix NULL columns, invalid WHERE conditions]
    SEND_TO_LLM_1 --> LLM_RESPONSE_1{🔄 LLM Response #1}
    LLM_RESPONSE_1 -->|Success| CLEANED_QUERY_1[✅ Query After First Cleanup]
    LLM_RESPONSE_1 -->|Failure| USE_REGEX_RESULT[⚠️ Use Regex-Fixed Query<br/>Skip LLM Cleanup #1]
    USE_REGEX_RESULT --> CLEANED_QUERY_1
    
    %% Step 5: Schema Validation
    CLEANED_QUERY_1 --> SCHEMA_VALIDATION[🏗️ Step 5: Schema Validation]
    SCHEMA_VALIDATION --> CHECK_TABLES[📋 Check Table Existence<br/>Validate FROM and JOIN tables]
    SCHEMA_VALIDATION --> CHECK_COLUMNS[🔍 Check Column Existence<br/>Validate SELECT, WHERE, JOIN columns]
    SCHEMA_VALIDATION --> REMOVE_INVALID[❌ Remove Invalid References<br/>Non-existent tables/columns]
    SCHEMA_VALIDATION --> VALIDATE_JOINS[🔗 Validate JOIN Conditions<br/>Check JOIN syntax and references]
    
    %% Combine Schema Validation
    CHECK_TABLES --> COMBINE_SCHEMA_VAL[🔄 Combine Schema Validation Results]
    CHECK_COLUMNS --> COMBINE_SCHEMA_VAL
    REMOVE_INVALID --> COMBINE_SCHEMA_VAL
    VALIDATE_JOINS --> COMBINE_SCHEMA_VAL
    
    %% Step 6: Final LLM Cleanup
    COMBINE_SCHEMA_VAL --> LLM_CLEANUP_2[🧠 Step 6: Final LLM Cleanup]
    LLM_CLEANUP_2 --> SEND_TO_LLM_2[📤 Send to Gemini for Final Cleanup<br/>Fix remaining syntax, remove NULL conditions]
    SEND_TO_LLM_2 --> LLM_RESPONSE_2{🔄 LLM Response #2}
    LLM_RESPONSE_2 -->|Success| FINAL_OPTIMIZED_QUERY[✅ Final Optimized Query]
    LLM_RESPONSE_2 -->|Failure| USE_SCHEMA_RESULT[⚠️ Use Schema-Validated Query<br/>Skip Final LLM Cleanup]
    USE_SCHEMA_RESULT --> FINAL_OPTIMIZED_QUERY
    
    %% Execution Phase
    FINAL_OPTIMIZED_QUERY --> EXECUTION_PHASE[⚡ Phase 4: Query Execution]
    EXECUTION_PHASE --> EXECUTE_ORIGINAL[📊 Execute Original Query<br/>Collect performance metrics]
    EXECUTION_PHASE --> EXECUTE_OPTIMIZED[🚀 Execute Optimized Query<br/>Collect performance metrics]
    
    %% Performance Metrics Collection
    EXECUTE_ORIGINAL --> COLLECT_METRICS_ORIG[📈 Collect Original Metrics<br/>Time, Bytes, Cost, Rows]
    EXECUTE_OPTIMIZED --> COLLECT_METRICS_OPT[📈 Collect Optimized Metrics<br/>Time, Bytes, Cost, Rows]
    
    %% Comparison Phase
    COLLECT_METRICS_ORIG --> COMPARISON_PHASE[📊 Phase 5: Result Comparison]
    COLLECT_METRICS_OPT --> COMPARISON_PHASE
    
    %% Hash-Based Validation
    COMPARISON_PHASE --> HASH_VALIDATION[🔐 Hash-Based Validation]
    HASH_VALIDATION --> GENERATE_HASHES[🔑 Generate MD5 Hashes<br/>Original Results + Optimized Results]
    GENERATE_HASHES --> COMPARE_HASHES[⚖️ Compare Hash Values<br/>Check if results are identical]
    
    %% Result Analysis
    COMPARE_HASHES --> RESULT_ANALYSIS[📋 Result Analysis]
    RESULT_ANALYSIS --> ROW_COUNT_CHECK[🔢 Row Count Validation<br/>Check if row counts match]
    RESULT_ANALYSIS --> DATA_STRUCTURE_CHECK[🏗️ Data Structure Validation<br/>Check column names, types]
    RESULT_ANALYSIS --> BUSINESS_LOGIC_CHECK[💼 Business Logic Preservation<br/>Check if semantics are preserved]
    
    %% Performance Analysis
    RESULT_ANALYSIS --> PERFORMANCE_ANALYSIS[📊 Performance Analysis]
    PERFORMANCE_ANALYSIS --> CALCULATE_IMPROVEMENTS[📈 Calculate Improvements<br/>Time, Bytes, Cost savings]
    PERFORMANCE_ANALYSIS --> GENERATE_METRICS[📊 Generate Performance Metrics<br/>Actual vs Expected improvements]
    
    %% Response Generation
    CALCULATE_IMPROVEMENTS --> GENERATE_RESPONSE[📤 Generate Unified Response]
    GENERATE_METRICS --> GENERATE_RESPONSE
    
    %% Response Structure
    GENERATE_RESPONSE --> RESPONSE_STRUCTURE[📋 Build Response Object]
    RESPONSE_STRUCTURE --> ADD_QUERIES[➕ Add Original & Optimized Queries]
    RESPONSE_STRUCTURE --> ADD_RESULTS[➕ Add Query Results & Metrics]
    RESPONSE_STRUCTURE --> ADD_VALIDATION[➕ Add Validation Results<br/>Hash comparison, preservation score]
    RESPONSE_STRUCTURE --> ADD_PERFORMANCE[➕ Add Performance Analysis<br/>Actual improvements, optimization details]
    
    %% Final Response
    ADD_QUERIES --> FINAL_RESPONSE[🎯 Final Unified Response]
    ADD_RESULTS --> FINAL_RESPONSE
    ADD_VALIDATION --> FINAL_RESPONSE
    ADD_PERFORMANCE --> FINAL_RESPONSE
    
    %% Return to API
    FINAL_RESPONSE --> RETURN_TO_API[📤 Return Response to API Gateway]
    RETURN_TO_API --> END([🏁 MCP Server Workflow Complete])
    
    %% Error Handling Paths
    GEMINI_FALLBACK --> ERROR_HANDLING[⚠️ Error Handling]
    USE_REGEX_RESULT --> ERROR_HANDLING
    USE_SCHEMA_RESULT --> ERROR_HANDLING
    ERROR_HANDLING --> RETURN_TO_API
    
    %% Styling
    classDef startEnd fill:#e8f5e8,stroke:#1b5e20,stroke-width:3px
    classDef mcpProcess fill:#e3f2fd,stroke:#0277bd,stroke-width:2px
    classDef aiProcess fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef validationProcess fill:#fce4ec,stroke:#880e4f,stroke-width:2px
    classDef executionProcess fill:#e0f2f1,stroke:#004d40,stroke-width:2px
    classDef comparisonProcess fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef responseProcess fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef errorProcess fill:#ffebee,stroke:#c62828,stroke-width:2px
    
    class START,END startEnd
    class INIT,LOAD_ENV,INIT_HANDLER,VALIDATE_INPUT,LOAD_DOCS,CHECK_TOKENS,TRIM_DOCS,PREPARE_PROMPT mcpProcess
    class SEND_TO_GEMINI,GEMINI_RESPONSE,EXTRACT_QUERY,SEND_TO_LLM_1,LLM_CLEANUP_1,LLM_RESPONSE_1,SEND_TO_LLM_2,LLM_CLEANUP_2,LLM_RESPONSE_2 aiProcess
    class VALIDATION_PIPELINE,REGEX_FIX,FIX_SPACES,FIX_KEYWORDS,FIX_QUOTES,FIX_COMPARISONS,COMBINE_REGEX_FIXES,LLM_CLEANUP_1,CLEANED_QUERY_1,SCHEMA_VALIDATION,CHECK_TABLES,CHECK_COLUMNS,REMOVE_INVALID,VALIDATE_JOINS,COMBINE_SCHEMA_VAL,LLM_CLEANUP_2,FINAL_OPTIMIZED_QUERY validationProcess
    class EXECUTION_PHASE,EXECUTE_ORIGINAL,EXECUTE_OPTIMIZED,COLLECT_METRICS_ORIG,COLLECT_METRICS_OPT executionProcess
    class COMPARISON_PHASE,HASH_VALIDATION,GENERATE_HASHES,COMPARE_HASHES,RESULT_ANALYSIS,ROW_COUNT_CHECK,DATA_STRUCTURE_CHECK,BUSINESS_LOGIC_CHECK,PERFORMANCE_ANALYSIS,CALCULATE_IMPROVEMENTS,GENERATE_METRICS comparisonProcess
    class GENERATE_RESPONSE,RESPONSE_STRUCTURE,ADD_QUERIES,ADD_RESULTS,ADD_VALIDATION,ADD_PERFORMANCE,FINAL_RESPONSE,RETURN_TO_API responseProcess
    class GEMINI_FALLBACK,USE_REGEX_RESULT,USE_SCHEMA_RESULT,ERROR_HANDLING errorProcess
```

## 🔍 **Detailed MCP Server Responsibilities**

### **1. 🎯 Workflow Orchestration**
- **Coordinates** all optimization steps
- **Manages** the flow between different phases
- **Handles** state transitions and error conditions
- **Ensures** consistent processing for all request types

### **2. 🤖 AI Integration Management**
- **Initializes** Gemini API client
- **Manages** token limits and documentation loading
- **Handles** AI API failures gracefully
- **Implements** fallback strategies

### **3. 🔍 Multi-Stage Validation**
- **Orchestrates** the 6-step validation pipeline
- **Coordinates** between regex fixes and LLM cleanup
- **Manages** schema validation against BigQuery
- **Ensures** query quality at each step

### **4. ⚡ Execution Management**
- **Coordinates** BigQuery query execution
- **Collects** performance metrics
- **Handles** execution errors
- **Manages** result collection

### **5. 📊 Analysis & Comparison**
- **Performs** hash-based result validation
- **Calculates** performance improvements
- **Analyzes** result preservation
- **Generates** comprehensive metrics

### **6. 📤 Response Generation**
- **Builds** unified response objects
- **Structures** data for frontend consumption
- **Handles** error cases gracefully
- **Ensures** consistent response format

## 🏗️ **MCP Server Architecture Components**

```mermaid
graph TB
    subgraph "MCP Server Core"
        MAIN[🎯 Main Workflow Controller<br/>DirectSQLOptimizationHandler]
        AI_MGR[🤖 AI Integration Manager<br/>Gemini Client Management]
        VAL_MGR[🔍 Validation Manager<br/>Multi-Stage Pipeline]
        EXEC_MGR[⚡ Execution Manager<br/>BigQuery Operations]
        COMP_MGR[📊 Comparison Manager<br/>Result Analysis]
    end
    
    subgraph "External Dependencies"
        GEMINI[🤖 Gemini 2.5 Pro API]
        BQ[⚡ BigQuery Client]
        DOCS[📚 Markdown Documentation]
        ENV[🔑 Environment Variables]
    end
    
    subgraph "Internal Services"
        TOKEN_MGR[🔢 Token Management<br/>Documentation Trimming]
        ERROR_HANDLER[⚠️ Error Handler<br/>Fallback Strategies]
        RESPONSE_BUILDER[📤 Response Builder<br/>Data Structuring]
        LOGGER[📝 Logger<br/>Workflow Tracking]
    end
    
    %% Core Flow
    MAIN --> AI_MGR
    MAIN --> VAL_MGR
    MAIN --> EXEC_MGR
    MAIN --> COMP_MGR
    
    %% AI Integration
    AI_MGR --> GEMINI
    AI_MGR --> TOKEN_MGR
    AI_MGR --> DOCS
    
    %% Validation
    VAL_MGR --> AI_MGR
    VAL_MGR --> ERROR_HANDLER
    
    %% Execution
    EXEC_MGR --> BQ
    EXEC_MGR --> ERROR_HANDLER
    
    %% Comparison
    COMP_MGR --> RESPONSE_BUILDER
    
    %% Environment & Logging
    MAIN --> ENV
    MAIN --> LOGGER
    
    %% Response
    MAIN --> RESPONSE_BUILDER
    
    style MAIN fill:#e8f5e8,stroke:#1b5e20,stroke-width:3px
    style AI_MGR fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style VAL_MGR fill:#fce4ec,stroke:#880e4f,stroke-width:2px
    style EXEC_MGR fill:#e0f2f1,stroke:#004d40,stroke-width:2px
    style COMP_MGR fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    style TOKEN_MGR fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    style ERROR_HANDLER fill:#ffebee,stroke:#c62828,stroke-width:2px
    style RESPONSE_BUILDER fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    style LOGGER fill:#f1f8e9,stroke:#33691e,stroke-width:2px
```

## 🎯 **Key MCP Server Features**

### **🔄 Unified Processing**
- **Single Entry Point**: All optimization requests go through the same workflow
- **Consistent Behavior**: Identical processing for single queries and test suites
- **Predictable Results**: Same validation and execution logic

### **🛡️ Robust Error Handling**
- **Graceful Degradation**: Continues processing even if some steps fail
- **Fallback Strategies**: Multiple approaches for handling failures
- **Comprehensive Logging**: Detailed tracking of all operations

### **⚡ Performance Optimization**
- **Token Management**: Intelligent documentation loading
- **Parallel Processing**: Where possible, operations run concurrently
- **Resource Management**: Efficient use of API calls and database connections

### **🔍 Quality Assurance**
- **Multi-Stage Validation**: Comprehensive query checking
- **Result Preservation**: Ensures optimized queries return identical results
- **Performance Monitoring**: Real-time metrics collection and analysis

The MCP Server is essentially the **"command center"** that makes the entire BigQuery optimization system work seamlessly! 🚀 