# 🧙‍♂️ AI Travel Planner - Agentic AI Demo

**Wizards of Agentic AI: A2A and AP2 Unleashed**

A production-ready demonstration of agentic AI concepts using AWS services, showcasing the evolution from single-agent failures to sophisticated multi-agent orchestration.

---

## 🎯 What This Demo Shows

This application demonstrates 5 progressive stages of agentic AI development:

1. **Single Agent (The Failure)** - Shows limitations of monolithic AI agents
2. **Multi-Agent with A2A** - AWS Multi-Agent Orchestrator for collaboration
3. **Strands Workflow** - Long-running stateful workflows with validation
4. **Guardrails** - Production security with AWS Bedrock Guardrails
5. **AP2 Protocol** - Autonomous agent payments for API services

### Use Case: AI Travel Planning Assistant
**Query:** "Plan a 5-day trip to Japan under $3000"

---

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│   React Frontend (Vite)             │
│   - 6 Demo Pages (Progressive)      │
│   - Real-time Agent Visualization   │
│   Deploy: AWS S3 + CloudFront       │
└──────────────┬──────────────────────┘
               ↓
┌──────────────────────────────────────┐
│   FastAPI Backend                    │
│   - 5 Stage Endpoints                │
│   - AWS Multi-Agent Orchestrator     │
│   Deploy: AWS Lambda + API Gateway   │
└──────────────┬───────────────────────┘
               ↓
┌──────────────────────────────────────┐
│   AWS Bedrock                        │
│   - Claude 3.5 Sonnet                │
│   - Multi-Agent Collaboration        │
│   - Guardrails                       │
└──────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- AWS Account with Bedrock access
- AWS CLI configured

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set AWS credentials
export AWS_REGION=us-east-1
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret

# Run development server
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Visit: http://localhost:5173

---

## 📁 Project Structure

```
travel-agent-demo/
├── backend/
│   ├── app/
│   │   ├── main.py                    # FastAPI entry point
│   │   ├── routers/
│   │   │   ├── single.py              # Stage 1: Single agent
│   │   │   ├── multi.py               # Stage 2: Multi-agent A2A
│   │   │   ├── strands.py             # Stage 3: Strands workflow
│   │   │   ├── guardrails.py          # Stage 4: Security
│   │   │   └── ap2.py                 # Stage 5: Autonomous payments
│   │   ├── agents/
│   │   │   ├── single_agent.py
│   │   │   ├── flight_agent.py
│   │   │   ├── hotel_agent.py
│   │   │   ├── activity_agent.py
│   │   │   └── budget_agent.py
│   │   ├── services/
│   │   │   ├── bedrock_service.py
│   │   │   ├── orchestrator_service.py
│   │   │   ├── guardrails_service.py
│   │   │   └── ap2_service.py
│   │   └── models/
│   │       ├── requests.py
│   │       └── responses.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── 01-SingleAgent.jsx
│   │   │   ├── 02-MultiAgent.jsx
│   │   │   ├── 03-Strands.jsx
│   │   │   ├── 04-Guardrails.jsx
│   │   │   ├── 05-AP2.jsx
│   │   │   └── 06-Complete.jsx
│   │   ├── components/
│   │   │   ├── AgentVisualizer.jsx
│   │   │   ├── WorkflowGraph.jsx
│   │   │   ├── CostMeter.jsx
│   │   │   └── TripCard.jsx
│   │   └── App.jsx
│   └── package.json
├── deploy/
│   ├── template.yaml              # AWS SAM template
│   └── deploy.sh                  # Deployment script
└── docs/
    ├── ARCHITECTURE.md
    ├── DEMO_SCRIPT.md
    └── API.md
```

---

## 🎭 Demo Flow (50 minutes)

### Act 1: A2A Multi-Agent Magic (10 min)
- Show single agent failure
- Introduce multi-agent orchestration
- Live demo with AWS Multi-Agent Orchestrator SDK

### Act 2: Strands Spell Crafting (10 min)
- Show workflow breaks without state management
- Demonstrate Strands workflow with validation loops
- Human-in-the-loop approvals

### Act 3: Guardrails Protection Shield (10 min)
- Demonstrate security vulnerabilities
- Show prompt injection attacks
- Deploy Bedrock Guardrails protection

### Act 4: AP2 Autonomous Commerce (8 min)
- Show traditional API subscription costs
- Demonstrate autonomous micropayments
- Cost comparison visualization

### Finale: Complete System (4 min)
- All stages working together
- Production AWS deployment
- GitHub boilerplate walkthrough

---

## 🛠️ Technology Stack

### Backend
- **FastAPI** - High-performance async API framework
- **AWS Bedrock** - LLM foundation (Claude 3.5 Sonnet)
- **AWS Multi-Agent Orchestrator** - Agent collaboration framework
- **Pydantic** - Data validation

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **TailwindCSS** - Styling
- **Recharts** - Data visualization

### AWS Services
- **Lambda** - Serverless compute
- **API Gateway** - REST API
- **S3** - Static hosting
- **CloudFront** - CDN
- **Bedrock** - AI/ML
- **CloudWatch** - Logging

---

## 📊 API Endpoints

| Endpoint | Description | Stage |
|----------|-------------|-------|
| `POST /api/single` | Single agent (fails gracefully) | 1 |
| `POST /api/multi` | Multi-agent A2A orchestration | 2 |
| `POST /api/strands` | Strands workflow with validation | 3 |
| `POST /api/guardrails` | Protected with security guardrails | 4 |
| `POST /api/ap2` | Autonomous payments enabled | 5 |

---

## 🔒 Security Features

- **Bedrock Guardrails** - Content filtering, PII detection
- **API Authentication** - JWT tokens (production)
- **Rate Limiting** - Prevent abuse
- **Input Validation** - Pydantic schemas
- **CORS Configuration** - Secure origins

---

## 💰 Cost Optimization

### Traditional Approach
- Flight API: $99/month
- Hotel API: $149/month
- Activity API: $79/month
- **Total: $327/month**

### With AP2 Protocol
- Pay-per-use: ~$0.15 per trip query
- **~99.5% cost reduction**

---

## 🚢 Deployment

### Using AWS SAM
```bash
cd deploy
./deploy.sh
```

### Manual Deployment
```bash
# Backend
cd backend
sam build
sam deploy --guided

# Frontend
cd frontend
npm run build
aws s3 sync dist/ s3://your-bucket-name
```

---

## 📖 Documentation

- [Architecture Deep-Dive](docs/ARCHITECTURE.md)
- [Demo Script](docs/DEMO_SCRIPT.md)
- [API Reference](docs/API.md)

---

## 🤝 Contributing

This is a demo/boilerplate project. Feel free to:
- Fork and extend
- Add more agents
- Integrate real APIs
- Improve UI/UX

---

## 📄 License

MIT License - Use freely for learning and production

---

## 🎓 Learning Resources

- [AWS Multi-Agent Orchestrator Docs](https://docs.aws.amazon.com/bedrock/)
- [Strands Protocol](https://strands.com)
- [AP2 Protocol Spec](https://ap2-protocol.org/)
- [Bedrock Guardrails Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html)

---

## 🧙‍♂️ Built by Wizards

Created for the "Wizards of Agentic AI: A2A and AP2 Unleashed" tech talk.

**May your agents collaborate wisely!** ✨
