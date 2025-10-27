# How to Start the API Server

## Quick Start

### Method 1: Using the Start Script (Recommended)

From the `backend` directory:

```bash
cd /Users/preethiangels/Documents/Tech_Talk_2025/travel-agent-demo/backend
./start.sh
```

### Method 2: Direct Command

From the `backend` directory:

```bash
cd /Users/preethiangels/Documents/Tech_Talk_2025/travel-agent-demo/backend
/Users/preethiangels/Documents/Tech_Talk_2025/venv/bin/python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Method 3: Activate venv first

```bash
# From project root
cd /Users/preethiangels/Documents/Tech_Talk_2025
source venv/bin/activate

# Then go to backend and start
cd travel-agent-demo/backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Verify Server is Running

Once started, you should see:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Test the API:

```bash
# Health check
curl http://localhost:8000/health

# Expected response:
{
    "status": "healthy",
    "aws_region": "us-east-1",
    "bedrock_model": "anthropic.claude-3-haiku-20240307-v1:0",
    "environment": "development"
}
```

## Common Issues

### Issue: "zsh: command not found: uvicorn"

**Solution:** Don't run `uvicorn` directly. Use one of the methods above that specifies the full path to the venv's Python.

### Issue: "ModuleNotFoundError: No module named 'app'"

**Solution:** Make sure you're in the `backend` directory when starting the server.

```bash
cd /Users/preethiangels/Documents/Tech_Talk_2025/travel-agent-demo/backend
./start.sh
```

### Issue: "FileNotFoundError: .env file not found"

**Solution:** Create a `.env` file from the example:

```bash
cd /Users/preethiangels/Documents/Tech_Talk_2025/travel-agent-demo/backend
cp .env.example .env
# Then edit .env with your AWS credentials
```

## API Endpoints

Once running, access:

- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### Available Endpoints:

1. **POST /api/single** - Single agent (demonstrates failures)
2. **POST /api/multi** - Multi-agent with AWS SDK (real A2A communication) ⭐

## Testing the API

### Single Agent Endpoint:

```bash
curl -X POST http://localhost:8000/api/single \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Tokyo, Japan",
    "duration_days": 5,
    "budget": 3000,
    "travelers": 2,
    "interests": ["food", "tech"],
    "enable_logging": true
  }'
```

### Multi-Agent Endpoint (Real AWS SDK):

```bash
curl -X POST http://localhost:8000/api/multi \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Tokyo, Japan",
    "duration_days": 5,
    "budget": 3000,
    "travelers": 2,
    "interests": ["food", "tech", "temples"],
    "hotel_preference": "mid-range",
    "enable_logging": true
  }'
```

## Stop the Server

Press `Ctrl+C` in the terminal where the server is running.

Or from another terminal:

```bash
pkill -f uvicorn
```

## Directory Structure

```
Tech_Talk_2025/
├── venv/                    # Virtual environment (shared)
└── travel-agent-demo/
    └── backend/
        ├── start.sh         # ✅ Start script
        ├── .env             # AWS credentials
        ├── requirements.txt
        └── app/
            ├── main.py      # FastAPI app
            ├── agents/
            ├── routers/
            └── services/
```

## Important Notes

- The virtual environment is at **project root level** (`Tech_Talk_2025/venv/`)
- Always start the server from the `backend` directory
- The server runs on port 8000 by default
- API docs are auto-generated at `/docs`

## For Your Tech Talk

Quick commands to demonstrate:

```bash
# Start server
cd backend && ./start.sh

# In another terminal - test single agent
curl -s http://localhost:8000/api/single -X POST -H "Content-Type: application/json" \
  -d '{"destination": "Tokyo, Japan", "duration_days": 5, "budget": 3000, "travelers": 2, "interests": ["food"], "enable_logging": true}' \
  | jq '.status'

# Test multi-agent with real AWS SDK
curl -s http://localhost:8000/api/multi -X POST -H "Content-Type: application/json" \
  -d '{"destination": "Tokyo, Japan", "duration_days": 5, "budget": 3000, "travelers": 2, "interests": ["food", "tech", "temples"], "hotel_preference": "mid-range", "enable_logging": true}' \
  | jq '.agent_logs'
```
