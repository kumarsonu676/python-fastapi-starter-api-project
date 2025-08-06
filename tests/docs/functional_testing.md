# Functional Testing Guide

Functional tests verify that your application works correctly from the user's perspective. They test complete user workflows by making real HTTP requests to your API and validating the full request-response cycle.

## What Are Functional Tests?

Functional tests simulate real user interactions with your application. They:
- Test the complete application stack (HTTP → Controllers → Services → Database)
- Make actual HTTP requests to API endpoints
- Test user workflows end-to-end
- Verify authentication and authorization
- Test error handling and edge cases
- Run the slowest but provide the highest confidence

## When to Write Functional Tests

Write functional tests for:
- **Complete user workflows**: Registration → Login → Access protected resources
- **API endpoint behavior**: Request/response formats, status codes, headers
- **Authentication flows**: Login, token validation, role-based access
- **Error scenarios**: Invalid inputs, unauthorized access, not found cases
- **Business workflows**: Multi-step processes that span several endpoints

## Examples from the Project

### 1. User Registration Workflow (`test_user_endpoints.py`)

Testing complete user registration flow:

```python
@pytest.mark.functional
class TestUserRegistration:
    """test user registration endpoints with full app"""
    
    async def test_register_user_success(self, client: AsyncClient):
        """test successful user registration"""
        user_data = {
            "email": "newuser@example.com",
            "password": "NewPassword123",
            "first_name": "New",
            "last_name": "User"
        }
        
        response = await client.post("/api/v1/auth/register", json=user_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        
        assert data["success"] is True
        assert data["message"] == "User created successfully"
        assert data["data"]["email"] == user_data["email"]
        assert data["data"]["role"] == UserRole.USER.value
        assert "hashed_password" not in data["data"]  # sensitive data excluded
```

**Why this is a good functional test**:
- Tests the complete HTTP request/response cycle
- Verifies API contract (status codes, response format)
- Tests real data validation and business logic
- Ensures sensitive data is properly excluded from responses

### 2. Authentication and Authorization (`test_user_endpoints.py`)

Testing login and protected endpoint access:

```python
@pytest.mark.functional
class TestUserAuthentication:
    """test user authentication endpoints"""
    
    async def test_login_success(self, client: AsyncClient, created_user, test_user_data):
        """test successful user login"""
        login_data = {
            "email": created_user.email,
            "password": test_user_data["password"]
        }
        
        response = await client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data["success"] is True
        assert isinstance(data["data"], str)  # jwt token
        assert len(data["data"]) > 20  # jwt tokens are long
        assert data["data"].count(".") == 2  # jwt format
```

### 3. Complete User Journey

Testing full workflow from registration to authenticated access:

```python
@pytest.mark.functional
@pytest.mark.slow
class TestFullUserFlow:
    """test complete user workflows end-to-end"""
    
    async def test_complete_user_registration_and_login_flow(self, client: AsyncClient):
        """test full user journey from registration to authenticated access"""
        # Step 1: register new user
        registration_data = {
            "email": "fullflow@example.com",
            "password": "FullFlowPassword123",
            "first_name": "Full",
            "last_name": "Flow"
        }
        
        register_response = await client.post("/api/v1/auth/register", json=registration_data)
        assert register_response.status_code == status.HTTP_201_CREATED
        user_id = register_response.json()["data"]["id"]
        
        # Step 2: login with registered user
        login_data = {
            "email": registration_data["email"],
            "password": registration_data["password"]
        }
        
        login_response = await client.post("/api/v1/auth/login", json=login_data)
        assert login_response.status_code == status.HTTP_200_OK
        token = login_response.json()["data"]
        
        # Step 3: access protected endpoint with token
        headers = {"Authorization": f"Bearer {token}"}
        me_response = await client.get("/api/v1/users/me", headers=headers)
        assert me_response.status_code == status.HTTP_200_OK
        
        me_data = me_response.json()["data"]
        assert me_data["id"] == user_id
        assert me_data["email"] == registration_data["email"]
```

## Functional Testing Patterns

### 1. HTTP Client Setup

Use AsyncClient for making real HTTP requests:

```python
@pytest_asyncio.fixture
async def client(setup_test_db):
    """provide async http client for functional tests"""
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
```

### 2. Authentication Helper

Create utilities for authenticated requests:

