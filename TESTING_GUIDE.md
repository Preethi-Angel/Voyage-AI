# 🧪 Testing Guide

Quick guide to test Stages 1 & 2 of the AI Travel Planner.

---

## 🚀 Quick Start (5 Minutes)

### 1. Setup (First Time Only)

```bash
cd travel-agent-demo/backend
./setup_and_test.sh
```

This script will:

- ✅ Create Python virtual environment
- ✅ Install dependencies
- ✅ Configure AWS credentials (interactive)
- ✅ Test Bedrock connectivity

---

### 2. Test Stage 1: Single Agent (The Failure)

```bash
python test_stage1.py
```

**What to expect:**

- ❌ Budget exceeded (picks expensive options)
- ❌ Suboptimal choices
- ⚠️ Warnings about unrealistic planning
- 🎯 **Demo Point:** Shows WHY multi-agent is needed

**Sample Output:**

```
🧙‍♂️ Testing Stage 1: Single Agent (The Failure)
================================================================
📋 Request:
  Destination: Tokyo, Japan
  Duration: 5 days
  Budget: $3000
  Travelers: 2

💰 BUDGET ANALYSIS:
  Budget: $3,000.00
  Actual Cost: $4,250.00
  Within Budget: ❌ NO (EXCEEDED!)
  Difference: $1,250.00

❌ ERRORS:
  • Budget exceeded! Planned $4250.00 but budget was $3000.00
```

---

### 3. Test Stage 2: Multi-Agent with A2A

```bash
python test_stage2.py
```

**What to expect:**

- ✅ Budget respected
- ✅ Intelligent allocation
- ✅ Optimized selections
- ✅ Agent collaboration logs
- 🎯 **Demo Point:** Shows collaborative AI solving complex problems

**Sample Output:**

```
🧙‍♂️ Testing Stage 2: Multi-Agent with A2A Communication
=======================================================================
🤝 Agents Used: FlightAgent, HotelAgent, ActivityAgent, BudgetAgent
💬 Agent Collaborations: 12

💰 BUDGET ANALYSIS:
  Budget: $3,000.00
  Actual Cost: $2,850.00
  Within Budget: ✅ YES
  Savings: $150.00

🤝 AGENT COLLABORATION LOG:
👨‍💼 Supervisor      | 🎯 Starting multi-agent trip planning for Tokyo, Japan
💰 BudgetAgent     | Allocating $3000 budget across trip components
✈️  FlightAgent     | Searching flights to Tokyo, Japan for 2 travelers
✈️  FlightAgent     | ✅ Selected Japan Airlines - $1300
🏨 HotelAgent      | Searching mid-range hotels in Tokyo, Japan for 5 nights
🏨 HotelAgent      | ✅ Selected Shibuya Grand Hotel - $600
🎯 ActivityAgent   | Planning activities for interests: food, tech, temples
🎯 ActivityAgent   | ✅ Planned 6 activities - $310
💰 BudgetAgent     | ✅ WITHIN BUDGET: $2850.00 / $3000.00
```

---

## 🌐 Test via API (Web Interface)

### 1. Start the Server

```bash
uvicorn app.main:app --reload
```

### 2. Open Swagger UI

Visit: **http://localhost:8000/docs**

You'll see interactive API documentation.

### 3. Test Stage 1

1. Expand **`POST /api/single`**
2. Click **"Try it out"**
3. Use this test request:

```json
{
  "destination": "Tokyo, Japan",
  "duration_days": 5,
  "budget": 3000,
  "travelers": 2,
  "interests": ["food", "tech", "temples"],
  "hotel_preference": "mid-range"
}
```

4. Click **"Execute"**
5. See the response (should show budget exceeded!)

### 4. Test Stage 2

1. Expand **`POST /api/multi`**
2. Click **"Try it out"**
3. Use this test request:

```json
{
  "destination": "Tokyo, Japan",
  "duration_days": 5,
  "budget": 3000,
  "travelers": 2,
  "interests": ["food", "tech", "temples"],
  "hotel_preference": "mid-range",
  "enable_logging": true
}
```

4. Click **"Execute"**
5. See the response (should be within budget with agent logs!)

