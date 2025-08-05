"""Main MCP server implementation for BigQuery optimization."""

import asyncio
import json
import time
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from config.settings import get_settings
from src.common.exceptions import MCPServerError
from src.common.logger import QueryOptimizerLogger
from src.common.models import MCPRequest, MCPResponse
from src.crawler.documentation_processor import DocumentationProcessor
from .handlers import DocumentationHandler, OptimizationHandler


class BigQueryMCPServer:
    """MCP Server for BigQuery optimization documentation and suggestions."""
    
    def __init__(self):
        self.settings = get_settings()
        self.logger = QueryOptimizerLogger(__name__)
        self.app = FastAPI(
            title="BigQuery Optimization MCP Server",
            description="Model Context Protocol server for BigQuery query optimization",
            version="1.0.0"
        )
        
        # Initialize components
        self.documentation_processor = DocumentationProcessor()
        self.documentation_handler = DocumentationHandler(self.documentation_processor)
        self.optimization_handler = OptimizationHandler(self.documentation_processor)
        
        # Setup middleware
        self._setup_middleware()
        
        # Setup routes
        self._setup_routes()
    
    def _setup_middleware(self):
        """Setup FastAPI middleware."""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    def _setup_routes(self):
        """Setup API routes."""
        
        @self.app.get("/")
        async def root():
            """Root endpoint with server information."""
            return {
                "name": "BigQuery Optimization MCP Server",
                "version": "1.0.0",
                "status": "running",
                "endpoints": [
                    "/search",
                    "/patterns",
                    "/analyze",
                    "/optimize",
                    "/health"
                ]
            }
        
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint."""
            try:
                summary = self.documentation_processor.get_documentation_summary()
                return {
                    "status": "healthy",
                    "timestamp": time.time(),
                    "documentation": summary
                }
            except Exception as e:
                raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")
        
        @self.app.post("/search")
        async def search_documentation(request: MCPRequest) -> MCPResponse:
            """Search documentation for relevant information."""
            start_time = time.time()
            
            try:
                query = request.query
                n_results = request.options.get("n_results", 5)
                filter_patterns = request.options.get("filter_patterns")
                
                results = await self.documentation_handler.search_documentation(
                    query, n_results, filter_patterns
                )
                
                processing_time = int((time.time() - start_time) * 1000)
                self.logger.log_mcp_request("search", processing_time)
                
                return MCPResponse(
                    success=True,
                    data={"results": results},
                    processing_time_ms=processing_time
                )
                
            except Exception as e:
                self.logger.log_error(e, {"endpoint": "/search", "query": request.query})
                return MCPResponse(
                    success=False,
                    error_message=str(e),
                    data={},
                    processing_time_ms=int((time.time() - start_time) * 1000)
                )
        
        @self.app.post("/patterns")
        async def get_optimization_patterns(request: MCPRequest) -> MCPResponse:
            """Get optimization patterns for a SQL query."""
            start_time = time.time()
            
            try:
                query = request.query
                patterns = await self.optimization_handler.get_patterns_for_query(query)
                
                processing_time = int((time.time() - start_time) * 1000)
                self.logger.log_mcp_request("patterns", processing_time)
                
                return MCPResponse(
                    success=True,
                    data={"patterns": [pattern.model_dump() for pattern in patterns]},
                    processing_time_ms=processing_time
                )
                
            except Exception as e:
                self.logger.log_error(e, {"endpoint": "/patterns", "query": request.query})
                return MCPResponse(
                    success=False,
                    error_message=str(e),
                    data={},
                    processing_time_ms=int((time.time() - start_time) * 1000)
                )
        
        @self.app.post("/analyze")
        async def analyze_query(request: MCPRequest) -> MCPResponse:
            """Analyze a SQL query for optimization opportunities."""
            start_time = time.time()
            
            try:
                query = request.query
                analysis = await self.optimization_handler.analyze_query(query)
                
                processing_time = int((time.time() - start_time) * 1000)
                self.logger.log_mcp_request("analyze", processing_time)
                
                return MCPResponse(
                    success=True,
                    data={"analysis": analysis.model_dump()},
                    processing_time_ms=processing_time
                )
                
            except Exception as e:
                self.logger.log_error(e, {"endpoint": "/analyze", "query": request.query})
                return MCPResponse(
                    success=False,
                    error_message=str(e),
                    data={},
                    processing_time_ms=int((time.time() - start_time) * 1000)
                )
        
        @self.app.post("/optimize")
        async def optimize_query(request: MCPRequest) -> MCPResponse:
            """Get optimization suggestions for a SQL query."""
            start_time = time.time()
            
            try:
                query = request.query
                suggestions = await self.optimization_handler.get_optimization_suggestions(query)
                
                processing_time = int((time.time() - start_time) * 1000)
                self.logger.log_mcp_request("optimize", processing_time)
                
                return MCPResponse(
                    success=True,
                    data={"suggestions": suggestions},
                    processing_time_ms=processing_time
                )
                
            except Exception as e:
                self.logger.log_error(e, {"endpoint": "/optimize", "query": request.query})
                return MCPResponse(
                    success=False,
                    error_message=str(e),
                    data={},
                    processing_time_ms=int((time.time() - start_time) * 1000)
                )
        
        @self.app.get("/patterns/all")
        async def get_all_patterns():
            """Get all available optimization patterns."""
            try:
                patterns = self.documentation_processor.optimization_patterns
                return {
                    "patterns": [pattern.model_dump() for pattern in patterns],
                    "total": len(patterns)
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
    
    async def start_server(self):
        """Start the MCP server."""
        self.logger.logger.info(
            f"Starting MCP server on {self.settings.mcp_host}:{self.settings.mcp_port}"
        )
        
        config = uvicorn.Config(
            self.app,
            host=self.settings.mcp_host,
            port=self.settings.mcp_port,
            log_level=self.settings.log_level.lower()
        )
        
        server = uvicorn.Server(config)
        await server.serve()
    
    def run(self):
        """Run the server synchronously."""
        try:
            asyncio.run(self.start_server())
        except KeyboardInterrupt:
            self.logger.logger.info("Server stopped by user")
        except Exception as e:
            self.logger.log_error(e, {"operation": "run_server"})
            raise MCPServerError(f"Failed to start server: {str(e)}")


def main():
    """Main function to start the MCP server."""
    server = BigQueryMCPServer()
    server.run()


if __name__ == "__main__":
    main()