```python
async def create_auth_headers(user_email: str):
    """helper to create authorization headers for testing"""
    token_data = {"email": user_email}
    token = create_access_token(token_data)
    return {"Authorization": f"Bearer {token}"}

# Usage in tests
async def test_protected_endpoint(self, client, created_user):
    headers = await create_auth_headers(created_user.email)
    response = await client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 200
```

### 3. Role-Based Access Testing

Test authorization for different user roles:

```python
@pytest.mark.functional
class TestUserEndpointsWithRoleAuth:
    """test role-based access control"""
    
    async def test_get_all_users_admin_success(self, client, created_admin):
        """test admin can get all users"""
        headers = await create_auth_headers(created_admin.email)
        
        response = await client.get("/api/v1/users/", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["success"] is True
        assert isinstance(data["data"], list)
    
    async def test_get_all_users_user_forbidden(self, client, created_user):
        """test regular user cannot get all users"""
        headers = await create_auth_headers(created_user.email)
        
        response = await client.get("/api/v1/users/", headers=headers)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
        data = response.json()
        assert data["success"] is False
        assert data["error_code"] == "ACCESS_FORBIDDEN"
```

### 4. Error Handling Testing

Test error scenarios and edge cases:

```python
@pytest.mark.functional
class TestErrorHandling:
    """test error handling in full app context"""
    
    async def test_404_endpoint(self, client):
        """test non-existent endpoint returns 404"""
        response = await client.get("/api/v1/nonexistent")
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    async def test_invalid_json_payload(self, client):
        """test invalid json in request body"""
        response = await client.post(
            "/api/v1/auth/register",
            content="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    async def test_unauthorized_access(self, client):
        """test accessing protected endpoint without auth fails"""
        response = await client.get("/api/v1/users/me")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
```

## Best Practices

### 1. Test Real User Workflows
```python
# Good: Complete user workflow
async def test_user_registration_and_profile_update(client):
    # Register user
    register_response = await client.post("/api/v1/auth/register", json=user_data)
    
    # Login
    login_response = await client.post("/api/v1/auth/login", json=login_data)
    token = login_response.json()["data"]
    
    # Update profile
    headers = {"Authorization": f"Bearer {token}"}
    update_response = await client.put("/api/v1/users/me", json=update_data, headers=headers)
    
    # Verify update
    profile_response = await client.get("/api/v1/users/me", headers=headers)
    assert profile_response.json()["data"]["first_name"] == update_data["first_name"]

# Bad: Testing isolated endpoints without context
async def test_get_user_endpoint(client):
    response = await client.get("/api/v1/users/1")
    # Missing authentication, context, etc.
```

### 2. Use Meaningful Test Data
```python
# Good: Realistic test data
user_data = {
    "email": "john.doe@company.com",
    "password": "SecurePassword123!",
    "first_name": "John",
    "last_name": "Doe",
    "role": "USER"
}

# Bad: Minimal or unrealistic data
user_data = {"email": "a@b.c", "password": "p"}
```

### 3. Test HTTP Specifics
```python
# Good: Test HTTP details
async def test_api_returns_correct_headers(client):
    response = await client.post("/api/v1/auth/register", json=user_data)
    
    assert response.status_code == 201
    assert response.headers["content-type"] == "application/json"
    assert "Set-Cookie" not in response.headers  # No session cookies

# Good: Test response format
async def test_api_response_format(client):
    response = await client.get("/api/v1/health")
    data = response.json()
    
    # Test standard response format
    assert "success" in data
    assert "data" in data
    assert "message" in data
```

### 4. Test Edge Cases
```python
async def test_register_duplicate_email(client, created_user):
    """test registration fails with duplicate email"""
    duplicate_data = {
        "email": created_user.email,  # duplicate
        "password": "AnotherPassword123",
        "first_name": "Another",
        "last_name": "User"
    }
    
    response = await client.post("/api/v1/auth/register", json=duplicate_data)
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    data = response.json()
    assert data["success"] is False
    assert data["error_code"] == "USER_ALREADY_EXISTS"
```

### 5. Test Application Health
```python
async def test_root_health_check(client):
    """test root endpoint health check"""
    response = await client.get("/")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["success"] is True
    assert data["data"]["status"] == "ok"
    assert data["message"] == "API is running"
```

## Common Pitfalls

