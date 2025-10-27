"""
AP2 (Agents Payments Protocol) API Router
Stage 4: Autonomous agent payments with full transparency
"""

import asyncio
import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.models.requests import MultiAgentRequest
from app.agents.ap2_orchestrator import AP2Orchestrator

router = APIRouter(prefix="/api/ap2", tags=["ap2"])


@router.post("/stream")
async def plan_trip_ap2_stream(request: MultiAgentRequest):
    """
    Stream real-time progress using AP2 (Agents Payments Protocol).

    Demonstrates the complete AP2 flow:
    1. Intent Mandate - Agent declares purchase intent
    2. Cart Mandate - Itemized breakdown with costs
    3. Payment Mandate - User authorization with cryptographic signature
    4. Transaction Execution - Payment processing with audit trail
    5. Receipt Generation - Blockchain-verified receipt

    This showcases autonomous agent payments with:
    - Full transparency (every step visible)
    - User control (explicit authorization required)
    - Verifiable intent (cryptographic signatures)
    - Audit trail (blockchain verification)
    """

    async def event_generator():
        try:
            orchestrator = AP2Orchestrator()

            async for event in orchestrator.plan_trip_with_ap2_stream(request):
                yield f"data: {json.dumps(event)}\n\n"
                await asyncio.sleep(0.01)

        except Exception as e:
            error_event = {
                "type": "error",
                "message": str(e),
                "timestamp": "error"
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


@router.get("/health")
async def health_check():
    """Health check endpoint for AP2 service."""
    return {
        "status": "healthy",
        "service": "AP2 Orchestrator",
        "version": "1.0.0"
    }
