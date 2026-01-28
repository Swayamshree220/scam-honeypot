#!/bin/bash

echo "🍯 Setting up Scam Honeypot..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

echo "✅ Setup complete!"
echo "📝 Please edit .env and add your API keys"
echo "🚀 Run: python app.py"