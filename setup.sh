#!/bin/bash

# Setup script for Spotify Mood Analyzer
# This script helps set up the development environment

echo "🎵 Spotify Mood Analyzer - Setup Script"
echo "========================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

echo "✅ pip3 found: $(pip3 --version)"

# Install requirements
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from example..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your actual API keys before running the app"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "🚀 Setup complete! Next steps:"
echo "1. Edit .env file with your API keys:"
echo "   - Get Spotify keys from: https://developer.spotify.com/dashboard"
echo "   - Get OpenAI key from: https://platform.openai.com/api-keys"
echo "   - Get Gemini key from: https://makersuite.google.com/app/apikey"
echo ""
echo "2. Run the application:"
echo "   python3 app.py"
echo ""
echo "3. Open http://localhost:5000 in your browser"
echo ""
echo "Happy analyzing! 🎶"
