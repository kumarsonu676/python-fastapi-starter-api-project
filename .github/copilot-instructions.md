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

### Example: Creating a Route

```python
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.schemas.common import PaginatedResponse
from app.services.user_service import UserService
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user with the provided details"
)
async def create_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """
    Create a new user.

    Args:
        user_in: User data to create
        db: Database session

    Returns:
        Newly created user data

    Raises:
        HTTPException: If user with the same email already exists
    """
    user_service = UserService(db)
    existing_user = await user_service.get_by_email(user_in.email)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    return await user_service.create(user_in)

@router.get(
    "/",
    response_model=PaginatedResponse[UserResponse],
    summary="Get all users",
    description="Get a list of users with optional pagination and filtering"
)
async def get_users(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Max number of records to return"),
    name: Optional[str] = Query(None, description="Filter by name"),
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> PaginatedResponse[UserResponse]:
    """
    Get list of users with pagination and optional filtering.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        name: Optional filter by name
        current_user: Currently authenticated user
        db: Database session

    Returns:
        Paginated list of users
    """
    user_service = UserService(db)
    users, total = await user_service.get_multi(skip=skip, limit=limit, name=name)

    return PaginatedResponse(
        items=users,
        total=total,
        page=skip // limit + 1 if limit else 1,
        size=limit,
        pages=(total + limit - 1) // limit if limit else 1
    )

@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
    description="Get detailed information about a specific user"
)
async def get_user(
    user_id: int = Path(..., description="The ID of the user to get"),
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """
    Get user by ID.

    Args:
        user_id: User ID
        current_user: Currently authenticated user
        db: Database session

    Returns:
        User data

    Raises:
        HTTPException: If user not found
    """
    user_service = UserService(db)
    user = await user_service.get(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user

@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update user",
    description="Update a user's information"
)
async def update_user(
    user_in: UserUpdate,
    user_id: int = Path(..., description="The ID of the user to update"),
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """
    Update user information.

    Args:
        user_id: User ID to update
        user_in: Updated user data
        current_user: Currently authenticated user
        db: Database session

    Returns:
        Updated user data

    Raises:
        HTTPException: If user not found
    """
    user_service = UserService(db)
    user = await user_service.get(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return await user_service.update(user_id, user_in)

@router.delete(
    "/{user_id}",
    response_model=UserResponse,
    summary="Delete user",
    description="Delete a user"
)
async def delete_user(
    user_id: int = Path(..., description="The ID of the user to delete"),
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """
    Delete a user.

    Args:
        user_id: User ID to delete
        current_user: Currently authenticated user
        db: Database session

    Returns:
        Deleted user data

    Raises:
        HTTPException: If user not found
    """
    user_service = UserService(db)
    user = await user_service.get(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return await user_service.delete(user_id)
```

### Example: Creating Pydantic Schemas

```python
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator

class UserBase(BaseModel):
    """Base User Schema with common attributes"""
    email: EmailStr
    first_name: Optional[str] = Field(None, min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, min_length=2, max_length=50)
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    """Schema for creating a new user"""
    email: EmailStr
    password: str = Field(..., min_length=8)

    @validator('password')
    def password_strength(cls, v):
        """Validate password strength"""
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c in "!@#$%^&*()-_=+[]{}|;:,.<>?/`~" for c in v):
            raise ValueError('Password must contain at least one special character')
        return v

class UserUpdate(BaseModel):
    """Schema for updating user information"""
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, min_length=2, max_length=50)
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    """Schema for user response"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
```

### Example: Creating a Common Schema

```python
from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

T = TypeVar('T')

class PaginatedResponse(GenericModel, Generic[T]):
    """Generic paginated response schema"""
    items: List[T]
    total: int
    page: int
    size: int
    pages: int

class ErrorResponse(BaseModel):
    """Standard error response schema"""
    detail: str
    code: Optional[str] = None

class SuccessResponse(BaseModel):
    """Standard success response schema with no data"""
    message: str = "Operation completed successfully"
```

### Example: Creating a Database Model

```python
from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class User(Base):
    """User model for database"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Define relationships
    items = relationship("Item", back_populates="owner")
```

### Example: Creating a Service

```python
from typing import List, Optional, Tuple, Union
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash

