"""
FastAPI application entry point.

This module initializes the FastAPI application, registers all routes,
configures middleware (CORS, etc.), and handles application lifecycle events
like database initialization on startup.

Interactions:
- Imports routes from api/routes/
- Uses database.py for database initialization
- Uses config.py for application settings
- Provides API endpoints for frontend to consume
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.config import settings
from backend.database import init_db
from backend.api.routes import reels, generate


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.
    
    Handles startup and shutdown events for the FastAPI application.
    On startup: initializes database tables.
    On shutdown: performs cleanup if needed.
    
    Args:
        app: FastAPI application instance
    """
    # Startup: Initialize database
    init_db()
    yield
    # Shutdown: Add cleanup code here if needed


# Create FastAPI application instance
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(reels.router, prefix=settings.api_prefix, tags=["reels"])
app.include_router(generate.router, prefix=settings.api_prefix, tags=["generate"])


@app.get("/")
def root():
    """
    Root endpoint for health checks.
    
    Returns:
        dict: Simple status message
    """
    return {"status": "ok", "message": "Brainrot News Reels API is running"}


@app.get("/health")
def health_check():
    """
    Health check endpoint.
    
    Returns:
        dict: Health status information
    """
    return {
        "status": "healthy",
        "version": settings.app_version,
    }

