# Integration Testing Guide

Integration tests verify that multiple components of your application work correctly together. They test the interactions between different layers like services, repositories, and databases.

## What Are Integration Tests?

Integration tests focus on testing how different parts of your system work together. They:
- Test multiple classes or modules working together
- Use real external dependencies (databases, APIs)
- Run slower than unit tests but faster than functional tests
- Verify data flows between components
- Test business logic with real data persistence

## When to Write Integration Tests

Write integration tests for:
- **Repository database operations**: CRUD operations, queries, transactions
- **Service layer interactions**: Business logic that uses repositories
- **External API integrations**: Third-party service calls
- **Data transformation pipelines**: Complex data processing workflows
- **Cross-component workflows**: Features spanning multiple modules

## Examples from the Project

### 1. Repository Testing (`test_repositories.py`)

Testing database operations with real database:

```python
@pytest.mark.integration 
class TestUserRepository:
    """test user repository database operations"""
    
    async def test_create_user(self, user_repository, test_user_data):
        """test creating user in database"""
        user_data = test_user_data.copy()
        del user_data["password"]  # repository doesn't handle password
        user_data["hashed_password"] = "hashed_password_value"
        
        user = await user_repository.create(obj_in=user_data)
        
        assert user is not None
        assert user.id is not None
        assert user.email == test_user_data["email"]
        assert user.hashed_password == "hashed_password_value"
        assert user.created_at is not None
```

**Why this is a good integration test**:
- Tests real database operations
- Verifies data persistence
- Tests the repository with actual SQL execution
- Validates database constraints and relationships

### 2. Service Layer Testing (`test_services.py`)

Testing business logic with repository interactions:

```python
@pytest.mark.integration
class TestUserService:
    """test user service business logic with repository integration"""
    
    async def test_create_user_success(self, user_service, test_user_create, db_session):
        """test successful user creation through service"""
        user = await user_service.create(test_user_create)
        await db_session.commit()
        
        assert user is not None
        assert user.email == test_user_create.email
        assert user.hashed_password is not None
        assert verify_password(test_user_create.password, user.hashed_password)
        assert user.is_active is True
```

**Why this is a good integration test**:
- Tests service and repository working together
- Verifies password hashing integration
- Tests real database transaction handling
- Validates business logic with persistence

## Integration Testing Patterns

### 1. Database Test Setup

Use a real database (SQLite for speed) with proper cleanup:

```python
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
```

### 2. Transaction Testing

Test transaction handling and rollbacks:

```python
async def test_create_without_commit(self, user_repository, db_session):
    """test creating without committing transaction"""
    user_data = {
        "email": "nocommit@example.com",
        "hashed_password": "hash",
        "first_name": "NoCommit"
    }
    
    user = await user_repository.create(obj_in=user_data, commit_txn=False)
    
    # user should exist in session but not committed
    assert user is not None
    assert user.email == "nocommit@example.com"
    
    # rollback and verify user doesn't persist
    await db_session.rollback()
    
    found_user = await user_repository.get_by_email("nocommit@example.com")
    assert found_user is None
```

### 3. Mocking External Dependencies

Use partial mocking for controlled testing:

```python
@pytest.mark.integration
class TestUserServiceWithMocks:
    """test user service with mocked dependencies for isolation"""
    
    async def test_create_user_repository_interaction(self, db_session):
        """test service properly calls repository during creation"""
        # create mock repository
        mock_repo = AsyncMock()
        mock_user = AsyncMock()
        mock_repo.create.return_value = mock_user
        
        service = UserService(db_session, mock_repo)
        user_create = UserCreate(
            email="test@example.com",
            password="TestPassword123",
            first_name="Test",
            last_name="User"
        )
        
        result = await service.create(user_create)
        
        # verify repository create was called
        mock_repo.create.assert_called_once()
        call_args = mock_repo.create.call_args
        
        # verify password was hashed and removed
        obj_in = call_args.kwargs["obj_in"]
        assert "password" not in obj_in
        assert "hashed_password" in obj_in
        assert obj_in["email"] == "test@example.com"
```

### 4. Complex Query Testing

Test sophisticated database queries:

```python
async def test_get_multi_with_filters(self, user_repository, db_session):
    """test filtering in get_multi"""
    # create users with different statuses
    users_data = [
        {"email": "active1@example.com", "hashed_password": "hash", "is_active": True},
        {"email": "active2@example.com", "hashed_password": "hash", "is_active": True},
        {"email": "inactive1@example.com", "hashed_password": "hash", "is_active": False},
    ]
    
    for user_data in users_data:
        await user_repository.create(obj_in=user_data)
    await db_session.commit()
    
    # filter for active users only
    active_users, total = await user_repository.get_multi(filters={"is_active": True})
    
    assert len(active_users) == 2
    assert total == 2
    assert all(user.is_active for user in active_users)
```

## Best Practices

### 1. Use Real Dependencies
```python
# Good: Use real database
async def test_user_creation(user_service, db_session):
    user = await user_service.create(user_data)
    await db_session.commit()
    # Test with real persistence

# Bad: Mock everything (this becomes a unit test)
@patch('app.repositories.UserRepository')
async def test_user_creation(mock_repo):
    # This is actually a unit test
```

### 2. Test Data Isolation
```python
# Good: Each test gets clean data
@pytest_asyncio.fixture
async def test_user_data():
    import uuid
    unique_id = str(uuid.uuid4())[:8]
    return {
        "email": f"test{unique_id}@example.com",
        "password": "TestPassword123"
    }

# Bad: Shared test data causes conflicts
test_email = "test@example.com"  # Reused across tests
```

### 3. Test Business Logic, Not Implementation
```python
# Good: Test business behavior
async def test_user_creation_sets_default_values(user_service):
    user = await user_service.create(user_data)
    assert user.is_active is True
    assert user.role == UserRole.USER.value

# Bad: Test implementation details
async def test_user_creation_calls_repository_create(user_service):
    # This tests how it works, not what it does
```

### 4. Test Error Conditions
```python
async def test_create_user_duplicate_email(user_service, created_user):
    """test creating user with duplicate email fails"""
    duplicate_data = UserCreate(
        email=created_user.email,  # Duplicate email
        password="AnotherPassword123"
    )
    
    with pytest.raises(IntegrityError):
        await user_service.create(duplicate_data)
```

### 5. Use Meaningful Assertions
```python
# Good: Specific assertions
assert user.email == expected_email
assert user.is_active is True
assert user.created_at is not None

# Bad: Vague assertions
assert user is not None
assert user  # Too general
```

## Common Pitfalls

### 1. Testing Too Little
```python
# Bad: Only testing happy path
async def test_user_creation(user_service):
    user = await user_service.create(valid_data)
    assert user is not None

# Good: Test various scenarios
async def test_user_creation_success(user_service):
    # Test successful creation
    
async def test_user_creation_duplicate_email(user_service):
    # Test error condition
    
async def test_user_creation_invalid_data(user_service):
    # Test validation
```

### 2. Improper Test Isolation
```python
# Bad: Tests depend on each other
class TestUserWorkflow:
    async def test_01_create_user(self):
        self.user = await create_user()
        
    async def test_02_update_user(self):
        await update_user(self.user.id)  # Depends on test_01

# Good: Independent tests
class TestUserWorkflow:
    async def test_create_user(self, user_service):
        user = await user_service.create(user_data)
        
    async def test_update_user(self, user_service, created_user):
        updated = await user_service.update(created_user.id, update_data)
```

### 3. Slow Tests
```python
# Bad: Creating too much test data
async def test_pagination(user_repository):
    # Creating 10,000 users for pagination test
    for i in range(10000):
        await user_repository.create(user_data)

# Good: Create minimal test data
async def test_pagination(user_repository):
    # Create just enough to test pagination (5-10 records)
    for i in range(5):
        await user_repository.create(user_data)
```

## Running Integration Tests

### Run All Integration Tests
```bash
pytest -m integration
```

### Run Specific Integration Test File
```bash
pytest tests/integration/test_repositories.py
```

### Run with Database Output
```bash
pytest -m integration -s --log-cli-level=DEBUG
```

### Run with Coverage
```bash
pytest -m integration --cov=app --cov-report=html
```

## Test Database Setup

### SQLite for Speed
```python
# Fast in-memory or file-based SQLite
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False  # Set to True for SQL debugging
)
```

### PostgreSQL for Production Similarity
```python
# Use test PostgreSQL database for production-like testing
TEST_DATABASE_URL = "postgresql+asyncpg://test_user:test_pass@localhost/test_db"
```

## Measuring Quality

### Coverage Metrics
- Target > 80% line coverage for business logic
- Focus on critical user workflows
- Cover error handling paths

### Performance Metrics
- Integration tests should run in < 30 seconds total
- Individual tests should complete in < 1 second
- Database operations should be optimized

### Data Quality
- Test with realistic data volumes
- Verify data integrity constraints
- Test concurrent access scenarios

## Integration Test Checklist

For each integration test, verify:
- [ ] Uses real database or external service
- [ ] Tests multiple components working together
- [ ] Has proper test data isolation
- [ ] Cleans up after itself
- [ ] Tests both success and failure scenarios
- [ ] Verifies data persistence/changes
- [ ] Has meaningful assertions
- [ ] Runs in reasonable time (< 1 second)

## Conclusion

Integration tests are crucial for ensuring your application components work correctly together. They provide confidence that:

- **Data flows correctly** between layers
- **Business logic works** with real persistence
- **Error handling functions** properly across boundaries
- **Performance is acceptable** under realistic conditions

Good integration tests catch issues that unit tests miss while remaining faster and more focused than functional tests. They form the essential middle layer of your testing pyramid. 