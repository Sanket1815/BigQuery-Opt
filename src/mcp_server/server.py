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
from .optimization_analyzer import OptimizationAnalyzer


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
        self.optimization_analyzer = OptimizationAnalyzer()
        
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
                patterns_count = len(self.optimization_analyzer.optimization_patterns)
                return {
                    "status": "healthy",
                    "timestamp": time.time(),
                    "optimization_patterns": patterns_count,
                    "documentation_source": str(self.optimization_analyzer.docs_file_path)
                }
            except Exception as e:
                raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")
        
        @self.app.post("/analyze")
        async def analyze_sql_query(request: MCPRequest) -> MCPResponse:
            """Analyze SQL query and return optimization suggestions."""
            start_time = time.time()
            
            try:
                sql_query = request.query
                
                # Analyze SQL query directly
                analysis_result = self.optimization_analyzer.analyze_sql_query(sql_query)
                
                processing_time = int((time.time() - start_time) * 1000)
                self.logger.log_mcp_request("analyze", processing_time)
                
                return MCPResponse(
                    success=True,
                    data=analysis_result,
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
        
        @self.app.post("/suggestions")
        async def get_optimization_suggestions(request: MCPRequest) -> MCPResponse:
            """Get optimization suggestions formatted for LLM."""
            start_time = time.time()
            
            try:
                sql_query = request.query
                
                # Get suggestions formatted for LLM
                suggestions_text = self.optimization_analyzer.get_optimization_suggestions_for_llm(sql_query)
                
                processing_time = int((time.time() - start_time) * 1000)
                self.logger.log_mcp_request("suggestions", processing_time)
                
                return MCPResponse(
                    success=True,
                    data={"suggestions_text": suggestions_text},
                    processing_time_ms=processing_time
                )
                
            except Exception as e:
                self.logger.log_error(e, {"endpoint": "/suggestions", "query": request.query})
                return MCPResponse(
                    success=False,
                    error_message=str(e),
                    data={},
                    processing_time_ms=int((time.time() - start_time) * 1000)
                )
        
        @self.app.get("/patterns")
        async def get_all_patterns():
            """Get all available optimization patterns."""
            try:
                patterns = []
                for pattern_id, pattern_data in self.optimization_analyzer.optimization_patterns.items():
                    patterns.append({
                        'pattern_id': pattern_id,
                        'title': pattern_data['title'],
                        'description': pattern_data['description'],
                        'performance_impact': pattern_data['performance_impact'],
                        'use_case': pattern_data['use_case']
                    })
                
                return {
                    "patterns": patterns,
                    "total": len(patterns)
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/optimize")
        async def get_optimization_for_query(request: MCPRequest) -> MCPResponse:
            """Get detailed optimization analysis for a specific SQL query."""
            start_time = time.time()
            
            try:
                sql_query = request.query
                analysis = self.optimization_analyzer.analyze_sql_query(sql_query)
                
                processing_time = int((time.time() - start_time) * 1000)
                self.logger.log_mcp_request("optimize", processing_time)
                
                return MCPResponse(
                    success=True,
                    data=analysis,
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
    
    async def start_server(self):
        """Start the MCP server."""
        self.logger.logger.info(
            f"Starting MCP server on {self.settings.mcp_host}:{self.settings.mcp_port} (separate from FastAPI)"
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