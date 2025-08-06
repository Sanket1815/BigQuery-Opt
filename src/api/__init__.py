"""REST API for BigQuery Query Optimizer."""

from .server import create_app
from .routes import router

__all__ = ["create_app", "router"]