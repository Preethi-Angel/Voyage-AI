# TravelAI Planner - Multi-Agent Architecture Documentation

This document provides a high-level architectural overview of each stage in the TravelAI Planner demo, explaining the purpose, architecture, and how each stage advances the multi-agent capabilities.

---

## Table of Contents
1. [Stage 1: Basic Single Agent](#stage-1-basic-single-agent)
2. [Stage 2: Agent Squad Orchestration](#stage-2-agent-squad-orchestration)
3. [Stage 3: Strands Intelligent Orchestration](#stage-3-strands-intelligent-orchestration)
4. [Stage 4: AP2 Autonomous Payments](#stage-4-ap2-autonomous-payments)
5. [Comparison Matrix](#comparison-matrix)

---

## Stage 1: Basic Single Agent

### Purpose
Demonstrates the **simplest approach** to AI-powered travel planning using a single LLM agent. This stage intentionally shows the **limitations** of a basic implementation.

### Architecture

```
┌─────────────┐
│   User      │
│  Request    │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│     Single Agent (Basic)            │
│                                     │
│  ┌───────────────────────────────┐ │
│  │  Bedrock LLM                  │ │
│  │  (claude-3-haiku)             │ │
│  │                               │ │
│  │  • Receives full request      │ │
│  │  • Makes all decisions alone  │ │
│  │  • No specialization          │ │
│  │  • No budget optimization     │ │
│  └───────────────────────────────┘ │
└─────────────────────────────────────┘
       │
       ▼
┌─────────────┐
│   Mock      │
│   Data      │
│  (Flights,  │
│   Hotels,   │
│ Activities) │
└─────────────┘
       │
       ▼
┌─────────────┐
│  Response   │
│ (Often Over │
│   Budget!)  │
└─────────────┘
```

### Key Characteristics

**Pros:**
- Simple to implement
- Fast response time
- Minimal infrastructure

**Cons:**
- ❌ No specialization - one agent tries to do everything
- ❌ Poor budget optimization
- ❌ No collaboration between different expertise areas
- ❌ Single point of failure
- ❌ **Often exceeds budget constraints**

### Why This Stage Matters
This stage establishes the **baseline problem** - showing that a single agent, while functional, lacks the sophistication needed for complex, multi-faceted tasks like budget-constrained travel planning. It motivates the need for multi-agent architectures.

---

## Stage 2: Agent Squad Orchestration

### Purpose
Demonstrates **intelligent intent classification and routing** to specialized agents using AWS Agent Squad framework (formerly Multi-Agent Orchestrator). This shows how to break down complex tasks and route them to the right specialists.

### Architecture

```
┌─────────────┐
│   User      │
│  Request    │
└──────┬──────┘
       │
       ▼
┌──────────────────────────────────────────────────────┐
│          Agent Squad Orchestrator                    │
│                                                      │
│  ┌────────────────────────────────────────────────┐ │
│  │  Intent Classifier (Bedrock)                   │ │
│  │  • Analyzes user request                       │ │
│  │  • Determines which specialist is needed       │ │
│  └──────────────┬─────────────────────────────────┘ │
│                 │                                    │
│                 ▼                                    │
│  ┌──────────────────────────────────────────────┐  │
│  │         Routing Engine                        │  │
│  │  Routes to appropriate specialist agent       │  │
│  └──┬───────┬──────────┬──────────┬─────────────┘  │
│     │       │          │          │                 │
│     ▼       ▼          ▼          ▼                 │
│  ┌────┐ ┌──────┐ ┌─────────┐ ┌────────┐           │
│  │Flight│ │Hotel│ │Activity│ │Budget │            │
│  │Agent│ │Agent│ │ Agent  │ │Optimizer│           │
│  └────┘ └──────┘ └─────────┘ └────────┘           │
│                                                      │
│  Each agent has:                                    │
│  • Isolated context                                 │
│  • Specialized expertise                            │
│  • Bedrock LLM backing                             │
└──────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────┐
│  Supervisor │
│    Agent    │
│  Synthesizes│
│   Results   │
└─────────────┘
       │
       ▼
┌─────────────┐
│  Response   │
│ (Better     │
│  Budget     │
│  Control)   │
└─────────────┘
```

### Key Characteristics

**Routing Strategy:**
- **Intent-based routing**: Classifier determines user intent
- **Context isolation**: Each specialist agent has its own conversation context
- **Sequential processing**: Agents are called one at a time based on need

**Agent Roles:**
- **FlightAgent**: Specializes in flight selection
- **HotelAgent**: Focuses on accommodation matching
- **ActivityAgent**: Curates activities based on interests
- **BudgetAgent**: Optimizes cost allocation
- **TravelSupervisor**: Coordinates and synthesizes results

**Important Note:**
- ⚠️ This is **NOT** Agent-to-Agent (A2A) communication
- ✅ This is **centralized orchestration** - agents don't talk to each other
- ✅ Orchestrator routes requests and aggregates responses

### Why This Advances
- ✅ **Specialization**: Each agent focuses on one domain
- ✅ **Better decision making**: Domain experts make better choices
- ✅ **Improved budget control**: Dedicated budget optimization agent
- ✅ **Scalability**: Easy to add new specialist agents
- ❌ **Limitation**: Still centralized coordination, no true agent collaboration

---

## Stage 3: Strands Intelligent Orchestration

### Purpose
Demonstrates **model-driven orchestration** where the LLM itself decides which tools (agents) to use and in what order. This enables dynamic, adaptive, and parallel agent execution with true **Agent-to-Agent (A2A) communication**.

### Architecture

```
┌─────────────┐
│   User      │
│  Request    │
└──────┬──────┘
       │
       ▼
┌────────────────────────────────────────────────────────────┐
│          Strands Intelligent Orchestrator                  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  Meta-Agent (Complexity Analyzer)                     │ │
│  │  • Analyzes trip complexity                           │ │
│  │  • Determines orchestration strategy                  │ │
│  │  • Decides: Sequential vs Swarm vs Parallel          │ │
│  └──────────────────┬───────────────────────────────────┘ │
│                     │                                      │
│                     ▼                                      │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  Coordinator Agent (Bedrock LLM)                      │ │
│  │  • Model-driven decision making                       │ │
│  │  • Autonomous tool selection                          │ │
│  │  • Dynamic agent spawning                             │ │
│  └──────────────────┬───────────────────────────────────┘ │
│                     │                                      │
│          ┌──────────┴──────────┐                          │
│          │                     │                          │
│      Sequential            Swarm Mode                      │
│     (Simple trips)     (Complex trips)                     │
│          │                     │                          │
│          ▼                     ▼                          │
│  ┌──────────────┐    ┌─────────────────────────────────┐ │
│  │ Tools called │    │  Parallel Tool Execution        │ │
│  │ one by one   │    │  ┌─────┐ ┌─────┐ ┌──────────┐  │ │
│  │              │    │  │Flight│ │Hotel│ │Activities│  │ │
│  │              │    │  │Tool │ │Tool │ │   Tool   │  │ │
│  │              │    │  └──┬──┘ └──┬──┘ └────┬─────┘  │ │
│  └──────────────┘    │     └────┬───┘────────┘        │ │
│                      │          │                      │ │
│                      │    ┌─────▼──────┐              │ │
│                      │    │  Budget    │              │ │
│                      │    │   Tool     │              │ │
│                      │    └────────────┘              │ │
│                      └─────────────────────────────────┘ │
│                                                           │
│  Tools = Specialized Functions:                          │
│  • search_flights(destination, preferences)              │
│  • search_hotels(destination, duration, type)            │
│  • search_activities(interests, budget)                  │
│  • calculate_budget_breakdown(costs)                     │
│                                                           │
│  A2A Support:                                            │
│  • Agents can communicate with each other                │
│  • Tools can be wrapped as A2A-enabled agents            │
│  • Network-accessible agent collaboration                │
└───────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────┐
│  Response   │
│ (Optimized  │
│ with Intel- │
│  ligent     │
│  Strategy)  │
└─────────────┘
```

### Key Characteristics

**Model-Driven Orchestration:**
- **LLM decides**: The Bedrock model autonomously chooses which tools to use
- **Dynamic strategy**: Adapts approach based on trip complexity
- **Parallel execution**: For complex trips, tools run simultaneously (Swarm Mode)

**Complexity Analysis:**
```
Simple Trip (1-2 days, few interests):
  → Sequential execution
  → 4-6 tools used

Moderate Trip (3-5 days, multiple interests):
  → Hybrid approach
  → 6-8 tools used

Complex Trip (7+ days, many interests, tight budget):
  → SWARM MODE ACTIVATED
  → 8+ tools in parallel
  → Maximum optimization
```

**A2A (Agent-to-Agent) Communication:**
- ✅ Agents can discover and call other agents
- ✅ Network-accessible collaboration
- ✅ Standardized communication protocol
- ✅ Agents act as tools for each other

### Why This Advances
- ✅ **Intelligence**: LLM makes orchestration decisions
- ✅ **Adaptability**: Strategy changes based on complexity
- ✅ **Parallelism**: Multiple agents work simultaneously
- ✅ **Efficiency**: Faster for complex scenarios
- ✅ **True collaboration**: Agents can communicate peer-to-peer (A2A)
- ✅ **Autonomy**: Minimal hardcoded logic, LLM-driven

**Key Difference from Stage 2:**
- Stage 2: Centralized router decides which agent to call
- Stage 3: **LLM autonomously decides** which tools to use and when

---

## Stage 4: AP2 Autonomous Payments

### Purpose
Demonstrates **autonomous agent payments** using the AP2 (Agents Payments Protocol). This shows how agents can autonomously handle financial transactions with user-delegated payment authority.

### Architecture

```
┌─────────────┐
│   User      │
│  Request +  │
│  Budget     │
│  Delegation │
└──────┬──────┘
       │
       ▼
┌────────────────────────────────────────────────────────────┐
│          AP2 Autonomous Payment Protocol                   │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  Step 1: Intent Mandate                               │ │
│  │  Agent declares: "I intend to book trip to Tokyo"    │ │
│  │  User reviews and authorizes                          │ │
│  └────────────────────┬─────────────────────────────────┘ │
│                       │                                    │
│                       ▼                                    │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  Step 2: Cart Building                                │ │
│  │  Agent autonomously:                                  │ │
│  │  • Searches and selects flights                       │ │
│  │  • Books hotels                                       │ │
│  │  • Reserves activities                                │ │
│  │  • Builds transaction cart                            │ │
│  └────────────────────┬─────────────────────────────────┘ │
│                       │                                    │
│                       ▼                                    │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  Step 3: Payment Mandate                              │ │
│  │  Agent requests: "Authorize $2,850 payment"          │ │
│  │  • Shows itemized breakdown                           │ │
│  │  • User reviews and approves                          │ │
│  └────────────────────┬─────────────────────────────────┘ │
│                       │                                    │
│                       ▼                                    │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  Step 4: Autonomous Execution                         │ │
│  │  Agent executes transactions:                         │ │
│  │  • Processes payments autonomously                    │ │
│  │  • Updates wallet balance                             │ │
│  │  • Records blockchain proof (mock)                    │ │
│  │  • Generates receipt                                  │ │
│  └────────────────────┬─────────────────────────────────┘ │
│                       │                                    │
│                       ▼                                    │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  Step 5: Verification & Receipt                       │ │
│  │  • Transaction verified                               │ │
│  │  • Receipt ID: AP2-xxx-xxx                           │ │
│  │  • Blockchain hash recorded                           │ │
│  │  • Wallet updated                                     │ │
│  └──────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│  Mock Wallet Integration         │
│  • Initial balance: $5000        │
│  • Transaction: -$2850           │
│  • Remaining: $2150              │
│  • Transaction logged            │
└─────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│  Complete Trip Package           │
│  • All bookings confirmed        │
│  • Payment receipt               │
│  • Blockchain proof              │
│  • Detailed itinerary            │
└─────────────────────────────────┘
```

### AP2 Protocol Flow

```
User                  Agent                 Payment System
  │                     │                          │
  │  1. Trip Request    │                          │
  ├────────────────────>│                          │
  │                     │                          │
  │  2. Intent Mandate  │                          │
  │<────────────────────┤                          │
  │  "I intend to book  │                          │
  │   Tokyo trip"       │                          │
  │                     │                          │
  │  3. Approve Intent  │                          │
  ├────────────────────>│                          │
  │                     │                          │
  │                     │  4. Build Cart           │
  │                     │  (autonomous)            │
  │                     │                          │
  │  5. Payment Mandate │                          │
  │<────────────────────┤                          │
  │  "Authorize $2850"  │                          │
  │                     │                          │
  │  6. Approve Payment │                          │
  ├────────────────────>│                          │
  │                     │                          │
  │                     │  7. Execute Transaction  │
  │                     ├─────────────────────────>│
  │                     │                          │
  │                     │  8. Transaction Confirmed│
  │                     │<─────────────────────────┤
  │                     │                          │
  │  9. Receipt         │                          │
  │<────────────────────┤                          │
  │                     │                          │
```

### Key Characteristics

**Autonomous Capabilities:**
- ✅ Agent makes purchasing decisions within delegated authority
- ✅ User maintains control through authorization gates
- ✅ Transparent itemized breakdown before payment
- ✅ Blockchain-verified transactions (mock implementation)

**Security & Trust:**
- **Intent Declaration**: Agent must declare what it intends to do
- **User Authorization**: User approves before agent acts
- **Payment Mandate**: Specific amount approval required
- **Audit Trail**: All transactions logged and verified
- **Wallet Balance**: Real-time balance tracking

**Mock Implementation:**
- Uses simulated wallet with $5000 initial balance
- Mock blockchain hash generation
- Mock payment processing
- Real AP2 protocol flow demonstration

### Why This Advances
- ✅ **Autonomy**: Agents can complete end-to-end transactions
- ✅ **Trust**: Protocol ensures user control and transparency
- ✅ **Real-world applicability**: Demonstrates practical agent commerce
- ✅ **Future-ready**: Shows the path to autonomous agent economies
- ✅ **User safety**: Multiple authorization checkpoints

**Use Cases:**
- Travel booking agents
- Personal shopping assistants
- Bill payment automation
- Subscription management
- Autonomous procurement

---

## Comparison Matrix

| Feature | Stage 1 | Stage 2 | Stage 3 | Stage 4 |
|---------|---------|---------|---------|---------|
| **Framework** | Single Agent | Agent Squad | Strands | AP2 + Agents |
| **Agent Count** | 1 | 5+ specialists | Dynamic (4-8+) | Payment + Planning |
| **Orchestration** | None | Centralized routing | Model-driven | Protocol-driven |
| **Specialization** | ❌ None | ✅ Domain experts | ✅ Tool-based | ✅ Payment focused |
| **Budget Control** | ❌ Poor | ✅ Better | ✅ Excellent | ✅ Strict (wallet) |
| **Parallelism** | ❌ No | ❌ No | ✅ Yes (Swarm) | ⚠️ Sequential protocol |
| **A2A Communication** | ❌ No | ❌ No | ✅ Yes | ✅ Yes (AP2) |
| **Adaptability** | ❌ Static | ⚠️ Fixed routes | ✅ Dynamic | ✅ Protocol-based |
| **Complexity** | Low | Medium | High | Very High |
| **Real-world Ready** | ❌ Demo only | ✅ Production-ready | ✅ Production-ready | ⚠️ Emerging standard |
| **AWS Service** | Bedrock | Agent Squad | Strands | Custom (AP2) |

---

## Progression Summary

### Stage 1 → Stage 2: **From Monolith to Specialists**
- **Problem**: Single agent can't optimize complex multi-faceted tasks
- **Solution**: Break into specialized agents with centralized routing
- **Gain**: Better domain expertise, improved results

### Stage 2 → Stage 3: **From Routing to Intelligence**
- **Problem**: Static routing can't adapt to varying complexity
- **Solution**: Let the LLM decide orchestration strategy
- **Gain**: Dynamic adaptation, parallel execution, A2A communication

### Stage 3 → Stage 4: **From Planning to Execution**
- **Problem**: Agents can plan but can't transact
- **Solution**: Add autonomous payment capability with user oversight
- **Gain**: End-to-end autonomous workflows, real commerce

---

## Technology Stack

### Backend
- **Python 3.12**: Core runtime
- **FastAPI**: Web framework
- **AWS Bedrock**: LLM service (Claude 3 Haiku)
- **Agent Squad (v1.0.2)**: Multi-agent orchestration
- **Strands SDK (v1.13.0)**: Model-driven orchestration with A2A
- **AP2 Protocol**: Autonomous payments (custom implementation)

### Frontend
- **React 18**: UI framework
- **TypeScript**: Type safety
- **Tailwind CSS**: Styling
- **Vite**: Build tool
- **Server-Sent Events (SSE)**: Real-time streaming

### AWS Services
- **Amazon Bedrock**: Foundation model hosting
- **Claude 3 Haiku**: LLM model
- **Agent Squad Framework**: Intent classification & routing
- **Strands Agents SDK**: Tool-based orchestration

---

## Running the Demo

### Prerequisites
```bash
# Python 3.12+
# Node.js 18+
# AWS credentials configured
```

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set AWS credentials
export AWS_REGION=us-east-1
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret

# Run server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Access
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## Key Takeaways

1. **Single agents have limitations** - demonstrated by Stage 1's poor budget control
2. **Specialization improves outcomes** - Stage 2 shows domain experts make better decisions
3. **Intelligence beats hardcoded logic** - Stage 3's model-driven approach adapts dynamically
4. **Autonomy requires oversight** - Stage 4's AP2 protocol balances automation with user control
5. **Progression is meaningful** - Each stage solves real problems from the previous stage

---

## Future Enhancements

- **Multi-modal agents**: Add vision capabilities for hotel/destination images
- **Real payment integration**: Connect to actual payment processors
- **Distributed A2A**: Deploy agents across different services/networks
- **Learning agents**: Implement memory and learning from past trips
- **Human-in-the-loop**: Add collaborative decision-making workflows

---

## References

- [AWS Agent Squad Documentation](https://awslabs.github.io/agent-squad/)
- [Strands Agents SDK](https://strandsagents.com/)
- [AP2 Protocol Specification](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/multi-agent/agent-to-agent/)
- [Amazon Bedrock](https://aws.amazon.com/bedrock/)
- [Multi-Agent Systems Patterns](https://aws.amazon.com/blogs/opensource/introducing-strands-agents-1-0-production-ready-multi-agent-orchestration-made-simple/)
