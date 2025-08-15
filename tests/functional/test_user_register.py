import pytest
from httpx import AsyncClient
from fastapi import status

from app.core.security import create_access_token
from app.models.user import User, UserRole


@pytest.mark.functional
@pytest.mark.asyncio
class TestUserRegistration:
    """test user registration endpoints with full app"""

    async def test_register_user_success(self, client: AsyncClient):
        """test successful user registration"""
        user_data = {
            "email": "newuser@example.com",
            "password": "NewPassword123",
            "first_name": "New",
            "last_name": "User",
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

    # NOTE
    async def test_register_user_duplicate_email(
        self, client: AsyncClient, created_user: User
    ):
        """useful because duplication check and handle is endpoint layer"""
        user_data = {
            "email": created_user.email,  # duplicate email
            "password": "AnotherPassword123",
            "first_name": "Another",
            "last_name": "User",
        }

        response = await client.post("/api/v1/auth/register", json=user_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()

        assert data["success"] is False
        assert data["error_code"] == "USER_ALREADY_EXISTS"
        assert "already exists" in data["errors"][0]

    # NOTE
    async def test_register_user_invalid_email(self, client: AsyncClient):
        """NOT really needed or appropriate here because email validation is done in the schema, only useful if no unit level tests exists in cov"""
        user_data = {
            "email": "invalid-email",
            "password": "ValidPassword123",
            "first_name": "Test",
            "last_name": "User",
        }

        response = await client.post("/api/v1/auth/register", json=user_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        data = response.json()

        assert "email" in str(data)
