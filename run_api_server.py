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
        print(f"✅ Python version: {sys.version}")
        
        # Check if sys.executable is available
        if not sys.executable:
            print("❌ Python executable path is empty - corrupted environment")
            return False
        
        print(f"✅ Python executable: {sys.executable}")
        
        # Test critical imports
        try:
            import importlib
            import json
            print("✅ Basic imports working")
        except ImportError as e:
            print(f"❌ Basic imports failed: {e}")
            return False
            
        return True
    except Exception as e:
        print(f"❌ Python environment check failed: {e}")
        return False

def check_os_module():
    """Check if os module has required attributes."""
    try:
        import os
        if not hasattr(os, 'chmod'):
            print("❌ os module missing chmod attribute - corrupted installation")
            return False
        print("✅ os module working correctly")
        return True
    except Exception as e:
        print(f"❌ os module check failed: {e}")
        return False

def main():
    print("🔍 Checking Python environment...")
    
    if not check_python_environment():
        print("\n❌ Python environment is corrupted or incomplete.")
        print("🔧 Please try the following steps:")
        print("   1. Create a new virtual environment: python -m venv venv")
        print("   2. Activate it:")
        print("      - Linux/Mac: source venv/bin/activate")
        print("      - Windows: venv\\Scripts\\activate")
        print("   3. Reinstall dependencies: pip install -r requirements.txt")
        print("   4. Try running the server again")
        sys.exit(1)
    
    if not check_os_module():
        print("\n❌ Operating system module is corrupted.")
        print("🔧 This indicates a severely corrupted Python installation.")
        print("   Please create a new virtual environment as described above.")
        sys.exit(1)
    
    # Only import these after basic checks pass
    try:
        import argparse
        from pathlib import Path
    except ImportError as e:
        print(f"❌ Failed to import required modules: {e}")
        print("🔧 Try creating a new virtual environment:")
        print("   python -m venv venv && source venv/bin/activate && pip install -r requirements.txt")
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