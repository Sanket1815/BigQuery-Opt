"""Logging utilities for BigQuery Query Optimizer."""

import logging
import sys
from typing import Optional
import structlog
from config.settings import get_settings


def configure_logging(
    level: Optional[str] = None,
    format_string: Optional[str] = None
) -> None:
    """Configure structured logging for the application."""
    settings = get_settings()
    
    # Use provided level or fall back to settings
    log_level = level or settings.log_level
    log_format = format_string or settings.log_format
    
    # Configure standard logging
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        stream=sys.stdout
    )
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.BoundLogger:
    """Get a structured logger instance."""
    # Ensure logging is configured
    if not structlog.is_configured():
        configure_logging()
    
    return structlog.get_logger(name)


class QueryOptimizerLogger:
    """Specialized logger for query optimization operations."""
    
    def __init__(self, name: str):
        self.logger = get_logger(name)
    
    def log_query_analysis(self, query: str, analysis_result: dict):
        """Log query analysis results."""
        self.logger.info(
            "Query analyzed",
            query_hash=hash(query),
            query_length=len(query),
            complexity=analysis_result.get("complexity"),
            table_count=analysis_result.get("table_count"),
            join_count=analysis_result.get("join_count"),
            issues_found=len(analysis_result.get("potential_issues", []))
        )
    
    def log_optimization_applied(
        self, 
        pattern_id: str, 
        pattern_name: str, 
        expected_improvement: Optional[float] = None
    ):
        """Log when an optimization is applied."""
        self.logger.info(
            "Optimization applied",
            pattern_id=pattern_id,
            pattern_name=pattern_name,
            expected_improvement=expected_improvement
        )
    
    def log_performance_comparison(
        self, 
        original_time_ms: Optional[int],
        optimized_time_ms: Optional[int],
        improvement: Optional[float]
    ):
        """Log performance comparison results."""
        self.logger.info(
            "Performance comparison",
            original_time_ms=original_time_ms,
            optimized_time_ms=optimized_time_ms,
            improvement_percentage=improvement
        )
    
    def log_validation_result(self, results_identical: bool, error: Optional[str] = None):
        """Log query validation results."""
        if results_identical:
            self.logger.info("Query validation passed", results_identical=True)
        else:
            self.logger.error(
                "Query validation failed", 
                results_identical=False,
                error=error
            )
    
    def log_error(self, error: Exception, context: Optional[dict] = None):
        """Log errors with context."""
        log_data = {
            "error_type": type(error).__name__,
            "error_message": str(error)
        }
        if context:
            log_data.update(context)
        
        self.logger.error("Operation failed", **log_data)
    
    def log_crawler_progress(self, url: str, status: str, pages_crawled: int):
        """Log documentation crawler progress."""
        self.logger.info(
            "Crawler progress",
            url=url,
            status=status,
            pages_crawled=pages_crawled
        )
    
    def log_mcp_request(self, request_type: str, processing_time_ms: int):
        """Log MCP server requests."""
        self.logger.info(
            "MCP request processed",
            request_type=request_type,
            processing_time_ms=processing_time_ms
        )