from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

def setup_cors_middleware(app: FastAPI) -> None:
    """
    Set up CORS middleware for the application.
    
    Args:
        app: FastAPI application instance
    """
    # Configure CORS middleware
    if settings.BACKEND_CORS_ORIGINS:
        # Allow CORS for specified origins
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )