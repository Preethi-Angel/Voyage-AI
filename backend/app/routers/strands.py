"""
Stage 3: AWS Strands Intelligent Orchestrator Router

SSE streaming endpoint for Strands-based orchestration.
"""
import json
import asyncio
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.models.requests import MultiAgentRequest
from app.agents.strands_orchestrator import StrandsOrchestrator

router = APIRouter(prefix="/api/strands", tags=["strands"])


@router.post("/stream")
async def plan_trip_strands_stream(request: MultiAgentRequest):
    """
    Stream real-time progress using AWS Strands intelligent orchestration.

    Features:
    - Model-driven orchestration
    - Dynamic agent spawning based on complexity
    - Swarm pattern for parallel execution
    - Faster completion with autonomous collaboration
    """
    async def event_generator():
        try:
            orchestrator = StrandsOrchestrator()
            async for event in orchestrator.plan_trip_stream(request):
                yield f"data: {json.dumps(event)}\n\n"
                await asyncio.sleep(0.01)  # Small delay for smooth streaming
        except Exception as e:
            error_event = {
                "type": "error",
                "message": str(e),
                "agent_name": "System"
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
