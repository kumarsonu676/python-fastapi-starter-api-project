import pytest
from httpx import AsyncClient
from fastapi import status


@pytest.mark.functional
class TestAppHealth:
    # basic app stuff
    async def test_root_health_check(self, client: AsyncClient):
        response = await client.get("/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["success"] is True
        assert data["data"]["status"] == "ok"
        assert data["message"] == "API is running"


@pytest.mark.functional
class TestErrorHandling:
    # NOTE
    """
    not that useful since we mostly want to test our own logic and not fastapi
    but can be done for a completer test suite
    """

    async def test_404_endpoint(self, client: AsyncClient):
        response = await client.get("/api/v1/nonexistent")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_method_not_allowed(self, client: AsyncClient):
        response = await client.delete("/")  # root only supports GET
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    async def test_invalid_json_payload(self, client: AsyncClient):
        response = await client.post(
            "/api/v1/auth/register",
            content="invalid json",
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_missing_content_type(self, client: AsyncClient):
        response = await client.post(
            "/api/v1/auth/register", content='{"test": "data"}'
        )
        # fastapi should handle this gracefully
        assert response.status_code in [
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        ]
