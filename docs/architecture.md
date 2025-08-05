# BigQuery Query Optimizer Architecture

## Overview

The BigQuery Query Optimizer is an AI-powered system that automatically optimizes BigQuery SQL queries while preserving exact business logic and results. The system combines documentation crawling, semantic search, AI-powered optimization, and comprehensive validation to deliver performance improvements of 30-50%.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    BigQuery Query Optimizer                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐ │
│  │   CLI/API       │    │   Web UI        │    │   Batch         │ │
│  │   Interface     │    │   (Future)      │    │   Processing    │ │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘ │
│           │                       │                       │        │
│           └───────────────────────┼───────────────────────┘        │
│                                   │                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              Query Optimizer Core                          │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │   │
│  │  │   Query     │  │    AI       │  │     Validator       │ │   │
│  │  │  Analyzer   │  │ Optimizer   │  │                     │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│           │                       │                       │        │
│           │                       │                       │        │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐ │
│  │      MCP        │    │  Documentation │    │    BigQuery     │ │
│  │     Server      │    │   Processor     │    │     Client      │ │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘ │
│           │                       │                       │        │
│           │                       │                       │        │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐ │
│  │   Vector DB     │    │  Documentation │    │   BigQuery      │ │
│  │   (ChromaDB)    │    │    Crawler     │    │   Service       │ │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘ │
│                                   │                                │
│                          ┌─────────────────┐                       │
│                          │  Google Cloud   │                       │
│                          │ Documentation   │                       │
│                          └─────────────────┘                       │
└─────────────────────────────────────────────────────────────────┘

