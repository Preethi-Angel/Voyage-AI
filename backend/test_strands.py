"""
Test script for Stage 3 Strands orchestration
"""
import asyncio
import json
from app.agents.strands_orchestrator import StrandsOrchestrator
from app.models.requests import MultiAgentRequest


async def test_strands_orchestration():
    """Test the Strands orchestrator with a sample trip request."""
    print("=" * 80)
    print("TESTING STAGE 3: AWS STRANDS INTELLIGENT ORCHESTRATOR")
    print("=" * 80)

    # Create sample request
    request = MultiAgentRequest(
        destination="Tokyo",
        duration_days=7,
        travelers=2,
        budget=6000,
        hotel_preference="mid-range",
        interests=["culture", "food", "technology"],
        activity_level="moderate"
    )

    print(f"\n📋 Request Details:")
    print(f"   Destination: {request.destination}")
    print(f"   Duration: {request.duration_days} days")
    print(f"   Travelers: {request.travelers}")
    print(f"   Budget: ${request.budget}")
    print(f"   Interests: {', '.join(request.interests)}")
    print(f"\n{'=' * 80}\n")

    # Create orchestrator
    orchestrator = StrandsOrchestrator()

    # Stream the planning process
    event_count = 0
    log_count = 0

    try:
        async for event in orchestrator.plan_trip_stream(request):
            event_count += 1

            if event.get("type") == "log":
                log_count += 1
                agent_name = event.get("agent_name", "Unknown")
                message = event.get("message", "")
                print(f"[{log_count}] {agent_name}: {message}")

                # If there's additional data, print it
                if "data" in event:
                    print(f"    └─ Data: {json.dumps(event['data'], indent=6)}")

            elif event.get("type") == "result":
                print(f"\n{'=' * 80}")
                print("✅ FINAL RESULT RECEIVED")
                print(f"{'=' * 80}\n")
                result = event.get("data", {})
                print(json.dumps(result, indent=2))

            elif event.get("type") == "error":
                print(f"\n❌ ERROR: {event.get('message')}")

    except Exception as e:
        print(f"\n❌ Exception during orchestration: {str(e)}")
        import traceback
        traceback.print_exc()

    print(f"\n{'=' * 80}")
    print(f"Total events received: {event_count}")
    print(f"Total log messages: {log_count}")
    print(f"{'=' * 80}\n")


if __name__ == "__main__":
    print("\n🚀 Starting Strands Orchestrator Test...\n")
    asyncio.run(test_strands_orchestration())
    print("\n✅ Test complete!\n")
