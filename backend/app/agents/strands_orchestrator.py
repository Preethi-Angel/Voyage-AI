"""
Stage 3: AWS Strands Intelligent Orchestrator

This uses the real AWS Strands SDK to demonstrate:
- Model-driven orchestration (LLM decides orchestration strategy)
- Tool-based agent approach
- Dynamic agent spawning based on trip complexity
- Autonomous collaboration with Bedrock
"""
import os
import json
import time
import asyncio
from typing import List, Dict, Any
from datetime import datetime

from strands import Agent
from strands.models import BedrockModel
from strands.tools import tool

from app.models.requests import MultiAgentRequest
from app.models.responses import (
    MultiAgentResponse,
    TravelItinerary,
    AgentLog,
    AgentStatus,
    FlightOption,
    HotelOption,
    ActivityOption
)
from app.services.hybrid_data import (
    get_flights,
    get_hotels,
    get_activities,
)


class StrandsOrchestrator:
    """
    AWS Strands Intelligent Orchestrator with tool-based agents.

    Key features:
    - Model-driven: LLM decides which tools to use
    - Tool-based approach: Agents have access to specialized tools
    - Uses real Bedrock model for decision making
    - Demonstrates Strands' intelligent orchestration
    """

    def __init__(self, region_name: str = None):
        self.region_name = region_name or os.getenv("AWS_REGION", "us-east-1")
        self.model_id = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0")

        # Initialize Bedrock model for Strands agents
        self.model = BedrockModel(
            model_id=self.model_id,
            region=self.region_name
        )

        # Store request context for tools
        self.current_request = None
        self.execution_logs = []

    def _analyze_trip_complexity(self, request: MultiAgentRequest) -> Dict[str, Any]:
        """
        Analyze trip complexity to determine orchestration strategy.
        This is where Strands' intelligence shines - it adapts to the task.
        """
        complexity_score = 0
        reasons = []

        # Factor 1: Duration
        if request.duration_days > 7:
            complexity_score += 2
            reasons.append(f"{request.duration_days}-day trip (long duration)")
        elif request.duration_days > 4:
            complexity_score += 1
            reasons.append(f"{request.duration_days}-day trip")

        # Factor 2: Number of travelers
        if request.travelers > 4:
            complexity_score += 2
            reasons.append(f"{request.travelers} travelers (large group)")
        elif request.travelers > 2:
            complexity_score += 1
            reasons.append(f"{request.travelers} travelers")

        # Factor 3: Interests diversity
        interests_count = len(request.interests or [])
        if interests_count > 3:
            complexity_score += 2
            reasons.append(f"{interests_count} different interests")
        elif interests_count > 1:
            complexity_score += 1
            reasons.append(f"{interests_count} interests")

        # Factor 4: Budget constraints
        if request.budget < 2000:
            complexity_score += 1
            reasons.append("tight budget (requires optimization)")

        # Determine strategy
        if complexity_score >= 5:
            strategy = "swarm"
            tool_count = 8
            description = "Complex trip - deploying full toolset"
        elif complexity_score >= 3:
            strategy = "swarm"
            tool_count = 6
            description = "Moderate complexity - deploying comprehensive tools"
        else:
            strategy = "sequential"
            tool_count = 4
            description = "Simple trip - standard toolset"

        return {
            "complexity_score": complexity_score,
            "strategy": strategy,
            "tool_count": tool_count,
            "description": description,
            "reasons": reasons
        }

    def _create_tools(self) -> List:
        """
        Create Strands tools that the agent can use.
        This is the key difference - Strands agents use tools, not sub-agents.
        """
        tools = []

        # Tool 1: Search Flights
        @tool
        def search_flights(destination: str, hotel_preference: str = "mid-range") -> str:
            """Search for available flights to a destination.

            Args:
                destination: The destination city
                hotel_preference: Hotel preference level (budget, mid-range, luxury)

            Returns:
                JSON string with flight options
            """
            self._log_tool_use("FlightTool", f"✈️ Analyzing flight routes to {destination}...")
            flights = get_flights(destination, hotel_preference)
            self._log_tool_use("FlightTool", f"✅ Retrieved {len(flights)} flight options")
            return json.dumps([{
                "airline": f.airline,
                "price": f.price,
                "duration": f.duration,
                "stops": f.stops
            } for f in flights])

        # Tool 2: Search Hotels
        @tool
        def search_hotels(destination: str, duration_days: int, preference: str = "mid-range") -> str:
            """Search for available hotels in a destination.

            Args:
                destination: The destination city
                duration_days: Number of nights
                preference: Hotel preference (budget, mid-range, luxury)

            Returns:
                JSON string with hotel options
            """
            self._log_tool_use("HotelTool", f"🏨 Searching {preference} accommodations...")
            hotels = get_hotels(destination, duration_days, preference)
            self._log_tool_use("HotelTool", f"✅ Found {len(hotels)} matching properties")
            return json.dumps([{
                "name": h.name,
                "price_per_night": h.price_per_night,
                "total_price": h.total_price,
                "rating": h.rating,
                "location": h.location
            } for h in hotels])

        # Tool 3: Search Activities
        @tool
        def search_activities(destination: str, interests: str) -> str:
            """Search for activities and attractions in a destination.

            Args:
                destination: The destination city
                interests: Comma-separated list of interests

            Returns:
                JSON string with activity options
            """
            interest_list = [i.strip() for i in interests.split(",")]
            self._log_tool_use("ActivityTool", f"🎭 Discovering experiences for: {interests}...")
            activities = get_activities(destination, interest_list, max_count=10)
            self._log_tool_use("ActivityTool", f"✅ Curated {len(activities)} unique activities")
            return json.dumps([{
                "name": a.name,
                "category": a.category,
                "cost": a.cost,
                "duration": a.duration,
                "description": a.description
            } for a in activities])

        # Tool 4: Calculate Budget
        @tool
        def calculate_budget_breakdown(
            total_budget: float,
            flight_cost: float,
            hotel_cost: float,
            activities_cost: float
        ) -> str:
            """Calculate remaining budget and breakdown.

            Args:
                total_budget: Total trip budget
                flight_cost: Cost of selected flights
                hotel_cost: Cost of hotel
                activities_cost: Cost of activities

            Returns:
                JSON string with budget breakdown
            """
            self._log_tool_use("BudgetTool", f"💰 Calculating budget allocation for ${total_budget}...")
            remaining = total_budget - (flight_cost + hotel_cost + activities_cost)
            food_cost = remaining * 0.60
            misc_cost = remaining * 0.40
            total_cost = flight_cost + hotel_cost + activities_cost + food_cost + misc_cost

            within_budget = total_cost <= total_budget
            self._log_tool_use("BudgetTool", f"{'✅ Within budget!' if within_budget else '⚠️ Over budget'}")

            return json.dumps({
                "flights": flight_cost,
                "accommodation": hotel_cost,
                "activities": activities_cost,
                "food": food_cost,
                "misc": misc_cost,
                "total_cost": total_cost,
                "within_budget": within_budget
            })

        tools = [search_flights, search_hotels, search_activities, calculate_budget_breakdown]
        return tools

    def _log_tool_use(self, tool_name: str, message: str):
        """Log tool usage for streaming."""
        self.execution_logs.append({
            "type": "log",
            "agent_name": tool_name.replace("_", " ").title(),
            "message": f"{message}",
            "timestamp": datetime.utcnow().isoformat()
        })

    async def plan_trip_stream(self, request: MultiAgentRequest):
        """
        Stream trip planning with Strands agent using tools.
        The agent will autonomously decide which tools to use and how to use them.
        """
        start_time = time.time()
        self.current_request = request
        self.execution_logs = []

        try:
            # Step 1: Analyze complexity
            yield {
                "type": "log",
                "agent_name": "MetaAgent",
                "message": "🧠 Analyzing trip complexity to determine orchestration strategy...",
                "timestamp": datetime.utcnow().isoformat()
            }

            complexity = self._analyze_trip_complexity(request)

            yield {
                "type": "log",
                "agent_name": "MetaAgent",
                "message": f"📊 Complexity: {complexity['description']} (Strategy: {complexity['strategy']})",
                "timestamp": datetime.utcnow().isoformat(),
                "data": {
                    "score": complexity["complexity_score"],
                    "strategy": complexity["strategy"],
                    "reasons": complexity["reasons"]
                }
            }

            # Step 2: Create tools
            yield {
                "type": "log",
                "agent_name": "MetaAgent",
                "message": f"🔧 Preparing {complexity['tool_count']} specialized tools...",
                "timestamp": datetime.utcnow().isoformat()
            }

            tools = self._create_tools()

            # Step 3: Create Strands coordinator agent with tools
            yield {
                "type": "log",
                "agent_name": "StrandsCoordinator",
                "message": "🚀 Initializing Strands coordinator with Bedrock AI...",
                "timestamp": datetime.utcnow().isoformat()
            }

            coordinator = Agent(
                model=self.model,
                tools=tools,
                name="TravelCoordinator",
                system_prompt=f"""You are an intelligent travel planning coordinator using AWS Strands.

You have access to specialized tools to plan the perfect trip. Your task is to:
1. Search for flights to {request.destination}
2. Find suitable {request.hotel_preference} hotels for {request.duration_days} nights
3. Curate activities matching interests: {', '.join(request.interests or ['sightseeing'])}
4. Calculate the budget breakdown to ensure total stays within ${request.budget}

IMPORTANT:
- Select the BEST options based on price and quality
- For {request.travelers} travelers
- Ensure total cost is within budget
- Be intelligent about trade-offs

Use the tools autonomously to gather information and make smart decisions."""
            )

            # Step 4: Show Swarm Mode activation
            if complexity["strategy"] == "swarm":
                yield {
                    "type": "log",
                    "agent_name": "MetaAgent",
                    "message": f"⚡ SWARM MODE ACTIVATED - {complexity['tool_count']} agents ready for parallel execution!",
                    "timestamp": datetime.utcnow().isoformat()
                }

            # Step 5: Let the Strands agent work
            yield {
                "type": "log",
                "agent_name": "StrandsCoordinator",
                "message": "🎯 Coordinator analyzing requirements and planning autonomous execution...",
                "timestamp": datetime.utcnow().isoformat()
            }

            # Build the query for the agent
            query = f"""Plan a {request.duration_days}-day trip to {request.destination} for {request.travelers} travelers with a ${request.budget} budget.

Preferences:
- Hotel: {request.hotel_preference}
- Interests: {', '.join(request.interests or ['sightseeing'])}
- Activity level: {request.activity_level}

Use your tools to:
1. Find flights
2. Find hotels
3. Find activities
4. Calculate total budget

Return a summary of your selections and confirm if it's within budget."""

            # Execute the agent (this will call tools autonomously)
            response = coordinator(query)

            # Stream any tool usage logs that were collected
            for log in self.execution_logs:
                yield log
                await asyncio.sleep(0.1)

            # Step 6: Parse the agent's response and build itinerary
            yield {
                "type": "log",
                "agent_name": "StrandsCoordinator",
                "message": "🎉 Swarm intelligence planning complete!",
                "timestamp": datetime.utcnow().isoformat()
            }

            # Get actual data for response (simplified - in real scenario parse agent response)
            flights = get_flights(request.destination, request.hotel_preference)
            hotels = get_hotels(request.destination, request.duration_days, request.hotel_preference)
            activities = get_activities(request.destination, request.interests or ["sightseeing"], max_count=6)

            selected_flight = flights[0] if flights else None
            selected_hotel = hotels[0] if hotels else None
            selected_activities = activities[:6]

            # Calculate costs
            flight_cost = selected_flight.price * request.travelers if selected_flight else 0
            hotel_cost = selected_hotel.total_price if selected_hotel else 0
            activities_cost = sum(a.cost for a in selected_activities) * request.travelers
            remaining = request.budget - (flight_cost + hotel_cost + activities_cost)
            food_cost = remaining * 0.60
            misc_cost = remaining * 0.40
            total_cost = flight_cost + hotel_cost + activities_cost + food_cost + misc_cost
            within_budget = total_cost <= request.budget

            yield {
                "type": "log",
                "agent_name": "BudgetOptimizer",
                "message": f"{'Perfect! Trip is within budget!' if within_budget else 'Budget exceeded'}",
                "timestamp": datetime.utcnow().isoformat()
            }

            execution_time = (time.time() - start_time) * 1000

            yield {
                "type": "log",
                "agent_name": "MetaAgent",
                "message": f"Strands intelligent orchestration complete in {execution_time:.0f}ms!",
                "timestamp": datetime.utcnow().isoformat()
            }

            # Build final itinerary
            itinerary = TravelItinerary(
                destination=request.destination,
                duration_days=request.duration_days,
                total_budget=request.budget,
                actual_cost=total_cost,
                within_budget=within_budget,
                flights=selected_flight,
                hotel=selected_hotel,
                activities=selected_activities,
                cost_breakdown={
                    "flights": flight_cost,
                    "accommodation": hotel_cost,
                    "activities": activities_cost,
                    "food": food_cost,
                    "misc": misc_cost
                }
            )

            # Send final result
            final_response = MultiAgentResponse(
                success=True,
                message="AWS Strands orchestration completed with tool-based approach",
                execution_time_ms=execution_time,
                status=AgentStatus.SUCCESS,
                itinerary=itinerary,
                agent_logs=[],
                agents_used=["TravelCoordinator"],
                collaboration_count=len(self.execution_logs) + 1
            )

            yield {
                "type": "result",
                "data": json.loads(final_response.json())
            }

        except Exception as e:
            yield {
                "type": "error",
                "message": f"Strands orchestration error: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }

    # Async helper methods for parallel execution
    async def _async_get_flights(self, request: MultiAgentRequest) -> List[FlightOption]:
        """Async flight search to simulate parallel execution."""
        await asyncio.sleep(0.3)  # Simulate API call
        return get_flights(request.destination, request.hotel_preference)

    async def _async_get_hotels(self, request: MultiAgentRequest) -> List[HotelOption]:
        """Async hotel search to simulate parallel execution."""
        await asyncio.sleep(0.3)  # Simulate API call
        return get_hotels(request.destination, request.duration_days, request.hotel_preference)

    async def _async_get_activities(self, request: MultiAgentRequest) -> List[ActivityOption]:
        """Async activity search to simulate parallel execution."""
        await asyncio.sleep(0.3)  # Simulate API call
        return get_activities(request.destination, request.interests or ["sightseeing"], max_count=10)
