"""Setup configuration for BigQuery Query Optimizer."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = requirements_file.read_text().strip().split('\n')
    requirements = [req.strip() for req in requirements if req.strip() and not req.startswith('#')]

setup(
    name="bigquery-query-optimizer",
    version="1.0.0",
    author="BigQuery Optimizer Team",
    author_email="optimizer@example.com",
    description="AI-powered BigQuery SQL query optimizer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/bigquery-query-optimizer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0",
            "pytest-asyncio>=0.21.1",
            "pytest-mock>=3.12.0",
            "black>=23.12.1",
            "isort>=5.13.2",
            "flake8>=6.1.0",
            "mypy>=1.8.0",
        ],
        "docs": [
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.3.0",
            "myst-parser>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "bq-optimizer=src.optimizer.main:cli",
            "bq-crawler=src.crawler.bigquery_docs_crawler:main",
            "bq-mcp-server=src.mcp_server.server:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.json", "*.yaml", "*.yml"],
    },
    project_urls={
        "Bug Reports": "https://github.com/yourusername/bigquery-query-optimizer/issues",
        "Source": "https://github.com/yourusername/bigquery-query-optimizer",
        "Documentation": "https://bigquery-query-optimizer.readthedocs.io/",
    },
)