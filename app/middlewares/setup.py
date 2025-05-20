from fastapi import FastAPI

from app.middlewares.cors import setup_cors_middleware
from app.middlewares.logging import setup_logging_middleware
from app.middlewares.clientid import setup_clientid_middleware

def setup_middlewares(app: FastAPI) -> None:
    """
    Set up all middlewares for the application.
    
    Args:
        app: FastAPI application instance
    """
    # Set up CORS middleware
    setup_cors_middleware(app)
    
    # Set up logging middleware
    setup_logging_middleware(app)

    # Set up client ID middleware
    setup_clientid_middleware(app)