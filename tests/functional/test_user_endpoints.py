import pytest
from httpx import AsyncClient
from fastapi import status

from app.core.security import create_access_token
from app.models.user import UserRole


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
        assert data["data"]["first_name"] == user_data["first_name"]
        assert data["data"]["last_name"] == user_data["last_name"]
        assert data["data"]["role"] == UserRole.USER.value
        assert data["data"]["is_active"] is True
        assert "id" in data["data"]
        assert "created_at" in data["data"]
        assert "hashed_password" not in data["data"]  # sensitive data excluded
    
    async def test_register_user_duplicate_email(self, client: AsyncClient, created_user):
        """test registration fails with duplicate email"""
        user_data = {
            "email": created_user.email,  # duplicate email
            "password": "AnotherPassword123",
            "first_name": "Another",
            "last_name": "User"
        }
        
        response = await client.post("/api/v1/auth/register", json=user_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        
        assert data["success"] is False
        assert data["error_code"] == "USER_ALREADY_EXISTS"
        assert "already exists" in data["errors"][0]
    
    async def test_register_user_invalid_email(self, client: AsyncClient):
        """test registration fails with invalid email format"""
        user_data = {
            "email": "invalid-email",
            "password": "ValidPassword123",
            "first_name": "Test",
            "last_name": "User"
        }
        
        response = await client.post("/api/v1/auth/register", json=user_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        data = response.json()
        
        assert "email" in str(data)
    
    async def test_register_user_weak_password(self, client: AsyncClient):
        """test registration fails with weak password"""
        user_data = {
            "email": "test@example.com",
            "password": "weak",  # no uppercase, no digit
            "first_name": "Test",
            "last_name": "User"
        }
        
        response = await client.post("/api/v1/auth/register", json=user_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        data = response.json()
        
        assert "password" in str(data).lower()
    
    async def test_register_user_missing_fields(self, client: AsyncClient):
        """test registration fails with missing required fields"""
        user_data = {
            "email": "test@example.com"
            # missing password, first_name, last_name
        }
        
        response = await client.post("/api/v1/auth/register", json=user_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        data = response.json()
        
        assert "password" in str(data)


@pytest.mark.functional
class TestUserAuthentication:
    """test user authentication endpoints"""
    
    async def test_login_success(self, client: AsyncClient, created_user, test_user_data):
        """test successful user login"""
        login_data = {
            "email": created_user.email,
            "password": test_user_data["password"]  # use original password
        }
        
        response = await client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data["success"] is True
        assert data["message"] == "User logged in successfully"
        assert isinstance(data["data"], str)  # jwt token
        assert len(data["data"]) > 20  # jwt tokens are long
        assert data["data"].count(".") == 2  # jwt format
    
    async def test_login_invalid_email(self, client: AsyncClient):
        """test login fails with non-existent email"""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "AnyPassword123"
        }
        
        response = await client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        data = response.json()
        
        assert data["success"] is False
        assert data["error_code"] == "INVALID_CREDENTIALS"
        assert "Invalid email or password" in data["errors"][0]
    
    async def test_login_invalid_password(self, client: AsyncClient, created_user):
        """test login fails with wrong password"""
        login_data = {
            "email": created_user.email,
            "password": "WrongPassword123"
        }
        
        response = await client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        data = response.json()
        
        assert data["success"] is False
        assert data["error_code"] == "INVALID_CREDENTIALS"
        assert "Invalid email or password" in data["errors"][0]
    
    async def test_token_endpoint_success(self, client: AsyncClient, created_user, test_user_data):
        """test oauth2 token endpoint for swagger ui"""
        form_data = {
            "username": created_user.email,  # oauth2 uses username field
            "password": test_user_data["password"]
        }
        
        response = await client.post(
            "/api/v1/auth/token",
            data=form_data,  # form data for oauth2
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert isinstance(data["access_token"], str)
        assert len(data["access_token"]) > 20


async def create_auth_headers(user_email: str):
    """helper to create authorization headers for testing"""
    token_data = {"email": user_email}
    token = create_access_token(token_data)
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.functional
class TestUserEndpointsWithAuth:
    """test user endpoints requiring authentication"""
    
    async def test_get_current_user_success(self, client: AsyncClient, created_user):
        """test getting current user info"""
        headers = await create_auth_headers(created_user.email)
        
        response = await client.get("/api/v1/users/me", headers=headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data["success"] is True
        assert data["data"]["id"] == created_user.id
        assert data["data"]["email"] == created_user.email
        assert data["data"]["first_name"] == created_user.first_name
        assert data["data"]["last_name"] == created_user.last_name
    
    async def test_get_current_user_unauthorized(self, client: AsyncClient):
        """test getting current user without auth fails"""
        response = await client.get("/api/v1/users/me")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    async def test_get_current_user_invalid_token(self, client: AsyncClient):
        """test getting current user with invalid token fails"""
        headers = {"Authorization": "Bearer invalid-token"}
        
        response = await client.get("/api/v1/users/me", headers=headers)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        data = response.json()
        
        assert data["success"] is False
        assert data["error_code"] == "INVALID_CREDENTIALS"
    
    async def test_get_user_by_id_success(self, client: AsyncClient, created_user):
        """test getting user by id with proper auth"""
        headers = await create_auth_headers(created_user.email)
        
        response = await client.get(f"/api/v1/users/{created_user.id}", headers=headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data["success"] is True
        assert data["data"]["id"] == created_user.id
        assert data["data"]["email"] == created_user.email
    
    async def test_get_user_by_id_not_found(self, client: AsyncClient, created_user):
        """test getting non-existent user returns null data"""
        headers = await create_auth_headers(created_user.email)
        
        response = await client.get("/api/v1/users/99999", headers=headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data["success"] is True
        assert data["data"] is None
    
    async def test_get_user_by_email_success(self, client: AsyncClient, created_user):
        """test getting user by email with proper auth"""
        headers = await create_auth_headers(created_user.email)
        
        response = await client.get(
            f"/api/v1/users/by-email?email={created_user.email}",
            headers=headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data["success"] is True
        assert data["data"]["id"] == created_user.id
        assert data["data"]["email"] == created_user.email
    
    async def test_get_user_by_email_not_found(self, client: AsyncClient, created_user):
        """test getting user by non-existent email"""
        headers = await create_auth_headers(created_user.email)
        
        response = await client.get(
            "/api/v1/users/by-email?email=nonexistent@example.com",
            headers=headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data["success"] is True
        assert data["data"] is None


@pytest.mark.functional
class TestUserEndpointsWithRoleAuth:
    """test role-based access control"""
    
    async def test_get_all_users_admin_success(self, client: AsyncClient, created_admin, created_user):
        """test admin can get all users"""
        headers = await create_auth_headers(created_admin.email)
        
        response = await client.get("/api/v1/users/", headers=headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data["success"] is True
        assert isinstance(data["data"], list)
        assert len(data["data"]) >= 2  # at least admin and user
        
        # find both users in response
        emails = [user["email"] for user in data["data"]]
        assert created_admin.email in emails
        assert created_user.email in emails
    
    async def test_get_all_users_user_forbidden(self, client: AsyncClient, created_user):
        """test regular user cannot get all users"""
        headers = await create_auth_headers(created_user.email)
        
        response = await client.get("/api/v1/users/", headers=headers)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        data = response.json()
        
        assert data["success"] is False
        assert data["error_code"] == "ACCESS_FORBIDDEN"
        assert "insufficient role" in data["errors"][0]
    
    async def test_get_all_users_unauthorized(self, client: AsyncClient):
        """test unauthenticated request to get all users fails"""
        response = await client.get("/api/v1/users/")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.functional
class TestAppHealthEndpoints:
    """test application health and root endpoints"""
    
    async def test_root_health_check(self, client: AsyncClient):
        """test root endpoint health check"""
        response = await client.get("/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data["success"] is True
        assert data["data"]["status"] == "ok"
        assert data["message"] == "API is running"
    
    async def test_favicon_endpoint(self, client: AsyncClient):
        """test favicon endpoint returns file"""
        response = await client.get("/favicon.ico")
        
        # should return file or appropriate response
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]


@pytest.mark.functional
class TestErrorHandling:
    """test error handling in full app context"""
    
    async def test_404_endpoint(self, client: AsyncClient):
        """test non-existent endpoint returns 404"""
        response = await client.get("/api/v1/nonexistent")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    async def test_method_not_allowed(self, client: AsyncClient):
        """test wrong http method returns 405"""
        response = await client.delete("/")  # root only supports GET
        
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
    async def test_invalid_json_payload(self, client: AsyncClient):
        """test invalid json in request body"""
        response = await client.post(
            "/api/v1/auth/register",
            content="invalid json",
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    async def test_missing_content_type(self, client: AsyncClient):
        """test request with missing content type"""
        response = await client.post("/api/v1/auth/register", content='{"test": "data"}')
        
        # fastapi should handle this gracefully
        assert response.status_code in [
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
        ]


@pytest.mark.functional
@pytest.mark.slow
class TestFullUserFlow:
    """test complete user workflows end-to-end"""
    
    async def test_complete_user_registration_and_login_flow(self, client: AsyncClient):
        """test full user journey from registration to authenticated access"""
        # step 1: register new user
        registration_data = {
            "email": "fullflow@example.com",
            "password": "FullFlowPassword123",
            "first_name": "Full",
            "last_name": "Flow"
        }
        
        register_response = await client.post("/api/v1/auth/register", json=registration_data)
        assert register_response.status_code == status.HTTP_201_CREATED
        
        user_data = register_response.json()["data"]
        user_id = user_data["id"]
        
        # step 2: login with registered user
        login_data = {
            "email": registration_data["email"],
            "password": registration_data["password"]
        }
        
        login_response = await client.post("/api/v1/auth/login", json=login_data)
        assert login_response.status_code == status.HTTP_200_OK
        
        token = login_response.json()["data"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # step 3: access protected endpoint with token
        me_response = await client.get("/api/v1/users/me", headers=headers)
        assert me_response.status_code == status.HTTP_200_OK
        
        me_data = me_response.json()["data"]
        assert me_data["id"] == user_id
        assert me_data["email"] == registration_data["email"]
        
        # step 4: access user by id
        user_response = await client.get(f"/api/v1/users/{user_id}", headers=headers)
        assert user_response.status_code == status.HTTP_200_OK
        
        fetched_user = user_response.json()["data"]
        assert fetched_user["id"] == user_id
        assert fetched_user["email"] == registration_data["email"]
    
    async def test_admin_user_workflow(self, client: AsyncClient, created_admin):
        """test admin-specific workflows"""
        # login as admin
        login_data = {
            "email": created_admin.email,
            "password": "AdminPassword123"  # from fixture
        }
        
        login_response = await client.post("/api/v1/auth/login", json=login_data)
        assert login_response.status_code == status.HTTP_200_OK
        
        token = login_response.json()["data"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # access admin-only endpoint
        users_response = await client.get("/api/v1/users/", headers=headers)
        assert users_response.status_code == status.HTTP_200_OK
        
        users_data = users_response.json()["data"]
        assert isinstance(users_data, list)
        assert len(users_data) >= 1
        
        # verify admin can access own profile
        me_response = await client.get("/api/v1/users/me", headers=headers)
        assert me_response.status_code == status.HTTP_200_OK
        
        me_data = me_response.json()["data"]
        assert me_data["role"] == UserRole.ADMIN.value 