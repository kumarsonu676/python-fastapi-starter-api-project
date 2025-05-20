from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.db.session import get_db
from app.utils.common import log_error
from app.utils.response import create_response

router = APIRouter()

@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Health check endpoint",
    description="Simple health check endpoint to verify the API is running",
)
def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint.
    
    This endpoint checks the health of the service and its dependencies.
    It verifies database connectivity and returns status information.
    
    Args:
        db: Database session dependency
        
    Returns:
        Success response with health status
    """
    # Log this operation
    log_error("Health check performed")
    
    # Try to connect to the database
    try:
        # Simple statement to test database connectivity using SQLAlchemy text()
        result = db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    data = {
        "status": "ok",
        "message": "Service is healthy",
        "database": db_status,
        "version": "0.1.0"
    }

    return create_response(
        data=data,
        message="Health check successful"
    )