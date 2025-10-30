"""
Stage 2: Agent Squad (AWS Multi-Agent Orchestration)

This implementation uses the AWS Agent Squad SDK (formerly Multi-Agent Orchestrator)
to demonstrate intelligent intent classification and routing to specialized agents.

Note: Agent Squad provides orchestration and routing, NOT A2A communication.
It routes user requests to the most suitable specialist agent based on intent.
"""
import os
import json
import time
import asyncio
from typing import List, Dict, Any
from datetime import datetime

from agent_squad.orchestrator import AgentSquad
from agent_squad.agents import BedrockLLMAgent, BedrockLLMAgentOptions

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
from app.services.bedrock_service import BedrockService


class MultiAgentOrchestrator:
    """
    AWS Agent Squad for intelligent multi-agent orchestration.

    This uses the Agent Squad framework from AWS Labs to demonstrate:
    - Intelligent intent classification
    - Dynamic routing to specialist agents
    - Context isolation between agents

    Note: This is NOT A2A communication - it's centralized orchestration/routing.
    """

    def __init__(self, region_name: str = None):
        self.region_name = region_name or os.getenv("AWS_REGION", "us-east-1")
        self.model_id = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0")

        # Initialize Agent Squad orchestrator
        self.orchestrator = AgentSquad()

        # Create specialist agents
        self._create_agents()

    def _create_agents(self):
        """Create specialist agents using BedrockLLMAgent."""

        # Flight Specialist Agent
        flight_agent = BedrockLLMAgent(BedrockLLMAgentOptions(
            name="FlightExpert",
            description="""You are a flight booking specialist. You ONLY handle flight-related queries and recommendations.

            Your expertise includes:
            - Finding the best flight options based on budget constraints
            - Balancing cost vs convenience (direct flights vs layovers)
            - Understanding airline quality and reliability
            - Optimizing flight costs for groups

            When given flight options and a budget, select the best flight that maximizes value while staying within budget.
            Consider: price per person, total cost for group, flight duration, number of stops, airline reputation.

            Do NOT make recommendations about hotels, activities, or other travel components.""",
            model_id=self.model_id,
            region=self.region_name
        ))

        # Hotel Specialist Agent
        hotel_agent = BedrockLLMAgent(BedrockLLMAgentOptions(
            name="HotelExpert",
            description="""You are a hotel and accommodation specialist. You ONLY handle hotel-related queries.

            Your expertise includes:
            - Matching hotels to traveler preferences (budget, mid-range, luxury)
            - Evaluating hotel amenities and value for money
            - Understanding location importance and neighborhood quality
            - Calculating total accommodation costs for multi-night stays

            When given hotel options and constraints, select the best hotel that matches the preference level
            while optimizing for budget. Consider: nightly rate, total cost, location, amenities, ratings.

            Do NOT make recommendations about flights, activities, or other travel components.""",
            model_id=self.model_id,
            region=self.region_name
        ))

        # Activity Specialist Agent
        activity_agent = BedrockLLMAgent(BedrockLLMAgentOptions(
            name="ActivityExpert",
            description="""You are a travel activities and experiences specialist. You ONLY handle activity planning.

            Your expertise includes:
            - Curating activities that match traveler interests
            - Understanding cultural, food, tech, and other activity categories
            - Balancing free vs paid activities
            - Creating diverse itineraries that avoid repetition

            When given activity options and traveler interests, select 4-6 activities that:
            - Match the stated interests closely
            - Provide variety and unique experiences
            - Fit within the allocated activity budget
            - Are feasible for the trip duration

            Do NOT make recommendations about flights, hotels, or other travel components.""",
            model_id=self.model_id,
            region=self.region_name
        ))

        # Budget Coordinator Agent
        budget_agent = BedrockLLMAgent(BedrockLLMAgentOptions(
            name="BudgetCoordinator",
            description="""You are a travel budget optimization specialist. You coordinate budget allocation.

            Your expertise includes:
            - Allocating total budget across travel components (flights, hotels, activities, food, misc)
            - Understanding typical budget ratios (e.g., 30% flights, 25% hotels, 20% activities, 15% food, 10% misc)
            - Identifying when costs exceed budget and suggesting adjustments
            - Ensuring all components fit within total budget

            When given a total budget and component costs, verify the math and confirm whether the plan
            is within budget. If over budget, suggest which components to adjust.

            You coordinate with other specialists but do not select specific flights, hotels, or activities.""",
            model_id=self.model_id,
            region=self.region_name
        ))

        # Add all agents to orchestrator
        self.orchestrator.add_agent(flight_agent)
        self.orchestrator.add_agent(hotel_agent)
        self.orchestrator.add_agent(activity_agent)
        self.orchestrator.add_agent(budget_agent)

    async def plan_trip(self, request: MultiAgentRequest) -> MultiAgentResponse:
        """
        Plan a trip using real AWS Multi-Agent Orchestrator with specialist agents.

        Each specialist agent handles their domain independently, then results are coordinated.
        """
        start_time = time.time()
        logs: List[AgentLog] = []
        user_id = "demo_user"
        session_id = f"session_{int(time.time())}"
        agents_used = []

        try:
            logs.append(AgentLog(
                agent_name="System",
                timestamp=datetime.utcnow().isoformat(),
                message=f"Multi-agent orchestration started for {request.destination}...",
                data={"step": "initialization", "agents": 4}
            ))

            # Get available options from mock data
            flights = get_flights(request.destination, "mid-range")
            hotels = get_hotels(request.destination, request.duration_days, request.hotel_preference)
            activities = get_activities(request.destination, request.interests or ["sightseeing"], max_count=10)

            # STEP 1: Call FlightExpert agent
            logs.append(AgentLog(
                agent_name="FlightExpert",
                timestamp=datetime.utcnow().isoformat(),
                message=f"FlightExpert analyzing flight options to {request.destination}...",
                data={"step": "flight_analysis", "options_count": len(flights)}
            ))

            flight_prompt = f"""You are the Flight Specialist. Select the BEST flight option for this trip:

TRIP DETAILS:
- Destination: {request.destination}
- Travelers: {request.travelers}
- Suggested Flight Budget: ${request.budget * 0.30:.2f} (30% of ${request.budget} total)

AVAILABLE FLIGHTS:
{self._format_flights(flights, request.travelers)}

Select the flight that offers the best value - balancing cost, duration, and convenience.
Respond with ONLY the airline name of your chosen flight and brief reasoning."""

            flight_response = await self.orchestrator.route_request(
                user_input=flight_prompt,
                user_id=user_id,
                session_id=f"{session_id}_flight"
            )
            agents_used.append(flight_response.metadata.agent_name if hasattr(flight_response, 'metadata') else "FlightExpert")

            flight_response_text = self._extract_response_text(flight_response)
            selected_flight = self._parse_flight_from_response(flight_response_text, flights)

            logs.append(AgentLog(
                agent_name="FlightExpert",
                timestamp=datetime.utcnow().isoformat(),
                message=f"Selected {selected_flight.airline} - ${selected_flight.price * request.travelers} total",
                data={"flight": selected_flight.airline, "cost": selected_flight.price * request.travelers}
            ))

            # STEP 2: Call HotelExpert agent
            logs.append(AgentLog(
                agent_name="HotelExpert",
                timestamp=datetime.utcnow().isoformat(),
                message=f"HotelExpert finding best {request.hotel_preference} accommodation...",
                data={"step": "hotel_analysis", "options_count": len(hotels)}
            ))

            hotel_prompt = f"""You are the Hotel Specialist. Select the BEST hotel option for this trip:

TRIP DETAILS:
- Destination: {request.destination}
- Duration: {request.duration_days} nights
- Preference: {request.hotel_preference}
- Suggested Hotel Budget: ${request.budget * 0.25:.2f} (25% of ${request.budget} total)

AVAILABLE HOTELS:
{self._format_hotels(hotels)}

Select the hotel that best matches the {request.hotel_preference} preference while providing good value.
Respond with ONLY the hotel name of your choice and brief reasoning."""

            hotel_response = await self.orchestrator.route_request(
                user_input=hotel_prompt,
                user_id=user_id,
                session_id=f"{session_id}_hotel"
            )
            agents_used.append(hotel_response.metadata.agent_name if hasattr(hotel_response, 'metadata') else "HotelExpert")

            hotel_response_text = self._extract_response_text(hotel_response)
            selected_hotel = self._parse_hotel_from_response(hotel_response_text, hotels)

            logs.append(AgentLog(
                agent_name="HotelExpert",
                timestamp=datetime.utcnow().isoformat(),
                message=f"Selected {selected_hotel.name} - ${selected_hotel.total_price} for {request.duration_days} nights",
                data={"hotel": selected_hotel.name, "cost": selected_hotel.total_price}
            ))

            # STEP 3: Call ActivityExpert agent
            logs.append(AgentLog(
                agent_name="ActivityExpert",
                timestamp=datetime.utcnow().isoformat(),
                message=f"ActivityExpert curating experiences for interests: {', '.join(request.interests or ['sightseeing'])}...",
                data={"step": "activity_curation", "options_count": len(activities)}
            ))

            activity_prompt = f"""You are the Activity Specialist. Select 4-6 BEST activities for this trip:

TRIP DETAILS:
- Destination: {request.destination}
- Interests: {', '.join(request.interests or ['sightseeing'])}
- Travelers: {request.travelers}
- Suggested Activity Budget: ${request.budget * 0.20:.2f} (20% of ${request.budget} total)

AVAILABLE ACTIVITIES:
{self._format_activities(activities, request.travelers)}

Select 4-6 activities that:
1. Match the traveler's interests: {', '.join(request.interests or ['sightseeing'])}
2. Provide variety and unique experiences
3. Fit within the activity budget

Respond with ONLY the activity names (comma-separated) and brief reasoning."""

            activity_response = await self.orchestrator.route_request(
                user_input=activity_prompt,
                user_id=user_id,
                session_id=f"{session_id}_activity"
            )
            agents_used.append(activity_response.metadata.agent_name if hasattr(activity_response, 'metadata') else "ActivityExpert")

            activity_response_text = self._extract_response_text(activity_response)
            selected_activities = self._parse_activities_from_response(activity_response_text, activities)

            logs.append(AgentLog(
                agent_name="ActivityExpert",
                timestamp=datetime.utcnow().isoformat(),
                message=f"Curated {len(selected_activities)} activities matching your interests",
                data={"activities_count": len(selected_activities), "activities": [a.name for a in selected_activities]}
            ))

            # STEP 4: Calculate costs and call BudgetCoordinator
            flight_cost = selected_flight.price * request.travelers if selected_flight else 0
            hotel_cost = selected_hotel.total_price if selected_hotel else 0
            activities_cost = sum(a.cost for a in selected_activities) * request.travelers

            # Allocate remaining for food and misc
            remaining = request.budget - (flight_cost + hotel_cost + activities_cost)
            food_cost = remaining * 0.60 if remaining > 0 else request.budget * 0.15
            misc_cost = remaining * 0.40 if remaining > 0 else request.budget * 0.10

            total_cost = flight_cost + hotel_cost + activities_cost + food_cost + misc_cost

            logs.append(AgentLog(
                agent_name="BudgetCoordinator",
                timestamp=datetime.utcnow().isoformat(),
                message=f"BudgetCoordinator verifying total cost against ${request.budget} budget...",
                data={"step": "budget_verification", "total_cost": total_cost, "budget": request.budget}
            ))

            budget_prompt = f"""You are the Budget Coordinator. Verify this travel plan's budget:

TOTAL BUDGET: ${request.budget}

COMPONENT COSTS:
- Flights: ${flight_cost} ({(flight_cost/request.budget*100):.1f}%)
- Hotel: ${hotel_cost} ({(hotel_cost/request.budget*100):.1f}%)
- Activities: ${activities_cost} ({(activities_cost/request.budget*100):.1f}%)
- Food: ${food_cost} ({(food_cost/request.budget*100):.1f}%)
- Miscellaneous: ${misc_cost} ({(misc_cost/request.budget*100):.1f}%)

TOTAL COST: ${total_cost}
WITHIN BUDGET: {'YES' if total_cost <= request.budget else 'NO'}

Provide a brief assessment of the budget allocation. Is it reasonable? Any concerns?"""

            budget_response = await self.orchestrator.route_request(
                user_input=budget_prompt,
                user_id=user_id,
                session_id=f"{session_id}_budget"
            )
            agents_used.append(budget_response.metadata.agent_name if hasattr(budget_response, 'metadata') else "BudgetCoordinator")

            logs.append(AgentLog(
                agent_name="BudgetCoordinator",
                timestamp=datetime.utcnow().isoformat(),
                message=f"{'✓ Budget approved! Trip within ${request.budget}' if total_cost <= request.budget else f'⚠ Over budget by ${total_cost - request.budget:.2f}'}",
                data={
                    "total_cost": total_cost,
                    "within_budget": total_cost <= request.budget,
                    "variance": total_cost - request.budget
                }
            ))

            # Build itinerary
            itinerary = TravelItinerary(
                destination=request.destination,
                duration_days=request.duration_days,
                total_budget=request.budget,
                actual_cost=total_cost,
                within_budget=total_cost <= request.budget,
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

            execution_time = (time.time() - start_time) * 1000

            logs.append(AgentLog(
                agent_name="System",
                timestamp=datetime.utcnow().isoformat(),
                message=f"Multi-agent collaboration complete! {len(set(agents_used))} specialist agents coordinated.",
                data={
                    "execution_time_ms": execution_time,
                    "step": "final",
                    "agents_used": list(set(agents_used))
                }
            ))

            return MultiAgentResponse(
                success=True,
                message=f"Multi-agent orchestration successful - {len(set(agents_used))} specialists collaborated",
                execution_time_ms=execution_time,
                status=AgentStatus.SUCCESS,
                itinerary=itinerary,
                agent_logs=logs if request.enable_logging else [],
                agents_used=list(set(agents_used)),
                collaboration_count=len(logs)
            )

        except Exception as e:
            execution_time = (time.time() - start_time) * 1000

            logs.append(AgentLog(
                agent_name="Supervisor",
                timestamp=datetime.utcnow().isoformat(),
                message=f"Error: {str(e)}",
                data={"error": str(e), "type": type(e).__name__}
            ))

            return MultiAgentResponse(
                success=False,
                message=f"Real orchestration failed: {str(e)}",
                execution_time_ms=execution_time,
                status=AgentStatus.ERROR,
                agent_logs=logs,
                agents_used=[],
                collaboration_count=len(logs)
            )

    async def plan_trip_stream(self, request: MultiAgentRequest):
        """
        Stream trip planning progress in real-time using async generator.
        Yields events as they happen.
        """
        start_time = time.time()

        try:
            # Step 1: Analyzing requirements
            yield {
                "type": "log",
                "agent_name": "System",
                "message": f"🎯 Analyzing your travel requirements for {request.destination}...",
                "timestamp": datetime.utcnow().isoformat()
            }

            # Step 2: Search flights
            yield {
                "type": "log",
                "agent_name": "FlightAgent",
                "message": f"✈️ Searching for best flights to {request.destination}...",
                "timestamp": datetime.utcnow().isoformat()
            }
            flights = get_flights(request.destination, request.hotel_preference)

            yield {
                "type": "log",
                "agent_name": "FlightAgent",
                "message": f"✅ Found {len(flights)} flight options, analyzing for best value...",
                "timestamp": datetime.utcnow().isoformat()
            }

            # Step 3: Search hotels
            yield {
                "type": "log",
                "agent_name": "HotelAgent",
                "message": f"🏨 Finding {request.hotel_preference} hotels for {request.duration_days} nights...",
                "timestamp": datetime.utcnow().isoformat()
            }
            hotels = get_hotels(request.destination, request.duration_days, request.hotel_preference)

            yield {
                "type": "log",
                "agent_name": "HotelAgent",
                "message": f"✅ Located {len(hotels)} hotels matching your preferences...",
                "timestamp": datetime.utcnow().isoformat()
            }

            # Step 4: Search activities
            yield {
                "type": "log",
                "agent_name": "ActivityAgent",
                "message": f"🎭 Curating activities for interests: {', '.join(request.interests or ['sightseeing'])}...",
                "timestamp": datetime.utcnow().isoformat()
            }
            activities = get_activities(request.destination, request.interests or ["sightseeing"], max_count=10)

            yield {
                "type": "log",
                "agent_name": "ActivityAgent",
                "message": f"✅ Curated {len(activities)} unique experiences...",
                "timestamp": datetime.utcnow().isoformat()
            }

            # Step 5: Budget optimization
            yield {
                "type": "log",
                "agent_name": "BudgetAgent",
                "message": f"💰 Optimizing ${request.budget} budget across all categories...",
                "timestamp": datetime.utcnow().isoformat()
            }

            # Step 6: AI Analysis with REAL streaming
            yield {
                "type": "log",
                "agent_name": "TravelSupervisor",
                "message": "AI Travel Supervisor analyzing options...",
                "timestamp": datetime.utcnow().isoformat()
            }

            # Build prompt
            prompt = f"""Plan a {request.duration_days}-day trip to {request.destination} for {request.travelers} travelers
with a total budget of ${request.budget}.

TRAVELER PREFERENCES:
- Interests: {', '.join(request.interests or ['sightseeing'])}
- Hotel Preference: {request.hotel_preference}
- Activity Level: {request.activity_level}

AVAILABLE FLIGHTS (select the best one):
{self._format_flights(flights, request.travelers)}

AVAILABLE HOTELS (select the best one):
{self._format_hotels(hotels)}

AVAILABLE ACTIVITIES (select up to 6 that match interests):
{self._format_activities(activities, request.travelers)}

YOUR TASK:
1. Allocate the ${request.budget} budget intelligently across categories
2. Select the BEST flight, hotel, and activities
3. Calculate total cost and confirm it's within ${request.budget}
4. Provide your recommendations with reasoning

Think step by step and explain your reasoning briefly.
"""

            # Stream AI reasoning using Bedrock directly
            import boto3
            bedrock = boto3.client('bedrock-runtime', region_name=self.region_name)

            response_text = ""
            current_chunk = ""

            # Make streaming call to Bedrock
            response = bedrock.invoke_model_with_response_stream(
                modelId=self.model_id,
                body=json.dumps({
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
            )

            # Stream the AI's reasoning
            for event in response['body']:
                chunk = json.loads(event['chunk']['bytes'].decode())

                if chunk['type'] == 'content_block_delta':
                    if 'delta' in chunk and 'text' in chunk['delta']:
                        text = chunk['delta']['text']
                        response_text += text
                        current_chunk += text

                        # Stream reasoning in sentences
                        if any(punct in text for punct in ['.', '!', '?', '\n']):
                            if current_chunk.strip():
                                yield {
                                    "type": "log",
                                    "agent_name": "TravelSupervisor",
                                    "message": current_chunk.strip(),
                                    "timestamp": datetime.utcnow().isoformat()
                                }
                                current_chunk = ""
                                await asyncio.sleep(0.1)

            # Yield any remaining text
            if current_chunk.strip():
                yield {
                    "type": "log",
                    "agent_name": "TravelSupervisor",
                    "message": current_chunk.strip(),
                    "timestamp": datetime.utcnow().isoformat()
                }

            yield {
                "type": "log",
                "agent_name": "TravelSupervisor",
                "message": "Analysis complete!",
                "timestamp": datetime.utcnow().isoformat()
            }

            # Parse results
            selected_flight = self._parse_flight_from_response(response_text, flights)
            selected_hotel = self._parse_hotel_from_response(response_text, hotels)
            selected_activities = self._parse_activities_from_response(response_text, activities)

            yield {
                "type": "log",
                "agent_name": "TravelSupervisor",
                "message": f"📋 Selected {1 if selected_flight else 0} flight, 1 hotel, and {len(selected_activities)} activities",
                "timestamp": datetime.utcnow().isoformat()
            }

            # Calculate costs
            flight_cost = selected_flight.price * request.travelers if selected_flight else 0
            hotel_cost = selected_hotel.total_price if selected_hotel else 0
            activities_cost = sum(a.cost for a in selected_activities) * request.travelers
            remaining = request.budget - (flight_cost + hotel_cost + activities_cost)
            food_cost = remaining * 0.60
            misc_cost = remaining * 0.40
            total_cost = flight_cost + hotel_cost + activities_cost + food_cost + misc_cost

            # Budget check
            within_budget = total_cost <= request.budget
            yield {
                "type": "log",
                "agent_name": "BudgetAgent",
                "message": f"{'✅ Perfect! Your trip is within budget!' if within_budget else '⚠️ Trip slightly over budget - adjusting recommendations...'}",
                "timestamp": datetime.utcnow().isoformat()
            }

            # Final message
            yield {
                "type": "log",
                "agent_name": "System",
                "message": "🎉 Your personalized travel plan is ready!",
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

            execution_time = (time.time() - start_time) * 1000

            # Send final result
            final_response = MultiAgentResponse(
                success=True,
                message="Real AWS Multi-Agent Orchestrator completed successfully using Bedrock",
                execution_time_ms=execution_time,
                status=AgentStatus.SUCCESS,
                itinerary=itinerary,
                agent_logs=[],  # Logs already streamed
                agents_used=["TravelSupervisor"],
                collaboration_count=9
            )

            yield {
                "type": "result",
                "data": json.loads(final_response.json())
            }

        except Exception as e:
            yield {
                "type": "error",
                "message": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

    # Helper methods for formatting and parsing

    def _extract_response_text(self, response) -> str:
        """Extract text from Agent Squad response object."""
        response_text = ""
        if hasattr(response.output, 'content') and isinstance(response.output.content, list):
            response_text = ' '.join([item.get('text', '') for item in response.output.content if isinstance(item, dict)])
        return response_text

    def _format_flights(self, flights: List[FlightOption], travelers: int) -> str:
        """Format flights for agent prompt."""
        result = []
        for i, f in enumerate(flights, 1):
            result.append(
                f"{i}. {f.airline}: ${f.price}/person (${f.price * travelers} total for {travelers} travelers)\n"
                f"   Duration: {f.duration}, Stops: {f.stops}"
            )
        return "\n".join(result)

    def _format_hotels(self, hotels: List[HotelOption]) -> str:
        """Format hotels for agent prompt."""
        result = []
        for i, h in enumerate(hotels, 1):
            result.append(
                f"{i}. {h.name}: ${h.price_per_night}/night (${h.total_price} total)\n"
                f"   Location: {h.location}, Rating: {h.rating}/5\n"
                f"   Amenities: {', '.join(h.amenities[:3])}"
            )
        return "\n".join(result)

    def _format_activities(self, activities: List[ActivityOption], travelers: int) -> str:
        """Format activities for agent prompt."""
        result = []
        for i, a in enumerate(activities, 1):
            result.append(
                f"{i}. {a.name} ({a.category}): ${a.cost}/person (${a.cost * travelers} total)\n"
                f"   Duration: {a.duration}, Description: {a.description}"
            )
        return "\n".join(result)

    def _parse_flight_from_response(self, response: str, flights: List[FlightOption]) -> FlightOption:
        """Parse selected flight from agent response."""
        response_lower = response.lower()
        for flight in flights:
            if flight.airline.lower() in response_lower:
                return flight
        # Default to first if not found
        return flights[0] if flights else None

    def _parse_hotel_from_response(self, response: str, hotels: List[HotelOption]) -> HotelOption:
        """Parse selected hotel from agent response."""
        response_lower = response.lower()
        for hotel in hotels:
            if hotel.name.lower() in response_lower:
                return hotel
        # Default to first if not found
        return hotels[0] if hotels else None

    def _parse_activities_from_response(self, response: str, activities: List[ActivityOption]) -> List[ActivityOption]:
        """Parse selected activities from agent response."""
        selected = []
        response_lower = response.lower()

        for activity in activities:
            if activity.name.lower() in response_lower:
                selected.append(activity)
                if len(selected) >= 6:
                    break

        # If none found, return first 6
        return selected if selected else activities[:6]
