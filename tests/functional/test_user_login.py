import pytest
from httpx import AsyncClient
from fastapi import status

from app.core.security import create_access_token
from app.models.user import User, UserRole


@pytest.mark.functional
@pytest.mark.asyncio
class TestUserAuthentication:
    """test user authentication endpoints"""

    async def test_login_success(
        self, client: AsyncClient, created_user: User, test_user_data
    ):
        """test successful user login"""
        login_data = {
            "email": created_user.email,
            "password": test_user_data["password"],  # use original password
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
        login_data = {"email": "nonexistent@example.com", "password": "AnyPassword123"}

        response = await client.post("/api/v1/auth/login", json=login_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        data = response.json()

        assert data["success"] is False
        assert data["error_code"] == "INVALID_CREDENTIALS"
        assert "Invalid email or password" in data["errors"][0]

    async def test_login_invalid_password(
        self, client: AsyncClient, created_user: User
    ):
        """test login fails with wrong password"""
        login_data = {"email": created_user.email, "password": "WrongPassword123"}

        response = await client.post("/api/v1/auth/login", json=login_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        data = response.json()

        assert data["success"] is False
        assert data["error_code"] == "INVALID_CREDENTIALS"
        assert "Invalid email or password" in data["errors"][0]
