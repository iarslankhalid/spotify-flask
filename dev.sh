#!/bin/bash

# Quick development commands for Spotify Mood Analyzer

case "$1" in
    "run")
        echo "🚀 Starting Spotify Mood Analyzer..."
        python3 app.py
        ;;
    "test")
        echo "🧪 Running tests..."
        python3 -m pytest tests/ -v
        ;;
    "install")
        echo "📦 Installing dependencies..."
        pip3 install -r requirements.txt
        ;;
    "clean")
        echo "🧹 Cleaning cache files..."
        find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
        find . -name "*.pyc" -delete 2>/dev/null || true
        echo "✅ Cache cleaned"
        ;;
    "ssl")
        echo "🔒 Generating SSL certificates..."
        python3 ssl_certs/generate_ssl.py
        ;;
    "check")
        echo "🔍 Checking API connections..."
        python3 utils/check_gemini_models.py
        ;;
    *)
        echo "🎵 Spotify Mood Analyzer - Development Helper"
        echo "Usage: ./dev.sh [command]"
        echo ""
        echo "Commands:"
        echo "  run     - Start the Flask application"
        echo "  test    - Run all tests"
        echo "  install - Install Python dependencies"
        echo "  clean   - Clean Python cache files"
        echo "  ssl     - Generate SSL certificates"
        echo "  check   - Check API connections"
        echo ""
        echo "Examples:"
        echo "  ./dev.sh run"
        echo "  ./dev.sh test"
        ;;
esac
