# Copilot Instructions for Python FastAPI Project

You are an expert in Python, FastAPI, and scalable API development.

Write concise, technical responses with accurate Python examples.
Use functional, declarative programming; avoid classes where possible.
Prefer iteration and modularization over code duplication.
Use descriptive variable names with auxiliary verbs (e.g., is_active, has_permission).
Use lowercase with underscores for directories and files (e.g., routers/user_routes.py).
Favor named exports for routes and utility functions.
Use the Receive an Object, Return an Object (RORO) pattern.
Use def for pure functions and async def for asynchronous operations.
Use type hints for all function signatures.
Prefer Pydantic models over raw dictionaries for input validation.

## Folder and File Structure Guidelines

1. **App**: Place all application code in the `app` directory.

   - **API**: Place all API routes in the `app/api` folder, with versioning (e.g., `app/api/v1`).
   - **Core**: Place core configuration in the `app/core` folder.
   - **DB**: Place database models and session management in the `app/db` folder.
   - **Models**: Place SQLAlchemy models for database in the `app/models` folder.
   - **Schemas**: Place Pydantic schemas for request/response in the `app/schemas` folder.
   - **Services**: Place business logic in the `app/services` folder.
   - **Dependencies**: Place dependency injection functions in the `app/dependencies` folder.
   - **Middlewares**: Place middleware functions in the `app/middlewares` folder.
   - **Utils**: Place utility functions in the `app/utils` folder.
   - **Repositories**: Place data access code in the `app/repositories` folder.
   - **Exceptions**: Place custom exception handlers in the `app/exceptions` folder.

2. **Tests**: Place all tests in the `tests` directory.

   - **Unit**: Place unit tests in the `tests/unit` folder.
   - **Integration**: Place integration tests in the `tests/integration` folder.
   - **Fixtures**: Place test fixtures in the `tests/fixtures` folder.

3. **Alembic**: Place database migrations in the `alembic` directory.

## Coding Guidelines

- Use **Python 3.9+** features and type hints throughout the codebase.
- **Validate incoming request data** using Pydantic models.
- **Keep route functions thin** by delegating business logic to services.
- **Handle errors** gracefully using FastAPI's exception handlers.
- **Use async/await** for database operations and external API calls.
- **Naming conventions**:
  - `snake_case` for variables, functions, and file names.
  - `PascalCase` for classes and Pydantic models.
- Write **modular, reusable, and well-documented** code.
- When creating a new endpoint, always create corresponding Pydantic schemas for request and response.

## Special Instructions for Copilot

- Only generate code that strictly follows this folder structure and coding style.
- Always separate concerns: route functions should not directly contain business logic or data access.
- Ensure error messages are meaningful and consistent across all APIs.
- Prioritize clean and maintainable code over shortcuts or hacks.
- Use SQLAlchemy with async support when generating database code.

## Best Practices for FastAPI with Python

1. **Use Type Hints**: Always define types for function parameters, return values, and variables.
2. **Modular Structure**: Separate concerns by organizing code into routes, services, and repositories.
3. **Error Handling**: Use FastAPI's exception handlers for centralized error handling.
4. **Environment Variables**: Store sensitive data in environment variables using Pydantic's `BaseSettings`.
5. **Validation**: Use Pydantic models for request validation and documentation.
6. **Logging**: Use Python's built-in logging module configured through settings.
7. **Security**: Implement proper authentication and authorization using FastAPI's security utilities.
8. **Testing**: Write unit and integration tests using pytest.
9. **Documentation**: Leverage FastAPI's automatic Swagger/OpenAPI documentation.
10. **Dependency Injection**: Use FastAPI's dependency injection system for clean code organization.

## API Design

- Use proper HTTP methods (GET, POST, PUT, DELETE, PATCH)
- Implement versioning for your API endpoints (e.g., `/api/v1/users`)
- Return appropriate status codes (200, 201, 400, 401, 403, 404, 500)
- Use path parameters for resource identifiers (e.g., `/users/{user_id}`)
- Use query parameters for filtering, sorting, and pagination
- Group related endpoints using APIRouter with tags
- Document API endpoints with descriptive summaries and descriptions
- Use consistent response formats across endpoints
- Implement proper error handling with custom exception handlers

## Data Validation

- Use Pydantic models for request and response validation
- Define clear schemas with appropriate field types and constraints
- Implement custom validators for complex business rules
- Use dependency injection for common validation logic
- Validate query parameters with appropriate types
- Use Enum classes for fields with a fixed set of values
- Implement proper error messages for validation failures
- Use Field class for advanced field validation

