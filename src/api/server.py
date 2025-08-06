"""FastAPI server for BigQuery Query Optimizer REST API."""

import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn

from config.settings import get_settings
from src.common.logger import QueryOptimizerLogger
from .routes import router


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    settings = get_settings()
    logger = QueryOptimizerLogger(__name__)
    
    app = FastAPI(
        title="BigQuery Query Optimizer API",
        description="REST API for AI-powered BigQuery SQL query optimization",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API routes
    app.include_router(router, prefix="/api/v1")
    
    # Serve static files for the UI
    static_dir = Path(__file__).parent / "static"
    static_dir.mkdir(exist_ok=True)
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
    
    # Root endpoint serves the UI
    @app.get("/", response_class=HTMLResponse)
    async def serve_ui():
        """Serve the main UI page."""
        ui_file = Path(__file__).parent / "templates" / "index.html"
        if ui_file.exists():
            return HTMLResponse(content=ui_file.read_text(), status_code=200)
        else:
            return HTMLResponse(
                content="""
                <html>
                    <head><title>BigQuery Optimizer</title></head>
                    <body>
                        <h1>BigQuery Query Optimizer</h1>
                        <p>UI not found. Please check the templates directory.</p>
                        <p><a href="/docs">View API Documentation</a></p>
                    </body>
                </html>
                """,
                status_code=200
            )
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy", "service": "BigQuery Query Optimizer API"}
    
    logger.logger.info("FastAPI application created successfully")
    return app


def run_server(host: str = "0.0.0.0", port: int = 8080, reload: bool = False):
    """Run the FastAPI server."""
    app = create_app()
    uvicorn.run(app, host=host, port=port, reload=reload)


if __name__ == "__main__":
    run_server(reload=True)