External Services:
┌─────────────────┐    ┌─────────────────┐
│   Gemini API    │    │   BigQuery      │
│   (Google AI)   │    │   Service       │
└─────────────────┘    └─────────────────┘
```

## Core Components

### 1. Documentation Crawler (`src/crawler/`)

**Purpose**: Crawls and processes BigQuery optimization documentation from Google Cloud.

**Key Components**:
- `BigQueryDocsCrawler`: Main crawler that fetches documentation pages
- `DocumentationProcessor`: Processes and creates embeddings for semantic search

**Features**:
- Respects rate limits with configurable delays
- Caches documentation locally to avoid repeated requests
- Extracts optimization patterns from documentation
- Creates searchable embeddings using sentence transformers

**Flow**:
1. Crawls predefined BigQuery documentation URLs
2. Extracts and cleans HTML content
3. Converts to markdown format
4. Identifies optimization patterns in content
5. Creates embeddings and stores in vector database

### 2. MCP Server (`src/mcp_server/`)

**Purpose**: Model Context Protocol server that provides documentation and optimization suggestions.

**Key Components**:
- `BigQueryMCPServer`: FastAPI-based server
- `DocumentationHandler`: Handles documentation search requests
- `OptimizationHandler`: Provides query analysis and optimization suggestions

**API Endpoints**:
- `POST /search`: Search documentation semantically
- `POST /patterns`: Get applicable optimization patterns
- `POST /analyze`: Analyze query structure and complexity
- `POST /optimize`: Get detailed optimization suggestions
- `GET /health`: Health check and system status

### 3. Query Optimizer (`src/optimizer/`)

**Purpose**: Main optimization engine that coordinates all components.

**Key Components**:
- `BigQueryOptimizer`: Main orchestrator class
- `GeminiQueryOptimizer`: AI-powered optimization using Gemini
- `BigQueryClient`: BigQuery service wrapper with performance measurement
- `QueryValidator`: Ensures optimized queries return identical results

**Optimization Flow**:
1. **Analysis**: Parse and analyze SQL query structure
2. **Pattern Matching**: Identify applicable optimization patterns
3. **Context Gathering**: Retrieve relevant documentation
4. **AI Optimization**: Use Gemini to generate optimized query
5. **Validation**: Verify results are identical (optional)
6. **Performance Measurement**: Compare execution times (optional)

### 4. Common Components (`src/common/`)

**Purpose**: Shared utilities and data models.

**Key Components**:
- `models.py`: Pydantic data models for all system entities
- `exceptions.py`: Custom exception classes
- `logger.py`: Structured logging utilities

## Data Models

### Core Models

#### `OptimizationResult`
Complete result of the optimization process including:
- Original and optimized queries
- Applied optimizations with explanations
- Performance metrics and validation results
- Processing metadata

#### `QueryAnalysis`
Detailed analysis of SQL query structure:
- Complexity assessment
- Table, JOIN, and function counts
- Identified performance issues
- Applicable optimization patterns

#### `OptimizationPattern`
Represents a specific optimization technique:
- Pattern identification and description
- Expected performance improvement
- Applicability conditions
- Documentation references

#### `PerformanceMetrics`
Performance measurement data:
- Execution time and resource usage
- Bytes processed and billed
- Cache hit information

## AI Integration

### Gemini API Integration

The system uses Google's Gemini AI model for intelligent query optimization:

1. **Context Building**: Combines query analysis, applicable patterns, and relevant documentation
2. **Prompt Engineering**: Structured prompts that ensure consistent, high-quality outputs
3. **Response Processing**: Parses AI responses and validates optimization suggestions
4. **Error Handling**: Graceful fallbacks when AI services are unavailable

### Optimization Patterns

The system recognizes and applies 20+ optimization patterns:

- **JOIN Reordering**: Optimize JOIN order based on table sizes
- **Partition Filtering**: Add partition filters to reduce data scanned
- **Subquery Conversion**: Convert subqueries to JOINs where appropriate
- **Window Function Optimization**: Improve window function specifications
- **Approximate Aggregation**: Use approximate functions for large datasets
- **Column Pruning**: Replace SELECT * with specific columns
- **Predicate Pushdown**: Move filters closer to data sources
- **Clustering Optimization**: Leverage clustering keys in WHERE clauses

## Performance and Scalability

### Performance Optimization

1. **Caching**: Documentation and embeddings are cached locally
2. **Batch Processing**: Support for optimizing multiple queries concurrently
3. **Async Operations**: Non-blocking operations where possible
4. **Connection Pooling**: Efficient BigQuery connection management

### Scalability Considerations

1. **Stateless Design**: All components are stateless for horizontal scaling
2. **Resource Management**: Configurable resource limits and timeouts
3. **Error Isolation**: Component failures don't cascade
4. **Monitoring**: Comprehensive logging and metrics

## Security and Privacy

### Data Handling

1. **No Query Storage**: Queries are processed in memory only
2. **Secure Connections**: All external API calls use HTTPS/TLS
3. **Credential Management**: Secure handling of API keys and service accounts
4. **Audit Logging**: All operations are logged for security auditing

### Access Control

1. **API Authentication**: MCP server supports authentication
2. **Role-Based Access**: Integration with Google Cloud IAM
3. **Rate Limiting**: Protection against abuse

## Configuration and Deployment

### Environment Configuration

The system uses environment variables and configuration files:
- Google Cloud project and credentials
- Gemini API configuration
- BigQuery settings and preferences
- Performance and logging parameters

### Deployment Options

1. **Local Development**: Run all components locally
2. **Container Deployment**: Docker containers for easy deployment
3. **Cloud Deployment**: Deploy to Google Cloud Run or Kubernetes
4. **Hybrid Deployment**: MCP server in cloud, CLI tools local

## Monitoring and Observability

### Logging

Structured logging using `structlog`:
- Query analysis and optimization events
- Performance metrics and timing
- Error tracking and debugging information
- API request/response logging

### Metrics

Key performance indicators:
- Optimization success rate
- Average performance improvement
- Processing time per query
- API response times
- Error rates by component

### Health Checks

Comprehensive health monitoring:
- BigQuery connectivity
- Gemini API availability
- Documentation freshness
- Vector database status

## Testing Strategy

### Test Categories

1. **Unit Tests**: Individual component testing with mocks
2. **Integration Tests**: End-to-end workflow testing
3. **Performance Tests**: Optimization effectiveness validation
4. **Functional Tests**: Result accuracy verification

### Test Coverage

- Query analysis accuracy
- Optimization pattern identification
- AI integration reliability
- Performance measurement precision
- Error handling robustness

## Future Enhancements

### Planned Features

1. **Web Interface**: Browser-based query optimization
2. **Query Recommendation**: Proactive optimization suggestions
3. **Cost Analysis**: Detailed cost impact analysis
4. **Custom Patterns**: User-defined optimization patterns
5. **Batch Analytics**: Analysis of query patterns across organizations

### Scalability Improvements

1. **Distributed Processing**: Multi-node query processing
2. **Advanced Caching**: Redis-based distributed caching
3. **Machine Learning**: Custom ML models for pattern recognition
4. **Real-time Optimization**: Stream processing for continuous optimization

This architecture provides a robust, scalable foundation for AI-powered BigQuery query optimization while maintaining flexibility for future enhancements and deployment scenarios.