## Authentication & Authorization

- Implement JWT-based authentication
- Use OAuth2PasswordBearer for token-based authentication
- Store passwords with proper hashing (e.g., Bcrypt)
- Implement role-based access control
- Use dependency injection for securing endpoints
- Implement proper token refresh mechanisms
- Set secure cookie attributes for session management
- Use HTTPS for all API communications
- Implement rate limiting for authentication endpoints

## Database Integration

- Use SQLAlchemy ORM for database operations
- Implement async database operations with appropriate drivers
- Use dependency injection for database sessions
- Implement the repository pattern for database access
- Use migrations for database schema changes (Alembic)
- Implement proper transaction management
- Use connection pooling for efficient resource usage
- Properly handle database errors and exceptions
- Implement pagination for database queries that return multiple records

## Dependency Injection

- Use FastAPI's dependency injection system
- Create reusable dependencies
- Use dependencies for database sessions
- Implement authentication as a dependency
- Use dependencies for common validation logic
- Create nested dependencies for complex scenarios
- Properly handle dependency scope (request, session, application)
- Use dependencies for feature flags and configuration

## Performance Optimization

- Use async/await for I/O-bound operations
- Implement proper caching strategies (Redis)
- Use background tasks for time-consuming operations
- Optimize database queries by selecting only required fields
- Use connection pooling for database connections
- Implement proper pagination to limit data load
- Use appropriate serialization/deserialization techniques
- Implement compression for response payloads
- Profile and optimize hot paths in the application

## Testing

- Write unit tests for utility functions and services
- Implement integration tests for API endpoints
- Use TestClient for API testing
- Use pytest fixtures for test setup and teardown
- Mock external dependencies in tests
- Implement database fixtures for testing with databases
- Use factories for test data generation
- Test error cases and edge conditions
- Aim for high test coverage

## Error Handling

- Implement centralized error handling
- Create custom exception classes for different error types
- Return appropriate HTTP status codes for different errors
- Provide helpful error messages for debugging
- Log errors with contextual information
- Handle validation errors gracefully
- Implement proper exception handling for external services
- Return consistent error response structure

## Security

- Implement proper authentication and authorization
- Use HTTPS for all communications
- Properly handle sensitive data (no logging of passwords or tokens)
- Implement CORS with appropriate restrictions
- Use secure headers (X-XSS-Protection, Content-Security-Policy)
- Implement rate limiting for API endpoints
- Validate all user input to prevent injection attacks
- Use parameterized queries for database operations
- Keep dependencies updated to avoid vulnerabilities

## Documentation

- Use OpenAPI for API documentation
- Document all endpoints with clear descriptions
- Provide examples for request and response payloads
- Document authentication requirements
- Use tags to organize API documentation
- Document error responses
- Generate interactive documentation with Swagger UI and ReDoc
- Keep documentation up-to-date with code changes

## Deployment

- Use containerization (Docker) for consistent environments
- Implement proper health check endpoints
- Use environment variables for configuration
- Implement proper logging for production
- Set up monitoring and alerting
- Use CI/CD for automated testing and deployment
- Implement proper database migration processes
- Configure appropriate scaling strategies
- Use proper resource management

## Asynchronous Operations

- Use async/await for I/O-bound operations
- Implement background tasks for time-consuming operations
- Use proper exception handling in async code
- Implement proper cancellation handling
- Use appropriate concurrency limits
- Implement proper connection pooling for external services
- Use event-driven architecture for asynchronous workflows
- Properly handle long-running tasks

---

## Code Generation Examples

### Example: Creating a SQLAlchemy model

```python
#filepath: `app/api/models/country.py`

from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from app.db.base_class import Base

class Country(Base):
    """Country model for database"""
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True, unique=True)
    code = Column(String(3), nullable=False, unique=True, index=True)  # ISO 3166-1 alpha-3 code
    phone_code = Column(String(5))  # International dialing code
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

```

### Example: Register the model in `app/db/base.py`

```python
#filepath: `app/db/base.py`

# Import all models for Alembic to detect
from app.db.base_class import Base
from app.models.user import User
from app.models.country import Country

```

### Example: Creating a Pydantic schema

