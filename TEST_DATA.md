# Test Data for AI Travel Planner API

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Quick Health Check

```bash
curl http://localhost:8000/health
```

---

## Test Case 1: Basic Tokyo Trip (Budget-Friendly)

**Endpoint**: `POST /api/multi`

```bash
curl -X POST http://localhost:8000/api/multi \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Tokyo, Japan",
    "duration_days": 5,
    "budget": 2000,
    "travelers": 1,
    "interests": ["food", "temples"],
    "hotel_preference": "budget",
    "activity_level": "moderate",
    "enable_logging": true
  }'
```

**JSON format**:
```json
{
  "destination": "Tokyo, Japan",
  "duration_days": 5,
  "budget": 2000,
  "travelers": 1,
  "interests": ["food", "temples"],
  "hotel_preference": "budget",
  "activity_level": "moderate",
  "enable_logging": true
}
```

---

## Test Case 2: Couple's Luxury Trip

**Endpoint**: `POST /api/multi`

```bash
curl -X POST http://localhost:8000/api/multi \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Tokyo, Japan",
    "duration_days": 7,
    "budget": 5000,
    "travelers": 2,
    "interests": ["food", "tech", "temples", "shopping"],
    "hotel_preference": "luxury",
    "activity_level": "high",
    "enable_logging": true
  }'
```

**JSON format**:
```json
{
  "destination": "Tokyo, Japan",
  "duration_days": 7,
  "budget": 5000,
  "travelers": 2,
  "interests": ["food", "tech", "temples", "shopping"],
  "hotel_preference": "luxury",
  "activity_level": "high",
  "enable_logging": true
}
```

---

## Test Case 3: Family Trip (Mid-Range)

**Endpoint**: `POST /api/multi`

```bash
curl -X POST http://localhost:8000/api/multi \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Tokyo, Japan",
    "duration_days": 5,
    "budget": 4000,
    "travelers": 4,
    "interests": ["food", "tech", "culture"],
    "hotel_preference": "mid-range",
    "activity_level": "moderate",
    "enable_logging": true
  }'
```

**JSON format**:
```json
{
  "destination": "Tokyo, Japan",
  "duration_days": 5,
  "budget": 4000,
  "travelers": 4,
  "interests": ["food", "tech", "culture"],
  "hotel_preference": "mid-range",
  "activity_level": "moderate",
  "enable_logging": true
}
```

---

## Test Case 4: Tech Enthusiast Trip

**Endpoint**: `POST /api/multi`

```bash
curl -X POST http://localhost:8000/api/multi \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Tokyo, Japan",
    "duration_days": 3,
    "budget": 1500,
    "travelers": 1,
    "interests": ["tech"],
    "hotel_preference": "budget",
    "activity_level": "high",
    "enable_logging": true
  }'
```

**JSON format**:
```json
{
  "destination": "Tokyo, Japan",
  "duration_days": 3,
  "budget": 1500,
  "travelers": 1,
  "interests": ["tech"],
  "hotel_preference": "budget",
  "activity_level": "high",
  "enable_logging": true
}
```

---

## Test Case 5: Single Agent (Demonstrates Failures)

**Endpoint**: `POST /api/single`

```bash
curl -X POST http://localhost:8000/api/single \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Tokyo, Japan",
    "duration_days": 5,
    "budget": 2000,
    "travelers": 2,
    "interests": ["food", "temples"],
    "hotel_preference": "mid-range",
    "enable_logging": true
  }'
```

**JSON format**:
```json
{
  "destination": "Tokyo, Japan",
  "duration_days": 5,
  "budget": 2000,
  "travelers": 2,
  "interests": ["food", "temples"],
  "hotel_preference": "mid-range",
  "enable_logging": true
}
```