### 1. Not Testing Complete Workflows
```python
# Bad: Testing endpoints in isolation
async def test_create_user(client):
    response = await client.post("/api/v1/users", json=user_data)
    assert response.status_code == 201

async def test_login_user(client):
    response = await client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 200

# Good: Testing complete workflow
async def test_user_registration_and_login_workflow(client):
    # Register
    register_response = await client.post("/api/v1/auth/register", json=user_data)
    assert register_response.status_code == 201
    
    # Login with registered user
    login_response = await client.post("/api/v1/auth/login", json=login_data)
    assert login_response.status_code == 200
```

### 2. Ignoring HTTP Details
```python
# Bad: Only testing data
async def test_get_user(client):
    response = await client.get("/api/v1/users/1")
    data = response.json()
    assert data["email"] == "test@example.com"

# Good: Testing HTTP behavior
async def test_get_user(client):
    response = await client.get("/api/v1/users/1")
    
    # Test HTTP response
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    
    # Test response format
    data = response.json()
    assert data["success"] is True
    assert data["data"]["email"] == "test@example.com"
```

### 3. Poor Test Isolation
```python
# Bad: Tests affecting each other
class TestUserFlow:
    user_id = None
    
    async def test_01_create_user(self, client):
        response = await client.post("/api/v1/auth/register", json=user_data)
        self.user_id = response.json()["data"]["id"]
    
    async def test_02_get_user(self, client):
        response = await client.get(f"/api/v1/users/{self.user_id}")  # Depends on test_01

# Good: Independent tests with fixtures
async def test_create_user(self, client):
    response = await client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 201

async def test_get_user(self, client, created_user):
    response = await client.get(f"/api/v1/users/{created_user.id}")
    assert response.status_code == 200
```

## Running Functional Tests

### Run All Functional Tests
```bash
pytest -m functional
```

### Run Specific Test Class
```bash
pytest tests/functional/test_user_endpoints.py::TestUserRegistration -v
```

### Run Slow Tests
```bash
pytest -m "functional and slow"
```

### Run with HTTP Logging
```bash
pytest -m functional -s --log-cli-level=DEBUG
```

### Run with Coverage
```bash
pytest -m functional --cov=app --cov-report=html
```

## Test Environment Setup

### Override Dependencies
```python
# Override database for testing
async def override_get_db():
    async with TestAsyncSessionLocal() as session:
        yield session

@pytest_asyncio.fixture
async def client(setup_test_db):
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
```

### Environment Variables
```python
# Set test environment variables
import os
os.environ["TESTING"] = "true"
os.environ["SECRET_KEY"] = "test-secret-key-for-jwt"
```

## Performance Considerations

### Keep Tests Fast
```python
# Good: Use minimal test data
async def test_pagination(client):
    # Create just enough data to test pagination
    for i in range(3):
        await client.post("/api/v1/auth/register", json=user_data)

# Bad: Excessive test data
async def test_pagination(client):
    # Creates unnecessary load
    for i in range(1000):
        await client.post("/api/v1/auth/register", json=user_data)
```

### Parallel Execution
```python
# Use pytest-xdist for parallel execution
# pytest -m functional -n auto
```

## Measuring Quality

### Coverage Metrics
- Target > 70% of user workflows covered
- Focus on critical business paths
- Test major error scenarios

### Performance Metrics
- Functional tests should complete in < 2 minutes total
- Individual tests should run in < 5 seconds
- API response times should be reasonable (< 1 second)

### Quality Metrics
- All major user workflows tested
- Authentication and authorization covered
- Error handling verified
- API contracts validated

## Functional Test Checklist

For each functional test, verify:
- [ ] Makes real HTTP requests to API
- [ ] Tests complete user workflow
- [ ] Validates HTTP status codes and headers
- [ ] Tests both success and error scenarios
- [ ] Includes authentication/authorization
- [ ] Uses realistic test data
- [ ] Has proper cleanup/isolation
- [ ] Tests API contract compliance

## Conclusion

Functional tests provide the highest level of confidence by testing your application as users would interact with it. They:

- **Validate complete workflows** from end to end
- **Test the API contract** with real HTTP requests
- **Verify authentication and authorization** work correctly
- **Catch integration issues** that unit and integration tests miss
- **Ensure the user experience** functions as expected

While slower than other test types, functional tests are essential for ensuring your API works correctly in production. They form the top of the testing pyramid and provide the ultimate validation of your application's behavior. 