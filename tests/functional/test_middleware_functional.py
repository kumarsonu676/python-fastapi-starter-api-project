import pytest
import pytest_asyncio
from httpx import AsyncClient
from fastapi import status


@pytest.mark.functional
class TestClientIdMiddlewareFunctional:
    """functional tests for client id middleware in full app context"""

    async def test_middleware_blocks_request_without_client_id(
        self, client: AsyncClient
    ):
        """test middleware blocks api requests without client id header"""
        # client fixture already includes X-Client-ID, so create new client without it
        from app.main import app

        async with AsyncClient(app=app, base_url="http://test") as test_client:
            response = await test_client.get("/api/v1/users/me")

            assert response.status_code == status.HTTP_401_UNAUTHORIZED
            data = response.json()

            assert data["success"] is False
            assert data["message"] == "Missing X-Client-ID header"

    async def test_middleware_allows_excluded_paths(self, client: AsyncClient):
        """test middleware allows excluded paths without client id"""
        from app.main import app

        async with AsyncClient(app=app, base_url="http://test") as test_client:
            # test various excluded paths
            excluded_paths = ["/", "/favicon.ico", "/api/v1/docs", "/api/v1/health"]

            for path in excluded_paths:
                response = await test_client.get(path)

                # should not get client id error (401/403)
                # may get 404 or 200 depending on path, but not client id errors
                assert response.status_code not in [
                    401,
                    403,
                ], f"Path {path} blocked by client id middleware"

    async def test_middleware_with_registration_endpoint(self, client: AsyncClient):
        """test middleware works with user registration"""
        user_data = {
            "email": "middleware_test@example.com",
            "password": "TestPassword123",
            "first_name": "Middleware",
            "last_name": "Test",
        }

        # should work with valid client id
        response = await client.post("/api/v1/auth/register", json=user_data)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["success"] is True
        assert data["data"]["email"] == user_data["email"]