class UserService:
    """Service for user-related operations"""

    def __init__(self, db: AsyncSession):
        """Initialize with database session"""
        self.db = db

    async def get(self, user_id: int) -> Optional[User]:
        """Get a user by ID"""
        query = select(User).where(User.id == user_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by email"""
        query = select(User).where(User.email == email)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_multi(
        self,
        skip: int = 0,
        limit: int = 100,
        name: Optional[str] = None
    ) -> Tuple[List[User], int]:
        """
        Get multiple users with filtering and pagination

        Returns:
            Tuple containing list of users and total count
        """
        # Base query
        query = select(User)

        # Apply filters if provided
        if name:
            query = query.where(
                or_(
                    User.first_name.ilike(f"%{name}%"),
                    User.last_name.ilike(f"%{name}%")
                )
            )

        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total = await self.db.execute(count_query)
        total = total.scalar_one()

        # Apply pagination
        query = query.offset(skip).limit(limit)

        # Execute query
        result = await self.db.execute(query)
        users = result.scalars().all()

        return users, total

    async def create(self, obj_in: UserCreate) -> User:
        """Create a new user"""
        hashed_password = get_password_hash(obj_in.password)

        # Create user object
        db_obj = User(
            email=obj_in.email,
            hashed_password=hashed_password,
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            is_active=obj_in.is_active
        )

        # Add to database
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)

        return db_obj

    async def update(self, user_id: int, obj_in: Union[UserUpdate, dict]) -> Optional[User]:
        """Update a user"""
        # Get current user
        db_obj = await self.get(user_id)
        if not db_obj:
            return None

        # Convert to dict if it's a Pydantic model
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.dict(exclude_unset=True)

        # Update user attributes
        for field, value in update_data.items():
            if field != "password" and hasattr(db_obj, field) and value is not None:
                setattr(db_obj, field, value)

        # Handle password update separately
        if "password" in update_data and update_data["password"]:
            db_obj.hashed_password = get_password_hash(update_data["password"])

        # Commit changes
        await self.db.commit()
        await self.db.refresh(db_obj)

        return db_obj

    async def delete(self, user_id: int) -> Optional[User]:
        """Delete a user"""
        db_obj = await self.get(user_id)
        if not db_obj:
            return None

        await self.db.delete(db_obj)
        await self.db.commit()

        return db_obj
```

### Example: Creating a Repository

```python
from typing import List, Optional, Tuple, Dict, Any
from sqlalchemy import func, select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User

class UserRepository:
    """Repository for user-related database operations"""

    def __init__(self, db: AsyncSession):
        """Initialize with database session"""
        self.db = db

    async def get(self, user_id: int) -> Optional[User]:
        """Get a user by ID"""
        query = select(User).where(User.id == user_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by email"""
        query = select(User).where(User.email == email)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_multi(
        self,
        filters: Dict[str, Any] = None,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[List[User], int]:
        """
        Get multiple users with filtering and pagination

        Args:
            filters: Optional dict of filter conditions
            skip: Number of records to skip
            limit: Max number of records to return

        Returns:
            Tuple containing list of users and total count
        """
        # Base query
        query = select(User)

        # Apply filters if provided
        if filters:
            if "name" in filters and filters["name"]:
                query = query.where(
                    or_(
                        User.first_name.ilike(f"%{filters['name']}%"),
                        User.last_name.ilike(f"%{filters['name']}%")
                    )
                )
            if "email" in filters and filters["email"]:
                query = query.where(User.email.ilike(f"%{filters['email']}%"))
            if "is_active" in filters and filters["is_active"] is not None:
                query = query.where(User.is_active == filters["is_active"])

        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total = await self.db.execute(count_query)
        total = total.scalar_one()

        # Apply pagination
        query = query.offset(skip).limit(limit)

        # Execute query
        result = await self.db.execute(query)
        users = result.scalars().all()

        return users, total

    async def create(self, user_data: Dict[str, Any]) -> User:
        """Create a new user"""
        # Create user object
        db_obj = User(**user_data)

        # Add to database
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)

        return db_obj

    async def update(self, user_id: int, update_data: Dict[str, Any]) -> Optional[User]:
        """
        Update a user

        Args:
            user_id: ID of user to update
            update_data: Dict of fields to update

        Returns:
            Updated user object or None if not found
        """
        # Get current user
        db_obj = await self.get(user_id)
        if not db_obj:
            return None

        # Update user attributes
        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        # Commit changes
        await self.db.commit()
        await self.db.refresh(db_obj)

        return db_obj

    async def delete(self, user_id: int) -> Optional[User]:
        """Delete a user"""
        db_obj = await self.get(user_id)
        if not db_obj:
            return None

        await self.db.delete(db_obj)
        await self.db.commit()

        return db_obj
```

### Example: Creating a Dependency

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.core.config import settings
from app.core.security import verify_token
from app.models.user import User
from app.schemas.token import TokenPayload
from app.services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Get the current authenticated user from the token.

    Args:
        token: JWT access token
        db: Database session

    Returns:
        Current authenticated user

    Raises:
        HTTPException: If authentication fails
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode token
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise credentials_exception

        token_data = TokenPayload(sub=str(user_id))
    except JWTError:
        raise credentials_exception

    # Get user from database
    user_service = UserService(db)
    user = await user_service.get(int(token_data.sub))

    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )

    return user

async def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Get the current authenticated superuser.

    Args:
        current_user: Current authenticated user

    Returns:
        Current authenticated superuser

    Raises:
        HTTPException: If user is not a superuser
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    return current_user
```

### Example: Creating Core Configuration

```python
from typing import Any, Dict, Optional, List
from pydantic import BaseSettings, EmailStr, validator, PostgresDsn
import secrets

class Settings(BaseSettings):
    """Application settings"""

    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    ALGORITHM: str = "HS256"

    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """Parse CORS origins from string or list"""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database settings
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        """Construct database URI from components"""
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    # Email settings
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None

    # First superuser
    FIRST_SUPERUSER_EMAIL: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    class Config:
        """Configuration for settings"""
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

### Example: Database Session Management

```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Create async engine
engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    echo=False,
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db() -> AsyncSession:
    """
    Dependency for getting async DB session

    Yields:
        AsyncSession: SQLAlchemy async session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

### Example: Base Database Model Class

```python
from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:
    """Base class for all database models"""

    # Generate __tablename__ automatically based on class name
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
```

### Example: Creating a Custom Exception

```python
from fastapi import HTTPException, status

class NotFoundError(HTTPException):
    """Exception raised when a resource is not found"""

    def __init__(self, resource_name: str, resource_id: Any = None):
        detail = f"{resource_name} not found"
        if resource_id:
            detail = f"{resource_name} with id {resource_id} not found"

        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )

class ConflictError(HTTPException):
    """Exception raised when there's a conflict with existing resources"""

    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )

