"""Response models for all API endpoints."""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum


class AgentStatus(str, Enum):
    """Agent execution status."""
    SUCCESS = "success"
    FAILURE = "failure"
    PARTIAL = "partial"
    ERROR = "error"


class FlightOption(BaseModel):
    """Flight option details."""
    airline: str
    departure_time: str
    arrival_time: str
    duration: str
    price: float
    stops: int = 0


class HotelOption(BaseModel):
    """Hotel option details."""
    name: str
    location: str
    price_per_night: float
    total_price: float
    rating: float
    amenities: List[str]


class ActivityOption(BaseModel):
    """Activity/attraction details."""
    name: str
    description: str
    cost: float
    duration: str
    category: str


class TravelItinerary(BaseModel):
    """Complete travel itinerary."""
    destination: str
    duration_days: int
    total_budget: float
    actual_cost: float
    within_budget: bool

    # Components
    flights: Optional[FlightOption] = None
    hotel: Optional[HotelOption] = None
    activities: List[ActivityOption] = []
    daily_plan: Optional[Dict[str, List[str]]] = None

    # Breakdown
    cost_breakdown: Dict[str, float] = Field(
        default_factory=lambda: {
            "flights": 0.0,
            "accommodation": 0.0,
            "activities": 0.0,
            "food": 0.0,
            "misc": 0.0
        }
    )


class AgentLog(BaseModel):
    """Individual agent execution log."""
    agent_name: str
    timestamp: str
    message: str
    data: Optional[Dict[str, Any]] = None


class WorkflowStep(BaseModel):
    """Strands workflow step."""
    step_number: int
    step_name: str
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class AP2Payment(BaseModel):
    """AP2 payment transaction."""
    service_name: str
    cost: float
    timestamp: str
    transaction_id: str
    status: str = "completed"


class BaseResponse(BaseModel):
    """Base response model."""
    success: bool
    message: str
    execution_time_ms: float
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class SingleAgentResponse(BaseResponse):
    """Response for single agent endpoint (Stage 1)."""
    status: AgentStatus
    itinerary: Optional[TravelItinerary] = None
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


class MultiAgentResponse(BaseResponse):
    """Response for multi-agent endpoint (Stage 2)."""
    status: AgentStatus
    itinerary: Optional[TravelItinerary] = None

    # Multi-agent specific
    agent_logs: List[AgentLog] = Field(default_factory=list)
    agents_used: List[str] = Field(default_factory=list)
    collaboration_count: int = 0


class StrandsResponse(BaseResponse):
    """Response for strands workflow endpoint (Stage 3)."""
    status: AgentStatus
    itinerary: Optional[TravelItinerary] = None

    # Workflow specific
    session_id: str
    workflow_steps: List[WorkflowStep] = Field(default_factory=list)
    iterations_used: int = 0
    validation_passed: bool = False
    can_resume: bool = True


class GuardrailsResponse(BaseResponse):
    """Response for guardrails-protected endpoint (Stage 4)."""
    status: AgentStatus
    itinerary: Optional[TravelItinerary] = None

    # Guardrails specific
    guardrails_triggered: bool = False
    blocked_content: List[str] = Field(default_factory=list)
    pii_detected: bool = False
    security_score: float = 1.0


class AP2Response(BaseResponse):
    """Response for AP2-enabled endpoint (Stage 5)."""
    status: AgentStatus
    itinerary: Optional[TravelItinerary] = None

    # AP2 specific
    payments: List[AP2Payment] = Field(default_factory=list)
    total_api_cost: float = 0.0
    wallet_balance_remaining: float = 0.0
    cost_savings_vs_traditional: float = 0.0
    apis_used: List[str] = Field(default_factory=list)


class ErrorResponse(BaseResponse):
    """Error response model."""
    success: bool = False
    error_code: str
    error_details: Optional[Dict[str, Any]] = None