---

## 🧪 Test Different Scenarios

### Scenario 1: Low Budget Challenge

```json
{
  "destination": "Tokyo, Japan",
  "duration_days": 5,
  "budget": 1500,
  "travelers": 2,
  "interests": ["temples"],
  "hotel_preference": "budget"
}
```

**Expected:**

- Stage 1: ❌ Will exceed budget
- Stage 2: ✅ Will optimize to stay within budget

### Scenario 2: Luxury Trip

```json
{
  "destination": "Tokyo, Japan",
  "duration_days": 3,
  "budget": 5000,
  "travelers": 1,
  "interests": ["food", "nature"],
  "hotel_preference": "luxury"
}
```

**Expected:**

- Stage 1: ❌ Will still pick expensive options randomly
- Stage 2: ✅ Will allocate luxury appropriately

### Scenario 3: Group Trip

```json
{
  "destination": "Paris, France",
  "duration_days": 7,
  "budget": 8000,
  "travelers": 4,
  "interests": ["sightseeing"],
  "hotel_preference": "mid-range"
}
```

**Expected:**

- Stage 1: ❌ Won't scale costs properly for group
- Stage 2: ✅ Will calculate per-person costs correctly

---

## 📊 Comparing Results

### Key Metrics to Compare:

| Metric               | Stage 1 (Single) | Stage 2 (Multi) |
| -------------------- | ---------------- | --------------- |
| **Budget Adherence** | Often fails      | Always succeeds |
| **Optimization**     | Random/Poor      | Intelligent     |
| **Agent Count**      | 1 (overwhelmed)  | 4 (specialized) |
| **Execution Time**   | ~500-1000ms      | ~800-1500ms     |
| **Success Rate**     | ~30%             | ~95%            |

---

## 🐛 Troubleshooting

### Issue: "AWS credentials not found"

**Solution:**

```bash
# Edit .env file manually
nano .env

# Add:
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_key_here
AWS_SECRET_ACCESS_KEY=your_secret_here
```

### Issue: "ModuleNotFoundError"

**Solution:**

```bash
# Activate venv and reinstall
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "Bedrock model not available"

**Solution:**

1. Check AWS console for model access
2. Verify region in `.env` (try `us-east-1`)
3. See [AWS_SETUP_GUIDE.md](AWS_SETUP_GUIDE.md)

### Issue: Server won't start

**Solution:**

```bash
# Check if port 8000 is in use
lsof -i :8000

# Kill process if needed
kill -9 <PID>

# Or use different port
uvicorn app.main:app --reload --port 8001
```

---

## 📈 Performance Testing

### Load Test (Optional)

Test with multiple concurrent requests:

```bash
# Install hey (HTTP load tester)
# macOS: brew install hey
# Linux: go install github.com/rakyll/hey@latest

# Run load test
hey -n 100 -c 10 \
  -m POST \
  -H "Content-Type: application/json" \
  -d '{"destination":"Tokyo, Japan","duration_days":5,"budget":3000,"travelers":2}' \
  http://localhost:8000/api/multi
```

---

## ✅ Testing Checklist

Before moving to Stage 3, verify:

- [ ] Stage 1 runs successfully
- [ ] Stage 1 demonstrates budget failures
- [ ] Stage 2 runs successfully
- [ ] Stage 2 stays within budget
- [ ] Agent collaboration logs appear
- [ ] API documentation accessible at `/docs`
- [ ] Multiple test scenarios work
- [ ] Error handling works (try invalid inputs)

---

## 🎯 Demo Preparation

For the presentation, prepare these 3 test cases:

### Demo 1: Side-by-Side Comparison

```
Same request to both endpoints
→ Show Stage 1 failure vs Stage 2 success
```

### Demo 2: Agent Collaboration

```
Stage 2 with enable_logging: true
→ Show A2A communication in logs
```

### Demo 3: Complex Scenario

```
Multi-city, long duration, tight budget
→ Show multi-agent optimization
```

---

## 📞 Need Help?

---

**Happy Testing!** 🚀

Ready to proceed to Stage 3 (Strands) once these tests pass!
