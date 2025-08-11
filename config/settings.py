"""Configuration settings for BigQuery Query Optimizer."""

import os
from pathlib import Path
from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Project settings
    project_name: str = "BigQuery Query Optimizer"
    version: str = "1.0.0"
    debug: bool = Field(default=False, description="Enable debug mode")
    
    # Google Cloud settings
    google_cloud_project: Optional[str] = Field(
        default=None,
        description="Google Cloud Project ID"
    )
    google_application_credentials: Optional[str] = Field(
        default=None,
        description="Path to Google Cloud service account JSON file"
    )
    
    # Gemini AI settings
    gemini_api_key: Optional[str] = Field(
        default=None,
        description="Gemini API key for AI optimization"
    )
    gemini_model_name: str = Field(
        default="models/gemini-pro",
        description="Gemini model to use for optimization"
    )
    
    # MCP Server settings
    mcp_host: str = Field(default="localhost", description="MCP server host")
    mcp_port: int = Field(default=8000, description="MCP server port")
    
    # Documentation crawler settings
    docs_base_url: str = Field(
        default="https://cloud.google.com/bigquery/docs",
        description="Base URL for BigQuery documentation"
    )
    docs_output_dir: Path = Field(
        default=Path("data/documentation"),
        description="Directory to store crawled documentation"
    )
    crawl_delay: float = Field(
        default=1.0,
        description="Delay between requests when crawling (seconds)"
    )
    
    # Vector database settings
    vector_db_path: Path = Field(
        default=Path("data/vector_db"),
        description="Path to vector database storage"
    )
    embedding_model: str = Field(
        default="all-MiniLM-L6-v2",
        description="Sentence transformer model for embeddings"
    )
    
    # Query optimization settings
    max_query_length: int = Field(
        default=100000,
        description="Maximum query length to process"
    )
    optimization_timeout: int = Field(
        default=300,
        description="Timeout for optimization process (seconds)"
    )
    
    # BigQuery settings
    default_location: str = Field(
        default="US",
        description="Default BigQuery location"
    )
    dry_run: bool = Field(
        default=True,
        description="Use dry run for query validation by default"
    )
    
    # Logging settings
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format string"
    )
    
    # Performance testing settings
    performance_test_iterations: int = Field(
        default=3,
        description="Number of iterations for performance testing"
    )
    performance_threshold: float = Field(
        default=0.3,
        description="Minimum performance improvement threshold (30%)"
    )
    
    # Documentation patterns to crawl
    documentation_patterns: List[str] = Field(
        default=[
            "best-practices-performance-overview",
            "best-practices-performance-compute",
            "best-practices-performance-input",
            "best-practices-performance-output",
            "best-practices-costs",
            "optimizing-query-computation",
            "partitioned-tables",
            "clustered-tables",
            "query-plan-explanation",
            "writing-efficient-queries",
        ],
        description="Documentation patterns to crawl"
    )
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        
    def __init__(self, **kwargs):
        """Initialize settings with environment variable validation."""
        super().__init__(**kwargs)
        
        # Create directories if they don't exist
        self.docs_output_dir.mkdir(parents=True, exist_ok=True)
        self.vector_db_path.mkdir(parents=True, exist_ok=True)
        
        # Debug: Print the actual project ID being used
        if self.google_cloud_project:
            print(f"✅ Using Google Cloud Project: {self.google_cloud_project}")
        else:
            print("❌ Google Cloud Project ID not set in environment variables")


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings."""
    return settings

print("✅ Using credentials from:", settings.google_application_credentials)