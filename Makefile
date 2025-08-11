.PHONY: help install install-dev test test-unit test-integration test-performance lint format clean crawl-docs start-mcp optimize status

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install the package and dependencies
	pip install -e .

install-dev: ## Install development dependencies
	pip install -e ".[dev]"
	pip install -r requirements.txt

test: ## Run all tests
	pytest tests/ -v

test-unit: ## Run unit tests only
	pytest tests/unit/ -v -m unit

test-integration: ## Run integration tests only
	pytest tests/integration/ -v -m integration

test-performance: ## Run performance tests only
	pytest tests/performance/ -v -m performance

test-coverage: ## Run tests with coverage report
	pytest tests/ --cov=src --cov-report=html --cov-report=term-missing

lint: ## Run linting checks
	flake8 src/ tests/
	mypy src/
	black --check src/ tests/
	isort --check-only src/ tests/

format: ## Format code with black and isort
	black src/ tests/
	isort src/ tests/

clean: ## Clean up generated files
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/
	rm -rf __pycache__/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

crawl-docs: ## Crawl BigQuery documentation
	python -m src.crawler.bigquery_docs_crawler

process-docs: ## Process crawled documentation and create embeddings
	python -m src.crawler.documentation_processor

start-mcp: ## Start the MCP server
	python -m src.mcp_server.server

optimize: ## Optimize a sample query (requires QUERY environment variable)
	@if [ -z "$(QUERY)" ]; then \
		echo "Usage: make optimize QUERY='SELECT * FROM table'"; \
	else \
		python -m src.optimizer.main optimize --query "$(QUERY)"; \
	fi

optimize-file: ## Optimize query from file (requires FILE environment variable)
	@if [ -z "$(FILE)" ]; then \
		echo "Usage: make optimize-file FILE=path/to/query.sql"; \
	else \
		python -m src.optimizer.main optimize --file "$(FILE)"; \
	fi

analyze: ## Analyze a query without optimization (requires QUERY environment variable)
	@if [ -z "$(QUERY)" ]; then \
		echo "Usage: make analyze QUERY='SELECT * FROM table'"; \
	else \
		python -m src.optimizer.main analyze --query "$(QUERY)"; \
	fi

status: ## Check system status
	python -m src.optimizer.main status

batch-optimize: ## Run batch optimization on sample queries
	python -m src.optimizer.main batch --queries-file tests/data/sample_queries.json

setup: ## Setup development environment
	python3 -m venv venv || python -m venv venv
	@echo "Activate virtual environment with: source venv/bin/activate (Linux/Mac) or venv\\Scripts\\activate (Windows)"
	@echo "Then run: make install-dev"

check-env: ## Check Python environment health
	@echo "🔍 Checking Python environment..."
	@python3 --version || python --version
	@python3 -c "import sys, os, importlib; print('✅ Basic imports working')" || python -c "import sys, os, importlib; print('✅ Basic imports working')"
	@echo "✅ Environment check complete"

docker-build: ## Build Docker image
	docker build -t bigquery-optimizer .

docker-run: ## Run Docker container
	docker run -it --rm \
		-e GOOGLE_CLOUD_PROJECT=$(GOOGLE_CLOUD_PROJECT) \
		-e GEMINI_API_KEY=$(GEMINI_API_KEY) \
		-v $(PWD)/data:/app/data \
		bigquery-optimizer

# Development shortcuts
dev-setup: setup install-dev crawl-docs process-docs ## Complete development setup

quick-test: test-unit ## Run quick unit tests only

full-test: test-coverage lint ## Run full test suite with coverage and linting

# Demo commands
demo-simple: ## Demo with a simple query
	@echo "Optimizing simple query..."
	python -m src.optimizer.main optimize --query "SELECT * FROM orders WHERE order_date >= '2024-01-01'"

demo-complex: ## Demo with a complex query
	@echo "Optimizing complex query..."
	python -m src.optimizer.main optimize --query "SELECT c.name, COUNT(DISTINCT o.order_id) FROM customers c JOIN orders o ON c.id = o.customer_id WHERE o.date >= '2024-01-01' GROUP BY c.name"

demo-batch: ## Demo batch optimization
	@echo "Running batch optimization demo..."
	python -m src.optimizer.main batch --queries-file tests/data/sample_queries.json --output-dir demo_results