"""Data models for the travel agent demo."""
from .requests import (
    TravelRequest,
    SingleAgentRequest,
    MultiAgentRequest,
    StrandsRequest,
    GuardrailsRequest,
    AP2Request,
)
from .responses import (
    AgentStatus,
    FlightOption,
    HotelOption,
    ActivityOption,
    TravelItinerary,
    AgentLog,
    WorkflowStep,
    AP2Payment,
    BaseResponse,
    SingleAgentResponse,
    MultiAgentResponse,
    StrandsResponse,
    GuardrailsResponse,
    AP2Response,
    ErrorResponse,
)

__all__ = [
    # Requests
    "TravelRequest",
    "SingleAgentRequest",
    "MultiAgentRequest",
    "StrandsRequest",
    "GuardrailsRequest",
    "AP2Request",
    # Responses
    "AgentStatus",
    "FlightOption",
    "HotelOption",
    "ActivityOption",
    "TravelItinerary",
    "AgentLog",
    "WorkflowStep",
    "AP2Payment",
    "BaseResponse",
    "SingleAgentResponse",
    "MultiAgentResponse",
    "StrandsResponse",
    "GuardrailsResponse",
    "AP2Response",
    "ErrorResponse",
]