```python
#filepath: `app/schemas/country.py`

from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class CountryBase(BaseModel):
    """Base Country Schema with common attributes"""
    name: str = Field(..., min_length=2, max_length=100, description="Name of the country")
    code: str = Field(..., min_length=2, max_length=3, description="ISO country code (2 or 3 characters)")
    phone_code: Optional[str] = Field(None, max_length=5, description="International calling code")
    is_active: Optional[bool] = Field(True, description="Whether the country is active in the system")

class CountryCreate(CountryBase):
    """Schema for creating a new country"""
    pass

class CountryUpdate(CountryBase):
    """Schema for updating country information"""
    pass

class CountryResponse(CountryBase):
    """Schema for country response"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic configuration"""
        orm_mode = True

```

### Example: Creating a Repository

```python

#filepath: `app/repositories/country.py`

from typing import Optional
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.country import Country
from app.repositories.base import BaseRepository

class CountryRepository(BaseRepository[Country]):
    """Repository for country-related database operations"""

    def __init__(self, db: AsyncSession):
        """Initialize with database session and model"""
        super().__init__(db, Country)


```

### Example: Creating a Service

```python
#filepath: `app/services/country.py`

from typing import List, Optional, Union

from app.core.security import get_password_hash
from app.exceptions.http_exceptions import ConflictError, NotFoundError
from app.models.country import Country
from app.repositories.country import CountryRepository
from app.schemas.country import CountryCreate, CountryUpdate

class CountryService:

    def __init__(self, country_repo: CountryRepository):
        """Initialize with country repository"""
        self.country_repo = country_repo

    async def get(self, country_id: int) -> Optional[Country]:
        """Get a country by ID"""
        result = await self.country_repo.get(country_id)
        return result

    async def get_all(self) -> List[Country]:
        """Get all countries"""
        countries, _ = await self.country_repo.get_multi()
        return countries

    async def create(self, obj_in: CountryCreate) -> Country:

        # Check if country with the same code already exists
        existing_country = await self.country_repo.get_by_code(obj_in.code)
        if existing_country:
            raise ConflictError(
                error_code="COUNTRY_ALREADY_EXISTS",
                detail=f"Country with code {obj_in.code} already exists"
            )

        """Create a new country"""
        return await self.country_repo.create(obj_in=obj_in.dict())

    async def update(self, country_id: int, obj_in: Union[CountryUpdate, dict]) -> Optional[Country]:
        """Update a country"""
        # Get current country
        db_obj = await self.country_repo.get(country_id)
        if not db_obj:
            raise NotFoundError(
                error_code="COUNTRY_NOT_FOUND",
                detail=f"Country with ID {country_id} not found"
            )

        # Convert to dict if it's a Pydantic model
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.dict(exclude_unset=True)

        # Check if country with the same code already exists
        existing_country = await self.country_repo.get_by_code(update_data.get("code") or "")
        if existing_country is not None and existing_country.id.__eq__(country_id) is False:
            raise ConflictError(
                error_code="COUNTRY_ALREADY_EXISTS",
                detail=f"Country with code {update_data.get('code')} already exists"
            )

        # Update fields
        for key, value in update_data.items():
            setattr(db_obj, key, value)

        # Convert Country model to dictionary for repository update
        update_dict = {
            column.name: getattr(db_obj, column.name)
            for column in Country.__table__.columns
            if column.name != "id"
        }

        return await self.country_repo.update(id=country_id, obj_in=update_dict)

    async def delete(self, country_id: int) -> Optional[Country]:
        """Delete a country by ID"""

        # Check if country exists
        db_obj = await self.country_repo.get(country_id)
        if not db_obj:
            raise NotFoundError(
                error_code="COUNTRY_NOT_FOUND",
                detail=f"Country with ID {country_id} not found"
            )

        result = await self.country_repo.delete(id=country_id)
        return result

```

### Example: Registering the Service Dependency in `app/dependencies/services.py` file

```python
#filepath: `app/dependencies/services.py`


from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.repositories.user import UserRepository
from app.services.user import UserService

from app.repositories.country import CountryRepository
from app.services.country import CountryService


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db))

def get_country_service(db: AsyncSession = Depends(get_db)) -> CountryService:
    return CountryService(CountryRepository(db))

```

### Example: Creating a FastAPI Router/Endpoint