**Expected**: Should fail due to budget overruns (single agent doesn't optimize well)

---

## Test Case 6: Tight Budget Challenge

**Endpoint**: `POST /api/multi`

```bash
curl -X POST http://localhost:8000/api/multi \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Tokyo, Japan",
    "duration_days": 5,
    "budget": 1800,
    "travelers": 2,
    "interests": ["food", "temples"],
    "hotel_preference": "budget",
    "activity_level": "low",
    "enable_logging": true
  }'
```

**JSON format**:
```json
{
  "destination": "Tokyo, Japan",
  "duration_days": 5,
  "budget": 1800,
  "travelers": 2,
  "interests": ["food", "temples"],
  "hotel_preference": "budget",
  "activity_level": "low",
  "enable_logging": true
}
```

---

## Test Case 7: Maximum Interests

**Endpoint**: `POST /api/multi`

```bash
curl -X POST http://localhost:8000/api/multi \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Tokyo, Japan",
    "duration_days": 10,
    "budget": 8000,
    "travelers": 2,
    "interests": ["food", "tech", "temples", "shopping", "culture", "nightlife"],
    "hotel_preference": "luxury",
    "activity_level": "high",
    "enable_logging": true
  }'
```

**JSON format**:
```json
{
  "destination": "Tokyo, Japan",
  "duration_days": 10,
  "budget": 8000,
  "travelers": 2,
  "interests": ["food", "tech", "temples", "shopping", "culture", "nightlife"],
  "hotel_preference": "luxury",
  "activity_level": "high",
  "enable_logging": true
}
```

---

## Available Options

### Destinations
- `"Tokyo, Japan"` (currently the only destination in mock data)

### Interests (can combine multiple)
- `"food"` - Culinary experiences, markets, cooking classes
- `"tech"` - Electronics districts, digital art museums
- `"temples"` - Traditional temples and shrines
- `"shopping"` - Shopping districts and stores
- `"culture"` - Cultural experiences
- `"nightlife"` - Evening entertainment

### Hotel Preferences
- `"budget"` - $80-100 per night
- `"mid-range"` - $120-150 per night
- `"luxury"` - $200-300 per night

### Activity Levels
- `"low"` - Relaxed pace, fewer activities
- `"moderate"` - Balanced schedule
- `"high"` - Packed itinerary, maximum activities

---

## Using with Swagger UI (Easiest)

1. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

2. Open http://localhost:8000/docs in your browser

3. Click on **POST /api/multi** endpoint

4. Click **"Try it out"**

5. Paste one of the JSON examples above into the Request body

6. Click **"Execute"**

7. See the response below!

---

## Response Structure

```json
{
  "success": true,
  "message": "Real AWS Multi-Agent Orchestrator completed successfully using Bedrock",
  "execution_time_ms": 9234.56,
  "timestamp": "2025-10-22T18:00:00.000000",
  "status": "success",
  "itinerary": {
    "destination": "Tokyo, Japan",
    "duration_days": 5,
    "total_budget": 3000.0,
    "actual_cost": 2980.0,
    "within_budget": true,
    "flights": { ... },
    "hotel": { ... },
    "activities": [ ... ],
    "cost_breakdown": {
      "flights": 1160.0,
      "accommodation": 750.0,
      "activities": 360.0,
      "food": 426.0,
      "misc": 284.0
    }
  },
  "agent_logs": [
    {
      "agent_name": "Supervisor",
      "timestamp": "2025-10-22T18:00:00.000000",
      "message": "🎯 Starting REAL multi-agent orchestration for Tokyo, Japan",
      "data": { ... }
    },
    ...
  ],
  "agents_used": ["TravelSupervisor"],
  "collaboration_count": 5
}
```

---

## Key Response Fields

- **success**: `true` if planning succeeded
- **execution_time_ms**: Time taken (~8-10 seconds for real AWS SDK)
- **within_budget**: `true` if total cost ≤ budget
- **actual_cost**: Total calculated cost
- **agent_logs**: Detailed logs showing A2A communication (when `enable_logging: true`)
- **flights**: Selected flight details
- **hotel**: Selected hotel details
- **activities**: List of recommended activities
- **cost_breakdown**: Breakdown by category

---

## For Your Tech Talk Demo

### Show Single Agent Failure:
```bash
# Single agent - will likely exceed budget
curl -X POST http://localhost:8000/api/single \
  -H "Content-Type: application/json" \
  -d '{"destination": "Tokyo, Japan", "duration_days": 5, "budget": 2000, "travelers": 2, "interests": ["food"], "enable_logging": true}'
```

### Show Multi-Agent Success:
```bash
# Multi-agent - intelligently stays within budget
curl -X POST http://localhost:8000/api/multi \
  -H "Content-Type: application/json" \
  -d '{"destination": "Tokyo, Japan", "duration_days": 5, "budget": 2000, "travelers": 2, "interests": ["food"], "hotel_preference": "budget", "enable_logging": true}'
```

### Compare Execution Times:
- **Single Agent**: ~1-2ms (hardcoded logic)
- **Multi-Agent with AWS SDK**: ~8-10 seconds (real Bedrock LLM calls)

This proves you're using the REAL AWS Multi-Agent Orchestrator SDK! ⚡

---

## Pretty Print JSON Response

Use `jq` for better formatting:

```bash
curl -s -X POST http://localhost:8000/api/multi \
  -H "Content-Type: application/json" \
  -d '{"destination": "Tokyo, Japan", "duration_days": 5, "budget": 3000, "travelers": 2, "interests": ["food", "tech"], "hotel_preference": "mid-range", "enable_logging": true}' \
  | jq '.'
```

Or just use the Swagger UI at http://localhost:8000/docs - it's much easier! 🚀
