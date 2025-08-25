# BigQuery Query Optimizer

A comprehensive AI-powered BigQuery SQL query optimization tool that combines Google's Gemini AI with BigQuery best practices to deliver significant performance improvements.

## 🚀 Features

### Unified SQL Optimization Workflow
- **Single Button Interface**: One "🚀 Optimize Query" button handles the entire optimization process
- **AI-Powered Optimization**: Uses Google's Gemini API to analyze and optimize SQL queries
- **Smart Documentation Selection**: Intelligently selects relevant optimization patterns based on query content
- **Token Limit Management**: Automatically handles large documentation sets within Gemini's token limits
- **Comprehensive Validation**: Schema validation, query execution, and result comparison
- **Performance Metrics**: Detailed performance analysis and improvement measurements

### Core Capabilities
- **Raw SQL Processing**: Sends SQL queries directly to MCP without intermediate validation
- **Markdown Documentation Integration**: Loads optimization patterns from `data/optimization_docs_md/` folder
- **Intelligent Content Selection**: Prioritizes relevant documentation based on query analysis
- **Token-Aware Processing**: Automatically truncates content to stay within API limits
- **Result Validation**: Uses hashing to compare original vs. optimized query results
- **Performance Comparison**: Executes both queries and measures actual performance improvements

## 🏗️ Architecture

### API Endpoints
- **`/api/v1/optimize-gemini`**: Main optimization endpoint using Gemini AI
- **`/api/v1/validate-schemas`**: Validates query schemas and table references
- **`/api/v1/execute-and-compare`**: Executes both queries and compares results

### Token Limit Management
The system automatically handles Gemini's token limits (1M tokens) through:

1. **Smart Content Selection**: Prioritizes documentation based on query relevance
2. **Intelligent Truncation**: Truncates content at sentence boundaries when needed
3. **Minimal Mode**: For very long queries, uses essential optimization patterns only
4. **Token Estimation**: Pre-checks limits before sending to Gemini API

### Content Prioritization
Documentation files are scored based on:
- **Query Relevance**: Matches between SQL keywords and documentation content
- **Pattern Importance**: Core optimization patterns get higher priority
- **Content Length**: Shorter, focused files are preferred
- **Examples**: Files with practical examples get bonus points

## 📁 Project Structure

```
BigQuery-Opt/
├── src/
│   ├── api/                    # FastAPI web server
│   ├── mcp_server/            # Model Context Protocol server
│   │   ├── handlers.py        # SQL optimization logic
│   │   └── server.py          # MCP server implementation
│   └── optimizer/             # Core optimization engine
├── data/
│   └── optimization_docs_md/  # Markdown optimization patterns
├── config/
│   └── settings.py            # Configuration and environment variables
└── tests/                     # Test suite
```

## 🛠️ Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables
Create a `.env` file in the project root:
```bash
# Required for AI optimization
GEMINI_API_KEY=your_actual_gemini_api_key_here

# Optional settings
GOOGLE_CLOUD_PROJECT=your_project_id_here
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
DEBUG=false
LOG_LEVEL=INFO
```

### 3. Start the Server
```bash
python run_api_server.py
```

The server will be available at:
- **Web UI**: http://localhost:8080/
- **API Docs**: http://localhost:8080/docs
- **Health Check**: http://localhost:8080/health

## 🧪 Testing

### Test Environment Variables
```bash
python test_env_loading.py
```

### Test Token Limits
```bash
python test_token_limits.py
```

### Test Full Workflow
```bash
python test_unified_workflow.py
```

## 🔧 Configuration

### Token Limits
- **Maximum Input Tokens**: 1,000,000 (Gemini 1.5 Flash limit)
- **Documentation Reserve**: 800,000 tokens
- **Query & Prompts Reserve**: 200,000 tokens
- **Smart Truncation**: Content is truncated at sentence boundaries when needed

### Content Selection Strategy
- **High Priority**: Performance, optimization, best-practice patterns
- **Medium Priority**: Join, partition, cluster, index, aggregation techniques
- **Lower Priority**: Overview and introduction documentation
- **Automatic Fallback**: Minimal essential patterns for very long queries

## 🚨 Troubleshooting

### Common Issues

#### Token Limit Exceeded
**Error**: `Input exceeds Gemini's token limit`
**Solution**: The system automatically handles this by:
- Prioritizing relevant documentation
- Truncating content intelligently
- Using minimal patterns for long queries

#### Gemini API Not Initialized
**Error**: `Gemini API not initialized`
**Solution**: 
1. Check your `.env` file has `GEMINI_API_KEY`
2. Run `python test_env_loading.py` to verify
3. Ensure `python-dotenv` is installed

#### Import Errors
**Error**: `No module named 'google.generativeai'`
**Solution**: Install the required package:
```bash
pip install google-generativeai
```

### Performance Optimization
- **Documentation Size**: Keep markdown files focused and concise
- **Query Length**: Very long queries automatically use minimal documentation
- **Content Relevance**: System prioritizes most relevant optimization patterns
- **Token Efficiency**: Content is automatically optimized for token usage

## 📊 Usage Examples

### Basic Optimization
1. Enter your SQL query in the web interface
2. Click "🚀 Optimize Query"
3. View the AI-generated optimization suggestions
4. Review performance improvements and validation results

### Advanced Features
- **Schema Validation**: Automatically validates table and column references
- **Result Comparison**: Compares original vs. optimized query results using hashing
- **Performance Metrics**: Measures actual execution time improvements
- **Documentation Context**: Shows which optimization patterns were applied

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section above
2. Run the test scripts to diagnose problems
3. Review the API documentation at `/docs`
4. Check the logs for detailed error information