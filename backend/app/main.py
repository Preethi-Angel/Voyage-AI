"""
Voyago API - Intelligent Travel Planning Platform
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routers
from app.routers import single, multi, strands, ap2

# Create FastAPI app
app = FastAPI(
    title="Voyago API - AI Travel Planning",
    description="""
    **Voyago - Your Intelligent Travel Companion**

    Experience next-generation travel planning powered by advanced AI:

    - **Quick Planning**: Fast, simple trip planning for straightforward journeys
    - **Smart Planning**: Intelligent optimization with budget guarantees
    - **Premium Planning**: Advanced AI with dynamic swarm intelligence
    - **Instant Booking**: Secure autonomous booking with cryptographic payments

    Built with cutting-edge AI technology and enterprise-grade security.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:5173").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint - health check."""
    return {
        "status": "healthy",
        "service": "Voyago API",
        "version": "1.0.0",
        "tagline": "Your Intelligent Travel Companion",
        "features": {
            "quick_planning": "Fast and simple travel planning",
            "smart_planning": "Budget-optimized intelligent planning",
            "premium_planning": "Advanced AI with swarm intelligence",
            "instant_booking": "Secure autonomous booking"
        },
        "documentation": "/docs"
    }


@app.get("/health")
async def health_check():
    """Detailed health check."""
    from app.services.hybrid_data import get_hybrid_service

    data_info = get_hybrid_service().get_data_source_info()

    return {
        "status": "healthy",
        "aws_region": os.getenv("AWS_REGION", "us-east-1"),
        "bedrock_model": os.getenv("BEDROCK_MODEL_ID", "claude-3-5-sonnet"),
        "environment": os.getenv("ENVIRONMENT", "development"),
        "data_source": data_info
    }


# Register routers
app.include_router(single.router)
app.include_router(multi.router)
app.include_router(strands.router)
app.include_router(ap2.router)
# TODO: Include other routers as we build them
# app.include_router(guardrails.router)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handle all unhandled exceptions."""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
            "error": str(exc),
            "type": type(exc).__name__
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=os.getenv("API_RELOAD", "true").lower() == "true"
    )
