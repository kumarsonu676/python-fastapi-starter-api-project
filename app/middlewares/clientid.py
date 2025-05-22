from typing import Callable
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings
from app.utils.response import create_response
from fastapi import status

class ClientIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Middleware to check the client ID in the request header.
        Args:
            request: The incoming request
            call_next: The next middleware or route handler
        Returns:
            The response from the next middleware or route handler
        Raises:
            HTTPException: If the client ID is invalid
        """

        # Get the list of valid client IDs from environment variables
        valid_client_ids: list[str] = settings.CLIENT_IDS.split(",")

        # Check if client ID is in the request header
        client_id = request.headers.get("X-Client-ID")

        # Skip client ID check for specific paths if needed
        excluded_paths: list[str] = ["/", "/favicon.ico", "/api/v1/docs", "/api/v1/redoc", "/api/v1/openapi.json", "/api/v1/health", "/api/v1/health/", "/api/v1/auth/token", "/api/v1/auth/token/"]
        if request.url.path in excluded_paths:
            return await call_next(request)
        
        # Validate client ID
        if not client_id:
            return create_response(
                success=False,
                message="Missing X-Client-ID header",
                errors=["Missing X-Client-ID header"],
                status_code=status.HTTP_401_UNAUTHORIZED
            )
            
        if client_id not in valid_client_ids:
            return create_response(
                success=False,
                message="Invalid X-Client-ID",
                errors=["Invalid X-Client-ID"],
                status_code=status.HTTP_403_FORBIDDEN
            )

        # Continue processing the request if client ID is valid
        return await call_next(request)

    
def setup_clientid_middleware(app: FastAPI) -> None:
    """
    Set up client ID middleware for the application.
    This middleware checks the client ID in the request header
    and validates it against a list of valid client IDs.
    Args:
        app: FastAPI application instance
    """
    app.add_middleware(ClientIdMiddleware)
