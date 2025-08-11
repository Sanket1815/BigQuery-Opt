#!/usr/bin/env python3
"""
Script to run the BigQuery Query Optimizer REST API server.
"""

import sys
import os

def check_python_environment():
    """Check if Python environment is working correctly."""
    try:
        # Test basic Python functionality
        import importlib
        import json
        print(f"✅ Python version: {sys.version}")
        print(f"✅ Python executable: {sys.executable}")
        return True
    except Exception as e:
        print(f"❌ Python environment check failed: {e}")
        return False

def main():
    print("🔍 Checking Python environment...")
    
    if not check_python_environment():
        print("\n❌ Python environment is corrupted or incomplete.")
        print("🔧 Please try the following steps:")
        print("   1. Reinstall Python from python.org")
        print("   2. Create a new virtual environment: python -m venv venv")
        print("   3. Activate it: source venv/bin/activate (Linux/Mac) or venv\\Scripts\\activate (Windows)")
        print("   4. Reinstall dependencies: pip install -r requirements.txt")
        sys.exit(1)
    
    try:
        import argparse
        from pathlib import Path
    except ImportError as e:
        print(f"❌ Failed to import required modules: {e}")
        print("🔧 Try reinstalling Python or creating a new virtual environment")
        sys.exit(1)
    
    # Add src to path
    project_root = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(project_root, "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    
    try:
        from src.api.server import run_server
    except ImportError as e:
        print(f"❌ Failed to import API server: {e}")
        print("🔧 Make sure you've installed the project dependencies:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    parser = argparse.ArgumentParser(description="Run BigQuery Query Optimizer API Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8080, help="Port to bind to (default: 8080)")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload for development")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()
    
    print(f"🚀 Starting BigQuery Query Optimizer API Server")
    print(f"📍 Server will be available at: http://{args.host}:{args.port}")
    print(f"📚 API Documentation: http://{args.host}:{args.port}/docs")
    print(f"🎨 Web UI: http://{args.host}:{args.port}/")
    print()
    
    if args.debug:
        os.environ["DEBUG"] = "1"
    
    try:
        run_server(host=args.host, port=args.port, reload=args.reload)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Server failed to start: {e}")
        print("🔧 Check that all dependencies are installed and ports are available")
        sys.exit(1)


if __name__ == "__main__":
    main()