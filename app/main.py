from fastapi import FastAPI
import logging
from contextlib import asynccontextmanager

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.api.v1.api import api_router
from app.exceptions.handlers import add_exception_handlers
from app.middlewares.setup import setup_middlewares
from app.utils.docs import setup_swagger_documentation
from app.utils.response import create_response

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for the FastAPI application.
    
    This context manager is used to manage the lifespan of the application,
    including startup and shutdown events.
    
    Args:
        app: FastAPI application instance
    """
    # Perform startup tasks here
    logger.info("Starting up the application...")
    
    yield
    # Perform shutdown tasks here
    logger.info("Shutting down the application...")
    # Close database connections, etc.

# Create FastAPI app
app = FastAPI(
    title="FastAPI Application",
    description="FastAPI application with SQLAlchemy and PostgreSQL",
    version="0.1.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=None,  # Disable default docs URL
    redoc_url=None, # Disable default redoc URL
    lifespan=lifespan
)

# Mount the "public" folder at "/static" path
app.mount("/images", StaticFiles(directory="app/public/images"), name="images")
app.mount("/css", StaticFiles(directory="app/public/css"), name="css")
app.mount("/js", StaticFiles(directory="app/public/js"), name="js")

# Set up custom Swagger documentation
setup_swagger_documentation(app, settings.API_V1_STR)

# global error handler
add_exception_handlers(app)

# Set up middlewares
setup_middlewares(app)

# Include API router
app.include_router(prefix=settings.API_V1_STR, router=api_router)

# Root health check endpoint
@app.get("/", tags=["health"])
def root():
    """Root endpoint for health checks"""
    data = {"status": "ok", "message": "API is running"}
    return create_response(
        data=data,
        message="API is running",
    )

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    """Favicon endpoint"""
    return FileResponse("app/public/images/favicon.ico")