class UnauthorizedError(HTTPException):
    """Exception raised for authentication failures"""

    def __init__(self, detail: str = "Not authenticated"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )

class ForbiddenError(HTTPException):
    """Exception raised for permission issues"""

    def __init__(self, detail: str = "Not enough permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )

class BadRequestError(HTTPException):
    """Exception raised for invalid requests"""

    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )
```

### Example: Main Application Setup

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
import logging

from app.api.v1.api import api_router
from app.core.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Create FastAPI app
app = FastAPI(
    title="FastAPI Application",
    description="FastAPI application with SQLAlchemy, PostgreSQL, and more",
    version="0.1.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=None,  # Disable default docs URL
    redoc_url=None,  # Disable default redoc URL
)

# Set up CORS middleware
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Custom docs URL
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        title="API Docs",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui.css",
    )

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", include_in_schema=False)
def root():
    """Root endpoint for health checks"""
    return {"message": "API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
```

## Notes

- Replace placeholders like `<resource>`, `<model>`, and `<schema>` with actual names relevant to your use case.
- Always use Pydantic models for data validation and serialization.
- Keep routes thin by delegating business logic to service classes.
- Use async/await for database operations to ensure proper performance.
- Follow proper error handling patterns with custom exceptions.
- Organize code by responsibility (routes, services, repositories).
- Use SQLAlchemy and Alembic for database interactions and migrations.
- Leverage FastAPI's built-in dependency injection system for clean code organization.
