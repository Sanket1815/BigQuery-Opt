#!/usr/bin/env python3
"""
Environment Setup Script for BigQuery Query Optimizer
This script helps you set up the required environment variables.
"""

import os
import sys
from pathlib import Path

def create_env_file():
    """Create a .env file from the template."""
    template_file = Path("env_template.txt")
    env_file = Path(".env")
    
    if env_file.exists():
        print("⚠️  .env file already exists!")
        response = input("Do you want to overwrite it? (y/N): ").strip().lower()
        if response != 'y':
            print("Keeping existing .env file")
            return False
    
    if not template_file.exists():
        print("❌ env_template.txt not found!")
        return False
    
    try:
        # Read template
        with open(template_file, 'r') as f:
            template_content = f.read()
        
        # Create .env file
        with open(env_file, 'w') as f:
            f.write(template_content)
        
        print("✅ .env file created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def check_gemini_api_key():
    """Check if GEMINI_API_KEY is properly set."""
    gemini_key = os.getenv('GEMINI_API_KEY')
    
    if not gemini_key:
        print("❌ GEMINI_API_KEY not set")
        return False
    
    if gemini_key == 'your_actual_gemini_api_key_here':
        print("❌ GEMINI_API_KEY still has placeholder value")
        return False
    
    if len(gemini_key) < 10:
        print("❌ GEMINI_API_KEY appears to be invalid (too short)")
        return False
    
    print("✅ GEMINI_API_KEY is properly set")
    return True

def get_gemini_api_key():
    """Get Gemini API key from user input."""
    print("\n🔑 Gemini API Key Setup")
    print("=" * 40)
    print("To get your Gemini API key:")
    print("1. Go to https://aistudio.google.com/app/apikey")
    print("2. Sign in with your Google account")
    print("3. Click 'Create API Key'")
    print("4. Copy the generated API key")
    print()
    
    api_key = input("Enter your Gemini API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided")
        return None
    
    if len(api_key) < 10:
        print("❌ API key appears to be too short")
        return None
    
    return api_key

def update_env_file(api_key):
    """Update the .env file with the actual API key."""
    env_file = Path(".env")
    
    if not env_file.exists():
        print("❌ .env file not found. Please run setup first.")
        return False
    
    try:
        # Read current content
        with open(env_file, 'r') as f:
            content = f.read()
        
        # Replace placeholder
        updated_content = content.replace(
            'GEMINI_API_KEY=your_actual_gemini_api_key_here',
            f'GEMINI_API_KEY={api_key}'
        )
        
        # Write updated content
        with open(env_file, 'w') as f:
            f.write(updated_content)
        
        print("✅ .env file updated with your API key!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to update .env file: {e}")
        return False

def test_environment():
    """Test if the environment is properly set up."""
    print("\n🧪 Testing Environment Setup")
    print("=" * 40)
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found")
        return False
    
    # Check if GEMINI_API_KEY is set
    if not check_gemini_api_key():
        return False
    
    # Test if the environment variable is loaded
    print("\n🔄 Testing environment variable loading...")
    
    # Try to import and test the handler
    try:
        from src.mcp_server.handlers import DirectSQLOptimizationHandler
        
        handler = DirectSQLOptimizationHandler()
        model = handler._initialize_gemini()
        
        if model:
            print("✅ Gemini API initialized successfully!")
            return True
        else:
            print("❌ Gemini API initialization failed")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 BigQuery Query Optimizer Environment Setup")
    print("=" * 50)
    
    # Step 1: Create .env file
    print("\n📝 Step 1: Creating .env file...")
    if not create_env_file():
        print("❌ Failed to create .env file")
        return False
    
    # Step 2: Get API key from user
    print("\n🔑 Step 2: Setting up Gemini API key...")
    api_key = get_gemini_api_key()
    if not api_key:
        print("❌ No valid API key provided")
        return False
    
    # Step 3: Update .env file
    print("\n📝 Step 3: Updating .env file...")
    if not update_env_file(api_key):
        print("❌ Failed to update .env file")
        return False
    
    # Step 4: Test environment
    print("\n🧪 Step 4: Testing environment...")
    if not test_environment():
        print("❌ Environment test failed")
        return False
    
    print("\n🎉 Environment setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Restart your application")
    print("2. Run test suites to verify optimization is working")
    print("3. Check that 'AI-Generated Optimization' appears in the UI")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        sys.exit(1) 