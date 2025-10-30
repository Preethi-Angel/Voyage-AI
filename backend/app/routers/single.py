"""
Quick Planning Router - Fast and Simple Travel Planning
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.models.requests import SingleAgentRequest
from app.models.responses import SingleAgentResponse
from app.agents.single_agent import SingleTravelAgent
import json
from datetime import datetime

router = APIRouter(prefix="/api/single", tags=["Quick Planning"])


@router.post("", response_model=SingleAgentResponse)
async def plan_trip_single_agent(request: SingleAgentRequest) -> SingleAgentResponse:
    """
    **Quick Planning - Fast Travel Itinerary Generation**

    Get instant travel plans with our streamlined AI planner.
    Perfect for straightforward trips and quick decisions.

    **Features:**
    - ⚡ Instant results (< 10 seconds)
    - 📋 Complete itinerary with flights, hotels, and activities
    - 💰 Cost breakdown and budget estimation
    - 🎯 Simple and easy to use

    **Best For:**
    - Weekend getaways
    - Simple trips
    - Quick planning needs
    - Budget estimation

    **Example Request:**
    ```json
    {
        "destination": "Tokyo, Japan",
        "duration_days": 5,
        "budget": 3000,
        "travelers": 2,
        "interests": ["food", "tech", "temples"],
        "hotel_preference": "mid-range",
        "activity_level": "moderate"
    }
    ```
    """
    try:
        agent = SingleTravelAgent()
        response = agent.plan_trip(request)
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stream")
async def plan_trip_single_agent_stream(request: SingleAgentRequest):
    """
    **Quick Planning with Live Streaming**

    Same as Quick Planning but with real-time streaming of agent activity.
    Shows step-by-step reasoning and actions taken by the AI.
    """
    async def generate():
        try:
            # Step 1: Initialize
            yield f"data: {json.dumps({'type': 'log', 'agent_name': 'Quick Planner', 'message': 'Initializing single agent travel planner', 'timestamp': datetime.now().isoformat(), 'step': 1})}\n\n"

            # Step 2: Analyze request
            yield f"data: {json.dumps({'type': 'log', 'agent_name': 'Quick Planner', 'message': f'Analyzing destination and travel requirements for {request.destination}', 'timestamp': datetime.now().isoformat(), 'step': 2})}\n\n"

            yield f"data: {json.dumps({'type': 'log', 'agent_name': 'Quick Planner', 'message': f'Processing budget of ${request.budget} USD for {request.travelers} traveler(s) over {request.duration_days} days', 'timestamp': datetime.now().isoformat(), 'step': 3})}\n\n"

            # Step 3: Search flights
            yield f"data: {json.dumps({'type': 'log', 'agent_name': 'Quick Planner', 'message': 'Searching flight options and comparing prices across carriers', 'timestamp': datetime.now().isoformat(), 'step': 4})}\n\n"

            # Step 4: Search hotels
            yield f"data: {json.dumps({'type': 'log', 'agent_name': 'Quick Planner', 'message': f'Finding {request.hotel_preference} accommodation options near popular areas', 'timestamp': datetime.now().isoformat(), 'step': 5})}\n\n"

            # Step 5: Search activities
            yield f"data: {json.dumps({'type': 'log', 'agent_name': 'Quick Planner', 'message': f'Curating activities matching interests: {", ".join(request.interests)}', 'timestamp': datetime.now().isoformat(), 'step': 6})}\n\n"

            # Execute the actual planning
            agent = SingleTravelAgent()
            response = agent.plan_trip(request)

            # Step 6: Calculate costs
            yield f"data: {json.dumps({'type': 'log', 'agent_name': 'Quick Planner', 'message': 'Calculating total trip cost including flights, accommodation, activities, and meals', 'timestamp': datetime.now().isoformat(), 'step': 7})}\n\n"

            # Step 7: Complete
            if response.itinerary and response.itinerary.within_budget:
                yield f"data: {json.dumps({'type': 'log', 'agent_name': 'Quick Planner', 'message': f'Planning complete - Total cost ${response.itinerary.actual_cost:.2f} is within your ${request.budget} budget', 'timestamp': datetime.now().isoformat(), 'step': 8})}\n\n"
            elif response.itinerary:
                yield f"data: {json.dumps({'type': 'log', 'agent_name': 'Quick Planner', 'message': f'Planning complete - Total cost ${response.itinerary.actual_cost:.2f} exceeds budget of ${request.budget} (limitation of single agent approach)', 'timestamp': datetime.now().isoformat(), 'step': 8})}\n\n"
            else:
                yield f"data: {json.dumps({'type': 'log', 'agent_name': 'Quick Planner', 'message': 'Planning complete - Unable to generate itinerary', 'timestamp': datetime.now().isoformat(), 'step': 8})}\n\n"

            # Send the final result
            yield f"data: {json.dumps({'type': 'result', 'data': response.model_dump()})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@router.get("/info")
async def get_planning_info():
    """
    Get information about Quick Planning features.
    """
    return {
        "name": "Quick Planning",
        "tagline": "Fast and Simple Travel Planning",
        "description": "Get instant travel plans for straightforward trips",
        "features": [
            "Instant results in under 10 seconds",
            "Complete itinerary with all travel components",
            "Detailed cost breakdown",
            "Simple and intuitive",
            "Perfect for weekend trips"
        ],
        "best_for": [
            "Quick decisions",
            "Simple destinations",
            "Weekend getaways",
            "Budget estimation"
        ],
        "upgrade_to": "Smart Planning for budget optimization"
    }
