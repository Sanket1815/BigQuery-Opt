"""FastAPI server for BigQuery Query Optimizer REST API."""

import os
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
    
    # Mount static files
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    if not os.path.exists(static_dir):
        try:
            os.makedirs(static_dir, exist_ok=True)
        except (OSError, AttributeError):
            # Handle environments without full os support
            pass
    
    try:
        app.mount("/static", StaticFiles(directory=static_dir), name="static")
    except Exception:
        # Skip static files if not available
        pass
    
    # Root endpoint serves the UI
    @app.get("/")
    async def serve_ui():
        """Serve the main UI page."""
        template_dir = os.path.join(os.path.dirname(__file__), "templates")
        template_path = os.path.join(template_dir, "index.html")
        
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return HTMLResponse(content=content, status_code=200)
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