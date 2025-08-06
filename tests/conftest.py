import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.main import app
from app.db.base_class import Base
from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas.user import UserCreate
from app.repositories.user import UserRepository
from app.services.user_service import UserService
from app.core.security import get_password_hash


# test database url using sqlite for speed and isolation
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False
)

# create test session factory
TestAsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
    class_=AsyncSession
)


@pytest_asyncio.fixture(scope="session")
async def setup_test_db():
    """setup test database schema"""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session(setup_test_db):
    """provide database session for tests"""
    async with TestAsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()


@pytest_asyncio.fixture
async def user_repository(db_session):
    """provide user repository instance"""
    return UserRepository(db_session)


@pytest_asyncio.fixture 
async def user_service(db_session, user_repository):
    """provide user service instance"""
    return UserService(db_session, user_repository)


@pytest_asyncio.fixture
async def test_user_data():
    """provide test user data"""
    import uuid
    unique_id = str(uuid.uuid4())[:8]
    return {
        "email": f"test{unique_id}@example.com",
        "password": "TestPassword123",
        "first_name": "Test",
        "last_name": "User",
        "role": UserRole.USER.value
    }


@pytest_asyncio.fixture
async def test_user_create(test_user_data):
    """provide test user create schema"""
    return UserCreate(**test_user_data)


@pytest_asyncio.fixture
async def created_user(db_session, user_service, test_user_create):
    """create and return test user in database"""
    user = await user_service.create(test_user_create)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def test_admin_data():
    """provide test admin user data"""
    import uuid
    unique_id = str(uuid.uuid4())[:8]
    return {
        "email": f"admin{unique_id}@example.com", 
        "password": "AdminPassword123",
        "first_name": "Admin",
        "last_name": "User",
        "role": UserRole.ADMIN.value
    }


@pytest_asyncio.fixture
async def created_admin(db_session, user_service, test_admin_data):
    """create and return test admin user in database"""
    admin_create = UserCreate(**test_admin_data)
    admin = await user_service.create(admin_create)
    await db_session.commit()
    await db_session.refresh(admin)
    return admin


# override database dependency for testing
async def override_get_db():
    async with TestAsyncSessionLocal() as session:
        yield session


@pytest_asyncio.fixture
async def client(setup_test_db):
    """provide async http client for functional tests"""
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.fixture
def sync_client():
    """provide sync test client for simple tests"""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear() 