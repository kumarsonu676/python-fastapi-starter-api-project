import pytest
from unittest.mock import AsyncMock, patch

from app.services.user_service import UserService
from app.schemas.user import UserCreate


@pytest.mark.unit
class TestUserServiceWithMocks:
    """test user service with mocked dependencies for isolation"""

    async def test_create_user_repository_interaction(self, db_session):
        """test service properly calls repository during creation"""
        # create mock repository
        mock_repo = AsyncMock()
        mock_user = AsyncMock()
        mock_user.id = 1
        mock_user.email = "test@example.com"
        mock_repo.create.return_value = mock_user

        service = UserService(db_session, mock_repo)
        user_create = UserCreate(
            email="test@example.com",
            password="TestPassword123",
            first_name="Test",
            last_name="User",
        )

        result = await service.create(user_create)

        # verify repository create was called
        mock_repo.create.assert_called_once()
        call_args = mock_repo.create.call_args

        # verify password was hashed and removed
        obj_in = call_args.kwargs["obj_in"]
        assert "password" not in obj_in
        assert "hashed_password" in obj_in
        assert obj_in["hashed_password"] != "TestPassword123"
        assert obj_in["email"] == "test@example.com"

        assert result == mock_user

    async def test_get_user_repository_delegation(self, db_session):
        """test service delegates get operations to repository"""
        mock_repo = AsyncMock()
        mock_user = AsyncMock()
        mock_repo.get.return_value = mock_user
        mock_repo.get_by_email.return_value = mock_user
        mock_repo.get_multi.return_value = ([mock_user], 1)

        service = UserService(db_session, mock_repo)

        # test get by id
        result = await service.get(1)
        mock_repo.get.assert_called_once_with(1)
        assert result == mock_user

        # test get by email
        result = await service.get_by_email("test@example.com")
        mock_repo.get_by_email.assert_called_once_with("test@example.com")
        assert result == mock_user

        # test get all users
        result = await service.get_all_users()
        mock_repo.get_multi.assert_called_once()
        assert result == [mock_user]

    @patch("app.services.user_service.get_password_hash")
    async def test_create_user_password_hashing_called(self, mock_hash, db_session):
        """test password hashing function is called during creation"""
        mock_hash.return_value = "hashed_password_value"
        mock_repo = AsyncMock()
        mock_user = AsyncMock()
        mock_repo.create.return_value = mock_user

        service = UserService(db_session, mock_repo)
        user_create = UserCreate(
            email="test@example.com",
            password="PlainPassword123",
            first_name="Test",
            last_name="User",
        )

        await service.create(user_create)

        # verify password hashing was called
        mock_hash.assert_called_once_with("PlainPassword123")

        # verify hashed password was passed to repository
        call_args = mock_repo.create.call_args
        obj_in = call_args.kwargs["obj_in"]
        assert obj_in["hashed_password"] == "hashed_password_value"
