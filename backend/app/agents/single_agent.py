"""
Stage 1: Single Agent Implementation (Intentionally Limited)

This agent demonstrates the FAILURES of a single monolithic agent:
- Overwhelmed by complex constraints
- Poor budget management
- Inconsistent recommendations
- No specialization
"""
import json
import boto3
import os
from typing import Dict, Any
from app.models.requests import SingleAgentRequest
from app.models.responses import (
    SingleAgentResponse,
    TravelItinerary,
    FlightOption,
    HotelOption,
    ActivityOption,
    AgentStatus
)
from app.services.hybrid_data import (
    get_flights,
    get_hotels,
    get_activities,
    calculate_daily_food_budget,
    calculate_misc_costs
)


class SingleTravelAgent:
    """
    A single monolithic agent that tries to do everything.

    Intentional Limitations (for demo):
    1. Doesn't properly validate budget
    2. Recommendations can exceed budget
    3. No iterative refinement
    4. Generic, not personalized
    5. Prone to making conflicting choices
    """

    def __init__(self, region_name: str = None):
        # Read from environment variables
        self.region_name = region_name or os.getenv("AWS_REGION", "us-east-1")
        self.model_id = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20241022-v2:0")

        self.bedrock = boto3.client("bedrock-runtime", region_name=self.region_name)

    def plan_trip(self, request: SingleAgentRequest) -> SingleAgentResponse:
        """
        Plan a trip using a single agent (will likely fail or produce suboptimal results).
        """
        import time
        start_time = time.time()

        try:
            # Build a single massive prompt (anti-pattern)
            prompt = self._build_monolithic_prompt(request)

            # Single LLM call to do EVERYTHING
            response = self._call_bedrock(prompt)

            # Try to extract structured data (often fails)
            itinerary = self._parse_agent_response(response, request)

            # Check if we exceeded budget (we often do!)
            exceeded_budget = itinerary.actual_cost > itinerary.total_budget
            warnings = []
            errors = []

            if exceeded_budget:
                errors.append(
                    f"Budget exceeded! Planned ${itinerary.actual_cost:.2f} "
                    f"but budget was ${itinerary.total_budget:.2f}"
                )

            # Check for other common failures
            if not itinerary.flights:
                errors.append("Failed to find suitable flights")

            if not itinerary.hotel:
                errors.append("Failed to find suitable accommodation")

            if len(itinerary.activities) == 0:
                warnings.append("No activities planned - generic itinerary")

            # Determine status
            if errors:
                status = AgentStatus.FAILURE
            elif warnings:
                status = AgentStatus.PARTIAL
            else:
                status = AgentStatus.SUCCESS

            execution_time = (time.time() - start_time) * 1000

            return SingleAgentResponse(
                success=True,
                message="Single agent completed trip planning (with limitations)",
                execution_time_ms=execution_time,
                status=status,
                itinerary=itinerary,
                errors=errors,
                warnings=warnings
            )

        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            return SingleAgentResponse(
                success=False,
                message=f"Single agent failed: {str(e)}",
                execution_time_ms=execution_time,
                status=AgentStatus.ERROR,
                errors=[str(e)]
            )

    def _build_monolithic_prompt(self, request: SingleAgentRequest) -> str:
        """Build a single massive prompt (anti-pattern - too much for one agent)."""
        return f"""You are a travel planning agent. Plan a complete trip with ALL of the following:

REQUIREMENTS:
- Destination: {request.destination}
- Duration: {request.duration_days} days
- Budget: ${request.budget} USD (TOTAL for everything)
- Travelers: {request.travelers}
- Interests: {', '.join(request.interests or ['general sightseeing'])}
- Hotel preference: {request.hotel_preference}

YOU MUST PROVIDE:
1. Flight recommendations (with prices)
2. Hotel recommendations (with nightly rates)
3. Daily activity itinerary
4. Food budget allocation
5. Miscellaneous costs (transport, etc.)
6. ENSURE TOTAL COST STAYS WITHIN BUDGET

Respond with a JSON object containing:
{{
    "flights_needed": true/false,
    "recommended_flight_cost": <amount>,
    "hotel_recommendation": "<hotel type>",
    "activities": ["activity1", "activity2"],
    "estimated_food_cost": <amount>,
    "misc_costs": <amount>
}}

Think carefully about budget allocation. This is complex!
"""

    def _call_bedrock(self, prompt: str) -> str:
        """Make a single call to Bedrock."""
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 2000,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7
        })

        response = self.bedrock.invoke_model(
            modelId=self.model_id,
            body=body
        )

        response_body = json.loads(response['body'].read())
        return response_body['content'][0]['text']

    def _parse_agent_response(
        self,
        agent_response: str,
        request: SingleAgentRequest
    ) -> TravelItinerary:
        """
        Parse the agent's response and build an itinerary.

        Note: This is intentionally simplistic and doesn't do proper
        budget optimization (demonstrating single agent limitations).
        """
        # For demo purposes, just build an itinerary from mock data
        # In reality, we'd parse the LLM response, but it's often inconsistent

        # Grab flights (often picks expensive ones)
        flights = get_flights(request.destination, "luxury")  # Anti-pattern: ignores budget
        selected_flight = flights[0] if flights else None

        # Grab hotels (may not match budget)
        hotels = get_hotels(
            request.destination,
            request.duration_days,
            request.hotel_preference
        )
        selected_hotel = hotels[-1] if hotels else None  # Pick most expensive (bug!)

        # Grab activities (too many, no budget check)
        activities = get_activities(
            request.destination,
            request.interests or ["sightseeing"],
            max_count=10  # Too many! Should limit based on budget
        )

        # Calculate costs (doesn't validate against budget!)
        flight_cost = selected_flight.price * request.travelers if selected_flight else 0
        hotel_cost = selected_hotel.total_price if selected_hotel else 0
        activities_cost = sum(a.cost for a in activities) * request.travelers
        food_cost = calculate_daily_food_budget(request.duration_days, request.hotel_preference)
        misc_cost = calculate_misc_costs(request.duration_days)

        total_cost = flight_cost + hotel_cost + activities_cost + food_cost + misc_cost

        return TravelItinerary(
            destination=request.destination,
            duration_days=request.duration_days,
            total_budget=request.budget,
            actual_cost=total_cost,
            within_budget=total_cost <= request.budget,
            flights=selected_flight,
            hotel=selected_hotel,
            activities=activities[:5],  # Limit for display
            cost_breakdown={
                "flights": flight_cost,
                "accommodation": hotel_cost,
                "activities": activities_cost,
                "food": food_cost,
                "misc": misc_cost
            }
        )
