#!/bin/bash

# Comprehensive setup and test script for AI Travel Planner

set -e  # Exit on error

echo "🧙‍♂️ AI Travel Planner - Setup and Test Script"
echo "=============================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.11+${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python 3 found: $(python3 --version)${NC}"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${GREEN}✅ Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

echo -e "${GREEN}✅ Dependencies installed${NC}"
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Please update .env with your AWS credentials!${NC}"
    echo ""
    echo "Required environment variables:"
    echo "  - AWS_REGION (default: us-east-1)"
    echo "  - AWS_ACCESS_KEY_ID"
    echo "  - AWS_SECRET_ACCESS_KEY"
    echo ""
    read -p "Do you want to enter AWS credentials now? (y/n) " -n 1 -r
    echo ""

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter AWS Region (default: us-east-1): " aws_region
        aws_region=${aws_region:-us-east-1}

        read -p "Enter AWS Access Key ID: " aws_key
        read -sp "Enter AWS Secret Access Key: " aws_secret
        echo ""

        # Update .env file
        sed -i.bak "s|AWS_REGION=.*|AWS_REGION=$aws_region|" .env
        sed -i.bak "s|AWS_ACCESS_KEY_ID=.*|AWS_ACCESS_KEY_ID=$aws_key|" .env
        sed -i.bak "s|AWS_SECRET_ACCESS_KEY=.*|AWS_SECRET_ACCESS_KEY=$aws_secret|" .env
        rm .env.bak

        echo -e "${GREEN}✅ AWS credentials saved to .env${NC}"
    else
        echo -e "${YELLOW}⚠️  Please manually edit .env file before testing${NC}"
        exit 0
    fi
else
    echo -e "${GREEN}✅ .env file already exists${NC}"
fi

echo ""
echo "🧪 Testing AWS Bedrock connectivity..."
python3 - << 'EOF'
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Check required env vars
required_vars = ['AWS_REGION', 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY']
missing_vars = [var for var in required_vars if not os.getenv(var) or os.getenv(var).startswith('your_')]

if missing_vars:
    print(f"❌ Missing or invalid AWS credentials: {', '.join(missing_vars)}")
    print("\nPlease update .env file with valid AWS credentials")
    sys.exit(1)

try:
    import boto3
    from botocore.exceptions import ClientError

    # Test Bedrock access
    bedrock = boto3.client('bedrock', region_name=os.getenv('AWS_REGION'))
    response = bedrock.list_foundation_models()

    print("✅ AWS Bedrock connection successful!")
    print(f"   Region: {os.getenv('AWS_REGION')}")
    print(f"   Available models: {len(response.get('modelSummaries', []))}")

except ClientError as e:
    print(f"❌ AWS Bedrock connection failed: {e}")
    print("\nPossible issues:")
    print("  1. Invalid AWS credentials")
    print("  2. Bedrock not enabled in your region")
    print("  3. Insufficient IAM permissions")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)
EOF

if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}❌ AWS setup failed. Please fix the issues above.${NC}"
    exit 1
fi

echo ""
echo "=============================================="
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo "=============================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Start the development server:"
echo "   uvicorn app.main:app --reload"
echo ""
echo "2. Open API documentation:"
echo "   http://localhost:8000/docs"
echo ""
echo "3. Or run quick tests:"
echo "   python test_stage1.py"
echo "   python test_stage2.py"
echo ""
echo "🚀 Happy coding!"
