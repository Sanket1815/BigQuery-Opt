"""Custom exceptions for BigQuery Query Optimizer."""


class QueryOptimizerError(Exception):
    """Base exception for all query optimizer errors."""
    
    def __init__(self, message: str, details: str = None):
        self.message = message
        self.details = details
        super().__init__(self.message)
    
    def __str__(self):
        if self.details:
            return f"{self.message}: {self.details}"
        return self.message


class QueryParsingError(QueryOptimizerError):
    """Exception raised when SQL query parsing fails."""
    
    def __init__(self, message: str, query: str = None, line_number: int = None):
        self.query = query
        self.line_number = line_number
        details = []
        if query:
            details.append(f"Query: {query[:100]}...")
        if line_number:
            details.append(f"Line: {line_number}")
        super().__init__(message, " | ".join(details) if details else None)


class OptimizationError(QueryOptimizerError):
    """Exception raised when query optimization fails."""
    
    def __init__(self, message: str, pattern_id: str = None, original_query: str = None):
        self.pattern_id = pattern_id
        self.original_query = original_query
        details = []
        if pattern_id:
            details.append(f"Pattern: {pattern_id}")
        if original_query:
            details.append(f"Query: {original_query[:100]}...")
        super().__init__(message, " | ".join(details) if details else None)


class BigQueryConnectionError(QueryOptimizerError):
    """Exception raised when BigQuery connection fails."""
    
    def __init__(self, message: str, project_id: str = None):
        self.project_id = project_id
        details = f"Project: {project_id}" if project_id else None
        super().__init__(message, details)


class DocumentationCrawlerError(QueryOptimizerError):
    """Exception raised when documentation crawling fails."""
    
    def __init__(self, message: str, url: str = None):
        self.url = url
        details = f"URL: {url}" if url else None
        super().__init__(message, details)


class MCPServerError(QueryOptimizerError):
    """Exception raised when MCP server operations fail."""
    
    def __init__(self, message: str, endpoint: str = None, status_code: int = None):
        self.endpoint = endpoint
        self.status_code = status_code
        details = []
        if endpoint:
            details.append(f"Endpoint: {endpoint}")
        if status_code:
            details.append(f"Status: {status_code}")
        super().__init__(message, " | ".join(details) if details else None)


class ValidationError(QueryOptimizerError):
    """Exception raised when query validation fails."""
    
    def __init__(self, message: str, original_result_count: int = None, optimized_result_count: int = None):
        self.original_result_count = original_result_count
        self.optimized_result_count = optimized_result_count
        details = []
        if original_result_count is not None:
            details.append(f"Original rows: {original_result_count}")
        if optimized_result_count is not None:
            details.append(f"Optimized rows: {optimized_result_count}")
        super().__init__(message, " | ".join(details) if details else None)


class ConfigurationError(QueryOptimizerError):
    """Exception raised when configuration is invalid."""
    
    def __init__(self, message: str, config_key: str = None):
        self.config_key = config_key
        details = f"Config key: {config_key}" if config_key else None
        super().__init__(message, details)