```python
#filepath: `app/api/v1/endpoints/country.py`

from typing import List
from fastapi import APIRouter, Depends, status

from app.dependencies.auth import authorize
from app.dependencies.services import get_country_service
from app.dtos.custom_response_dto import CustomResponse
from app.models.user import UserRole
from app.schemas.country import CountryCreate, CountryResponse, CountryUpdate
from app.schemas.user import UserResponse
from app.services.country import CountryService
from app.utils.response import create_response

router = APIRouter()

@router.get(
    "/",
    response_model=CustomResponse[List[CountryResponse]],
    summary="Get all countries",
    description="Get a list of all countries"
)
async def get_countries(
    country_service: CountryService = Depends(get_country_service)
):
    countries = await country_service.get_all_countries()

    if not countries:
        return create_response(
            data=None
        )

    return create_response(
        data=[CountryResponse.from_orm(countries) for countries in countries]
    )

@router.get(
    "/{id}",
    response_model=CustomResponse[CountryResponse],
    summary="Get country by ID",
    description="Get a country by its ID"
)
async def get_country(
    id: int,
    country_service: CountryService = Depends(get_country_service)
):
    country = await country_service.get(id)

    if not country:
        return create_response(
            data=None
        )

    return create_response(
        data=CountryResponse.from_orm(country)
    )


@router.post(
    "/",
    response_model=CustomResponse[CountryResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new country",
    description="Create a new country with the provided details"
)
async def create_country(
    country_create: CountryCreate,
    country_service: CountryService = Depends(get_country_service),
    _ = Depends(authorize(allowed_roles=[UserRole.ADMIN.value]))
):

    country = await country_service.create(obj_in=country_create)

    return create_response(
        data=CountryResponse.from_orm(country)
    )



@router.put(
    "/{id}",
    response_model=CustomResponse[CountryResponse],
    summary="Update a country",
    description="Update an existing country by its ID"
)
async def update_country(
    id: int,
    country_update: CountryUpdate,
    country_service: CountryService = Depends(get_country_service),
    _: UserResponse = Depends(authorize(allowed_roles=[UserRole.ADMIN.value]))
):
    country = await country_service.update(id, obj_in=country_update)

    return create_response(
        data=CountryResponse.from_orm(country)
    )


@router.delete(
    "/{id}",
    response_model=CustomResponse[CountryResponse],
    summary="Delete a country",
    description="Delete a country by its ID"
)
async def delete_country(
    id: int,
    country_service: CountryService = Depends(get_country_service),
    _ = Depends(authorize(allowed_roles=[UserRole.ADMIN.value]))
):
    await country_service.delete(id)

    return create_response(
        data="Country deleted successfully",
        status_code=status.HTTP_204_NO_CONTENT
    )

```

### Example: Registering the Router in `app/api/v1/api.py`

```python
#filepath: `app/api/v1/api.py`

from fastapi import APIRouter

from app.api.v1.endpoints import health
from app.api.v1.endpoints import users
from app.api.v1.endpoints import auth
from app.api.v1.endpoints import country

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(country.router, prefix="/countries", tags=["countries"])

# This is the main API router that includes all endpoint routers

```

### Example: Creating the middleware

```python
#filepath: `app/middlewares/custom_middleware.py`

from typing import Callable
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings
from app.utils.response import create_response
from fastapi import status

class CustomMiddleware(BaseHTTPMiddleware):
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

        # if path starts with /images, /css, /js, /favicon.ico, skip client ID check
        if request.url.path.startswith("/images") or request.url.path.startswith("/css") or request.url.path.startswith("/js") or request.url.path.startswith("/favicon.ico"):
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


def setup_custom_middleware(app: FastAPI) -> None:
    """
    Set up custom middleware for the application.
    This middleware checks the client ID in the request header
    and validates it against a list of valid client IDs.
    Args:
        app: FastAPI application instance
    """
    app.add_middleware(CustomMiddleware)


```

### Example: Registering the Middleware in `app/middlewares/setup.py`

```python
#filepath: `app/main.py`

from fastapi import FastAPI
from app.middlewares.custom_middleware import setup_custom_middleware

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

    # Set up custom middleware
    setup_custom_middleware(app)

```

## Notes

- Replace placeholders like `<resource>`, `<model>`, and `<schema>` with actual names relevant to the use case.
- Always use Pydantic models for data validation and serialization.
- Keep routes thin by delegating business logic to service classes.
- Use async/await for database operations to ensure proper performance.
- Follow proper error handling patterns with custom exceptions.
- Organize code by responsibility (routes, services, repositories).
- Use SQLAlchemy and Alembic for database interactions and migrations.
- Leverage FastAPI's built-in dependency injection system for clean code organization.
- Ensure all endpoints are documented with OpenAPI specifications.
- Use environment variables for configuration and sensitive data management.
