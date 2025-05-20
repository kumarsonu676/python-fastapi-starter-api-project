import time
from typing import Callable
import logging

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging requests and responses"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process the request, log timing and status code.
        
        Args:
            request: The incoming request
            call_next: The next middleware or route handler
            
        Returns:
            The response from the next middleware or route
        """
        start_time = time.time()
        
        # Get request details
        method = request.method
        url = str(request.url)
        
        # Log the request
        logger.info(f"Request: {method} {url}")
        
        # Process the request
        try:
            response = await call_next(request)
            
            # Calculate processing time
            process_time = time.time() - start_time
            
            # Log the response
            logger.info(
                f"Response: {method} {url} - Status: {response.status_code} - "
                f"Completed in {process_time:.4f}s"
            )
            
            # Add custom header with processing time
            response.headers["X-Process-Time"] = str(process_time)
            
            return response
        except Exception as e:
            # Log any unhandled exceptions
            process_time = time.time() - start_time
            logger.error(
                f"Error: {method} {url} - Error: {str(e)} - "
                f"Terminated in {process_time:.4f}s"
            )
            raise

def setup_logging_middleware(app: FastAPI) -> None:
    """
    Set up logging middleware for the application.
    
    Args:
        app: FastAPI application instance
    """
    app.add_middleware(LoggingMiddleware)