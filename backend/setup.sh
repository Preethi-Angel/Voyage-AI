#!/bin/bash

# Setup script for backend development

echo "🧙‍♂️ Setting up AI Travel Planner Backend..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Copy .env.example to .env if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please update .env with your AWS credentials!"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env with your AWS credentials"
echo "2. Activate the virtual environment: source venv/bin/activate"
echo "3. Run the development server: uvicorn app.main:app --reload"
echo ""
echo "🚀 Happy coding!"
