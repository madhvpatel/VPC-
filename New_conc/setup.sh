#!/bin/bash

# Setup script for AI Financial Relationship Manager
# This script handles dependency installation and server startup

echo "🚀 Setting up AI Financial Relationship Manager..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies one by one with fallbacks for problematic packages
echo "📥 Installing dependencies..."

# Core dependencies first
pip install fastapi uvicorn python-dotenv httpx

# Try newer compatible versions that have prebuilt wheels
echo "Installing LangChain and AI providers..."
pip install langchain langchain-google-genai langchain-openai

# Data science libraries
echo "Installing data science libraries..."
pip install pandas numpy yfinance

# Try pydantic with newer version that has ARM wheels
echo "Installing pydantic..."
pip install "pydantic>=2.0,<3.0" "pydantic-core>=2.0,<3.0"

echo "✅ Installation complete!"
echo ""
echo "📝 Next steps:"
echo "1. Copy .env.example to .env"
echo "2. Add your API key (Google Gemini, OpenAI, or Anthropic)"  
echo "3. Run: source venv/bin/activate && python main.py"
echo ""
echo "🌐 The app will be available at http://localhost:8000"
