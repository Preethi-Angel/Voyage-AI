"""
Router for Stage 2: AWS Multi-Agent Orchestrator SDK

This uses the REAL AWS Multi-Agent Orchestrator SDK to demonstrate
true A2A (Agent-to-Agent) communication with Bedrock LLM agents.
"""
import json
import asyncio
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.models.requests import MultiAgentRequest
from app.models.responses import MultiAgentResponse
from app.agents.multi_agent_orchestrator import MultiAgentOrchestrator

router = APIRouter(prefix="/api/multi", tags=["Stage 2: AWS Multi-Agent Orchestrator"])


@router.post("", response_model=MultiAgentResponse)
async def plan_trip_multi_agent(request: MultiAgentRequest) -> MultiAgentResponse:
    """
    **Stage 2: AWS Multi-Agent Orchestrator with Real A2A Communication**

    This endpoint uses the **REAL AWS Multi-Agent Orchestrator SDK** from AWS Labs
    to demonstrate true Agent-to-Agent (A2A) communication using Bedrock LLM agents.

    **What Makes This Real:**
    - ✅ Uses `multi-agent-orchestrator` package from AWS Labs
    - ✅ Real Bedrock LLM calls (Claude 3 Haiku)
    - ✅ True A2A communication via AWS SDK
    - ✅ LLM-powered intelligent decision making
    - ✅ Conversation memory and context management

    **How It Works:**
    1. AWS orchestrator receives trip planning request
    2. TravelSupervisor agent (Bedrock-powered) analyzes requirements
    3. Agent uses Claude 3 Haiku to make intelligent decisions about:
       - Best flight options within budget
       - Optimal hotel selection
       - Activity recommendations matching interests
       - Budget allocation across components
    4. Returns comprehensive travel plan with AI reasoning

    **Improvements Over Single Agent:**
    - ✅ Real LLM reasoning (not hardcoded logic)
    - ✅ Intelligent trade-offs between cost and quality
    - ✅ Natural language explanations for choices
    - ✅ Production-ready AWS SDK
    - ✅ Automatic error handling and retries

    **Example Request:**
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

    **Performance:**
    - Execution time: ~8-10 seconds (real Bedrock API calls)
    - Cost: ~$0.01-0.02 per request (Haiku model)
    """
    try:
        orchestrator = MultiAgentOrchestrator()
        response = await orchestrator.plan_trip(request)
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stream")
async def plan_trip_multi_agent_stream(request: MultiAgentRequest):
    """
    Stream real-time progress as agents work on the travel plan.
    Uses Server-Sent Events (SSE) to send logs as they happen.
    """
    async def event_generator():
        try:
            orchestrator = MultiAgentOrchestrator()

            # Stream logs and final result
            async for event in orchestrator.plan_trip_stream(request):
                # Send each event as SSE
                yield f"data: {json.dumps(event)}\n\n"
                await asyncio.sleep(0.01)  # Small delay to ensure delivery

        except Exception as e:
            error_event = {
                "type": "error",
                "message": str(e)
            }
            yield f"data: {json.dumps(error_event)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@router.get("/demo-explanation")
async def get_stage_explanation():
    """
    Get explanation of what this stage demonstrates.
    """
    return {
        "stage": 2,
        "name": "Multi-Agent with A2A Communication",
        "purpose": "Demonstrate collaborative multi-agent systems",
        "key_concepts": [
            "Agent specialization",
            "A2A (Agent-to-Agent) communication",
            "Supervisor pattern",
            "Budget-aware planning",
            "Parallel agent execution"
        ],
        "agents": [
            {
                "name": "FlightAgent",
                "role": "Search and recommend flights within budget"
            },
            {
                "name": "HotelAgent",
                "role": "Find accommodation matching preferences and budget"
            },
            {
                "name": "ActivityAgent",
                "role": "Curate activities based on interests and budget"
            },
            {
                "name": "BudgetAgent",
                "role": "Allocate budget and validate total cost"
            }
        ],
        "advantages_over_single_agent": [
            "Specialized expertise per domain",
            "Better budget management",
            "Scalable (can add more agents)",
            "Parallel processing capability",
            "More consistent results"
        ],
        "next_stage": "Strands Workflow (long-running stateful processes)"
    }


@router.get("/agents")
async def list_agents():
    """
    List all available agents and their capabilities.
    """
    return {
        "agents": [
            {
                "name": "FlightAgent",
                "description": "Expert in finding optimal flights within budget constraints",
                "capabilities": [
                    "Search multiple airlines",
                    "Filter by budget",
                    "Optimize for stops vs price",
                    "Calculate total cost for group"
                ]
            },
            {
                "name": "HotelAgent",
                "description": "Expert in finding accommodation matching preferences and budget",
                "capabilities": [
                    "Filter by budget and preference",
                    "Rate-based selection",
                    "Calculate total accommodation cost",
                    "Match location to itinerary"
                ]
            },
            {
                "name": "ActivityAgent",
                "description": "Expert in curating activities based on interests and budget",
                "capabilities": [
                    "Interest-based recommendations",
                    "Budget-aware selection",
                    "Activity scheduling",
                    "Category balancing"
                ]
            },
            {
                "name": "BudgetAgent",
                "description": "Expert in budget allocation and financial optimization",
                "capabilities": [
                    "Intelligent budget allocation",
                    "Cost validation",
                    "Optimization recommendations",
                    "Financial reporting"
                ]
            }
        ],
        "total_agents": 4
    }
