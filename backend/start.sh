#!/bin/bash

# Startup script for AI Travel Planner API
# Run this from the backend directory: ./start.sh

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting AI Travel Planner API...${NC}"

# Get the project root directory (parent of backend)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/../.." && pwd )"
VENV_PATH="$PROJECT_ROOT/venv"

# Check if venv exists
if [ ! -d "$VENV_PATH" ]; then
    echo "Error: Virtual environment not found at $VENV_PATH"
    exit 1
fi

# Check if .env exists
if [ ! -f "$SCRIPT_DIR/.env" ]; then
    echo "Error: .env file not found. Please create one from .env.example"
    exit 1
fi

echo -e "${GREEN}✓${NC} Found virtual environment at: $VENV_PATH"
echo -e "${GREEN}✓${NC} Found .env file"

# Start the server using the venv's python
cd "$SCRIPT_DIR"
echo -e "${BLUE}Starting uvicorn server...${NC}"
echo ""

"$VENV_PATH/bin/python3" -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
