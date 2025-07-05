#!/usr/bin/env python3
"""
Test script to verify the demo setup
"""

import os
import sys
from pathlib import Path

def test_imports():
    """Test if all required packages can be imported"""
    print("Testing imports...")
    
    try:
        import flask
        print("✅ Flask")
    except ImportError:
        print("❌ Flask - run: pip install flask")
        return False
    
    try:
        import spotipy
        print("✅ Spotipy")
    except ImportError:
        print("❌ Spotipy - run: pip install spotipy")
        return False
    
    try:
        import openai
        print("✅ OpenAI")
    except ImportError:
        print("❌ OpenAI - run: pip install openai")
        return False
    
    try:
        import pandas
        print("✅ Pandas")
    except ImportError:
        print("❌ Pandas - run: pip install pandas")
        return False
    
    try:
        import numpy
        print("✅ Numpy")
    except ImportError:
        print("❌ Numpy - run: pip install numpy")
        return False
    
    return True

def test_config():
    """Test if configuration can be loaded"""
    print("\nTesting configuration...")
    
    try:
        from config import Config
        print("✅ Config loaded")
        
        # Check if API keys are set
        if Config.SPOTIFY_CLIENT_ID != 'your_spotify_client_id':
            print("✅ Spotify client ID configured")
        else:
            print("⚠️  Spotify client ID not configured")
        
        if Config.OPENAI_API_KEY != 'your_openai_api_key':
            print("✅ OpenAI API key configured")
        else:
            print("⚠️  OpenAI API key not configured")
        
        return True
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False

def test_components():
    """Test if main components can be initialized"""
    print("\nTesting components...")
    
    try:
        from spotify_client import SpotifyClient
        client = SpotifyClient()
        print("✅ SpotifyClient initialized")
    except Exception as e:
        print(f"❌ SpotifyClient error: {e}")
        return False
    
    try:
        from mood_analyzer import MoodAnalyzer
        analyzer = MoodAnalyzer()
        print("✅ MoodAnalyzer initialized")
    except Exception as e:
        print(f"❌ MoodAnalyzer error: {e}")
        return False
    
    return True

def test_flask_app():
    """Test if Flask app can be created"""
    print("\nTesting Flask app...")
    
    try:
        from app import app
        print("✅ Flask app created")
        
        # Test if templates directory exists
        templates_dir = Path('templates')
        if templates_dir.exists():
            print("✅ Templates directory found")
        else:
            print("❌ Templates directory missing")
            return False
        
        # Test if index.html exists
        index_file = templates_dir / 'index.html'
        if index_file.exists():
            print("✅ index.html template found")
        else:
            print("❌ index.html template missing")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Flask app error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Spotify Mood Analyzer Demo Setup")
    print("=" * 50)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test configuration
    if not test_config():
        all_passed = False
    
    # Test components
    if not test_components():
        all_passed = False
    
    # Test Flask app
    if not test_flask_app():
        all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ All tests passed! Demo is ready to run.")
        print("\nTo start the demo, run:")
        print("python app.py")
        print("\nThen open: http://localhost:5000")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 