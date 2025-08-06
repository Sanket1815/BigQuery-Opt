"""Documentation crawler for BigQuery optimization best practices."""

from .bigquery_docs_crawler import BigQueryDocsCrawler

try:
    from .documentation_processor import DocumentationProcessor
    __all__ = ["BigQueryDocsCrawler", "DocumentationProcessor"]
except ImportError:
    # If documentation_processor is not available, only export the crawler
    __all__ = ["BigQueryDocsCrawler"]