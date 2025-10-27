"""Request models for all API endpoints."""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date


class TravelRequest(BaseModel):
    """Base travel planning request."""
    destination: str = Field(..., description="Travel destination (e.g., 'Tokyo, Japan')")
    duration_days: int = Field(..., ge=1, le=30, description="Trip duration in days")
    budget: float = Field(..., gt=0, description="Total budget in USD")
    travelers: int = Field(default=1, ge=1, le=10, description="Number of travelers")
    departure_date: Optional[str] = Field(None, description="Preferred departure date (YYYY-MM-DD)")

    # Preferences
    interests: Optional[List[str]] = Field(
        default=["sightseeing"],
        description="Travel interests (e.g., 'food', 'tech', 'temples', 'nature')"
    )
    dietary_restrictions: Optional[List[str]] = Field(
        default=None,
        description="Dietary restrictions (e.g., 'vegetarian', 'halal', 'gluten-free')"
    )

    # Advanced options
    hotel_preference: Optional[str] = Field(
        default="mid-range",
        description="Hotel category: 'budget', 'mid-range', 'luxury'"
    )
    activity_level: Optional[str] = Field(
        default="moderate",
        description="Activity level: 'relaxed', 'moderate', 'active'"
    )


class SingleAgentRequest(TravelRequest):
    """Request for single agent endpoint (Stage 1)."""
    pass


class MultiAgentRequest(TravelRequest):
    """Request for multi-agent endpoint (Stage 2)."""
    enable_logging: bool = Field(
        default=True,
        description="Enable agent conversation logging for demo"
    )


class StrandsRequest(TravelRequest):
    """Request for strands workflow endpoint (Stage 3)."""
    session_id: Optional[str] = Field(
        None,
        description="Session ID for resuming workflows"
    )
    max_iterations: int = Field(
        default=3,
        ge=1,
        le=5,
        description="Maximum budget refinement iterations"
    )


class GuardrailsRequest(TravelRequest):
    """Request for guardrails-protected endpoint (Stage 4)."""
    enable_guardrails: bool = Field(
        default=True,
        description="Enable Bedrock Guardrails protection"
    )


class AP2Request(TravelRequest):
    """Request for AP2-enabled endpoint (Stage 5)."""
    ap2_wallet_address: Optional[str] = Field(
        None,
        description="Mock wallet address for AP2 payments"
    )
    max_api_cost: float = Field(
        default=1.0,
        description="Maximum allowed cost for API calls in USD"
    )

    # Which APIs to enable (for demo control)
    enable_flight_api: bool = Field(default=True)
    enable_hotel_api: bool = Field(default=True)
    enable_activity_api: bool = Field(default=True)
    enable_weather_api: bool = Field(default=True)
