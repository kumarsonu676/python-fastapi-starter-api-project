from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from app.exceptions.http_exceptions import BaseCustomError
from app.utils.response import create_response
from fastapi import status
from starlette.exceptions import HTTPException as StarletteHTTPException  # Import Starlette's HTTPException

def add_exception_handlers(app: FastAPI) -> None:
    """Add exception handlers to the FastAPI application."""
    
    # Add handler for Starlette's HTTPException (handles non-existent routes)
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        """Handle HTTP exceptions including 404 Not Found for routes"""
        return create_response(
            success=False,
            message=str(exc.detail),
            errors=[str(exc.detail)],
            error_code="NOT_FOUND" if exc.status_code == status.HTTP_404_NOT_FOUND else f"HTTP_ERROR_{exc.status_code}",
            status_code=exc.status_code
        )
    
    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request: Request, exc: ValidationError):
        """Handle Pydantic validation errors"""
        errors = [f"{'.'.join(str(loc) for loc in err['loc'])}: {err['msg']}" for err in exc.errors()]
        return create_response(
            success=False,
            message="Validation error",
            errors=errors,
            error_code="VALIDATION_ERROR",  # Custom error code for validation errors
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle FastAPI request validation errors"""
        errors = [
            f"{'.'.join(str(loc) for loc in err['loc'])}: {err['msg']}"
            for err in exc.errors()
        ]
        return create_response(
            success=False,
            message="Validation error",
            errors=errors,
            error_code="VALIDATION_ERROR",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY  # This is FastAPI's default for validation
        )
    
    @app.exception_handler(BaseCustomError)  # Handle all custom errors with one handler
    async def custom_exception_handler(request: Request, exc: BaseCustomError):
        """Handle all custom exceptions"""
        response = create_response(
            success=False,
            message=exc.detail,
            errors=[exc.detail],
            error_code=getattr(exc, 'error_code', None),
            status_code=exc.status_code
        )
        
        # Add headers if they exist (for UnauthorizedError)
        if hasattr(exc, 'headers') and exc.headers:
            for key, value in exc.headers.items():
                response.headers[key] = value
                
        return response
        
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        """Handle unhandled exceptions"""
        return create_response(
            success=False,
            message="Internal server error",
            errors=["Internal server error"],
            error_code="INTERNAL_ERROR",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )