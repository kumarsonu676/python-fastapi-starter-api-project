# Testing Guide for FastAPI Applications

This guide demonstrates three essential layers of testing for modern web applications, using a FastAPI project as an example. Each layer serves a specific purpose and provides different types of confidence in your code.

## Testing Pyramid Overview

```
     /\
    /  \    Functional Tests (Few)
   /____\   - End-to-end workflows
  /      \  - Full application testing
 /        \ - Real HTTP requests
/__________\
Integration Tests (Some)
- Multi-component interactions
- Database operations
- Service layer testing

Unit Tests (Many)
- Individual functions
- Pure logic testing
- Fast and isolated
```

## Three Layers of Testing

### 1. Unit Tests 🧪
**Purpose**: Test individual functions and methods in isolation
**Speed**: Very Fast (< 1ms per test)
**Scope**: Single function or method
**Dependencies**: Mocked or stubbed

Unit tests focus on testing the smallest units of code - individual functions, methods, or classes. They should be fast, isolated, and test pure logic without external dependencies.

**What to Test**:
- Complex business logic functions
- Validation logic
- Utility functions
- Algorithm implementations
- Edge cases and error conditions

**Example**: Testing password hashing functions
```python
def test_get_password_hash_returns_hash():
    password = "TestPassword123"
    hashed = get_password_hash(password)
    
    assert hashed is not None
    assert hashed != password
    assert len(hashed) > 20
    assert hashed.startswith("$2b$")
```

### 2. Integration Tests 🔗
**Purpose**: Test how multiple components work together
**Speed**: Medium (100ms - 1s per test)
**Scope**: Multiple classes, database operations
**Dependencies**: Real database, real services

Integration tests verify that different parts of your application work correctly when combined. They test the interaction between layers like services and repositories.

**What to Test**:
- Repository database operations
- Service layer business logic
- External API integrations
- Cross-component workflows
- Data transformation pipelines

**Example**: Testing user service with repository
```python
async def test_create_user_success(self, user_service, test_user_create, db_session):
    user = await user_service.create(test_user_create)
    await db_session.commit()
    
    assert user is not None
    assert user.email == test_user_create.email
    assert verify_password(test_user_create.password, user.hashed_password)
```

### 3. Functional Tests 🌐
**Purpose**: Test complete user workflows end-to-end
**Speed**: Slow (1s+ per test)
**Scope**: Full application, real HTTP requests
**Dependencies**: Complete running application

Functional tests simulate real user interactions with your application. They test the entire stack from HTTP request to database and back.

**What to Test**:
- API endpoint workflows
- Authentication and authorization
- Error handling and edge cases
- Complete user journeys
- Integration with external systems

**Example**: Testing user registration and login flow
```python
async def test_complete_user_registration_and_login_flow(self, client: AsyncClient):
    # Step 1: Register new user
    registration_data = {...}
    register_response = await client.post("/api/v1/auth/register", json=registration_data)
    assert register_response.status_code == 201
    
    # Step 2: Login with registered user
    login_response = await client.post("/api/v1/auth/login", json=login_data)
    token = login_response.json()["data"]
    
    # Step 3: Access protected endpoint
    headers = {"Authorization": f"Bearer {token}"}
    me_response = await client.get("/api/v1/users/me", headers=headers)
    assert me_response.status_code == 200
```

## Running Tests

### Run All Tests
```bash
pytest
```

### Run by Layer
```bash
# Unit tests only (fast)
pytest -m unit

# Integration tests only
pytest -m integration

# Functional tests only
pytest -m functional
```

### Run with Coverage
```bash
pytest --cov=app --cov-report=html
```

### Parallel Execution
```bash
pytest -n auto  # Requires pytest-xdist
```

## Test Organization

```
tests/
├── conftest.py              # Shared fixtures
├── unit/                    # Unit tests
│   ├── test_security.py     # Security functions
│   ├── test_schemas.py      # Validation logic
│   └── test_utils.py        # Utility functions
├── integration/             # Integration tests
│   ├── test_repositories.py # Database operations
│   └── test_services.py     # Service layer
├── functional/              # Functional tests
│   └── test_user_endpoints.py # API endpoints
└── docs/                    # Documentation
    ├── testing_guide.md
    ├── unit_testing.md
    ├── integration_testing.md
    └── functional_testing.md
```

## Best Practices

### General Testing Principles
1. **Follow the Testing Pyramid**: Many unit tests, some integration tests, few functional tests
2. **Test Behavior, Not Implementation**: Focus on what the code should do, not how it does it
3. **Use Descriptive Test Names**: Test names should explain what is being tested and expected outcome
4. **Arrange-Act-Assert**: Structure tests with clear setup, execution, and verification phases
5. **One Assertion Per Test**: Each test should verify one specific behavior
6. **Fast and Deterministic**: Tests should run quickly and produce consistent results

### Layer-Specific Guidelines

#### Unit Tests
- Mock all external dependencies
- Test edge cases and error conditions
- Keep tests simple and focused
- Use parameterized tests for multiple scenarios
- Test pure functions when possible

#### Integration Tests
- Use test database for isolation
- Test realistic data flows
- Verify cross-component interactions
- Test transaction handling
- Clean up test data properly

#### Functional Tests
- Test real user workflows
- Use realistic test data
- Test authentication and authorization
- Verify error responses
- Test complete request/response cycles

## Common Patterns

### Test Fixtures
Use pytest fixtures for reusable test setup:
```python
@pytest_asyncio.fixture
async def created_user(db_session, user_service, test_user_create):
    user = await user_service.create(test_user_create)
    await db_session.commit()
    return user
```

### Mocking External Dependencies
```python
@patch('app.services.user_service.get_password_hash')
async def test_create_user_password_hashing_called(self, mock_hash, db_session):
    mock_hash.return_value = "hashed_password_value"
    # Test continues...
```

### Async Testing
```python
@pytest.mark.asyncio
async def test_async_function():
    result = await some_async_function()
    assert result is not None
```

## Test Data Management

### Test Database Setup
- Use SQLite for fast test execution
- Create/destroy schema for each test session
- Use transactions for test isolation
- Provide clean fixtures for common entities

### Test Data Factories
Create reusable test data generators:
```python
@pytest_asyncio.fixture
async def test_user_data():
    return {
        "email": "test@example.com",
        "password": "TestPassword123",
        "first_name": "Test",
        "last_name": "User",
        "role": UserRole.USER.value
    }
```

## Debugging Tests

### Running Individual Tests
```bash
pytest tests/unit/test_security.py::TestPasswordSecurity::test_verify_password_correct -v
```

### Debug Mode
```bash
pytest --pdb  # Drop into debugger on failure
```

### Verbose Output
```bash
pytest -v -s  # Verbose with print statements
```

## Continuous Integration

### GitHub Actions Example
```yaml
- name: Run Tests
  run: |
    pytest -m unit --cov=app
    pytest -m integration --cov=app --cov-append
    pytest -m functional --cov=app --cov-append
```

### Test Environment Variables
```bash
export TESTING=true
export DATABASE_URL=sqlite:///./test.db
```

## Metrics and Coverage

### Coverage Goals
- Unit Tests: > 90% line coverage
- Integration Tests: > 80% feature coverage
- Functional Tests: > 70% user journey coverage

### Quality Metrics
- Test execution time: < 30 seconds for full suite
- Test reliability: > 99% pass rate
- Test maintainability: < 5 minutes to understand and modify

## Conclusion

This three-layer testing approach provides comprehensive coverage while maintaining development velocity:

- **Unit tests** catch bugs early and enable confident refactoring
- **Integration tests** verify component interactions work correctly
- **Functional tests** ensure the complete user experience works

Remember: Tests are code too - keep them clean, maintainable, and well-documented! 