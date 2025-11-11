#!/bin/bash
set -e

echo "🚀 Bootstrapping NDT Bot development environment..."

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate || source venv/Scripts/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements-dev.txt

# Create .env from example if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please update .env with your API keys"
fi

# Create necessary directories
echo "Creating directory structure..."
mkdir -p storage/vector_store
mkdir -p data/docs
mkdir -p data/cache
mkdir -p data/LICENSES

# Install pre-commit hooks
echo "Installing pre-commit hooks..."
pre-commit install

echo "✅ Bootstrap complete! Run 'source venv/bin/activate' to activate the environment."
