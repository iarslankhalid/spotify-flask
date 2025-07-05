#!/usr/bin/env python3
"""
Quick demo runner for Spotify Mood Analyzer
"""

import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Check if requirements are installed"""
    try:
        import flask
        import spotipy
        import openai
        import pandas
        import numpy
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("\nPlease install requirements first:")
        print("pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists and has the required variables"""
    env_path = Path('.env')
    
    if not env_path.exists():
        print("❌ .env file not found")
        print("\nPlease create a .env file with your API keys:")
        print("SPOTIFY_CLIENT_ID=your_spotify_client_id")
        print("SPOTIFY_CLIENT_SECRET=your_spotify_client_secret")
        print("OPENAI_API_KEY=your_openai_api_key")
        print("FLASK_ENV=development")
        print("FLASK_SECRET_KEY=your_random_secret_key")
        return False
    
    # Check if file has content
    with open(env_path, 'r') as f:
        content = f.read()
        if 'your_spotify_client_id' in content or 'your_openai_api_key' in content:
            print("⚠️  .env file exists but contains placeholder values")
            print("Please update .env file with your actual API keys")
            return False
    
    print("✅ .env file is configured")
    return True

def main():
    """Main demo runner"""
    print("🎵 Spotify Mood Analyzer Demo")
    print("=" * 40)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check environment file
    env_configured = check_env_file()
    
    if not env_configured:
        print("\n⚠️  Environment not fully configured")
        print("The demo will start but API features won't work without proper API keys")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    print("\n🚀 Starting demo server...")
    print("📱 Demo will be available at: http://localhost:5000")
    print("🔧 Press Ctrl+C to stop the server")
    print("-" * 40)
    
    try:
        # Start the Flask app
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\n✅ Demo server stopped")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 