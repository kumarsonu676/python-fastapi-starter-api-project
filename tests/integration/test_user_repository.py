import pytest
import pytest_asyncio
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserRole
from app.repositories.user import UserRepository
from app.repositories.base import BaseRepository


@pytest.mark.integration
class TestUserRepository:
    """test user repository database operations"""

    async def test_create_user(
        self, user_repository: UserRepository, test_user_data: dict
    ):
        """test creating user in database"""
        user_data = test_user_data.copy()
        del user_data["password"]  # repository doesn't handle password
        user_data["hashed_password"] = "hashed_password_value"

        user = await user_repository.create(obj_in=user_data)

        assert user is not None
        assert user.id is not None
        assert user.email == test_user_data["email"]
        assert user.first_name == test_user_data["first_name"]
        assert user.last_name == test_user_data["last_name"]
        assert user.role == test_user_data["role"]
        assert user.hashed_password == "hashed_password_value"
        assert user.is_active is True
        assert user.is_verified is False
        assert user.created_at is not None

    async def test_get_user_by_id(
        self, user_repository: UserRepository, created_user: User
    ):
        """test retrieving user by id"""
        user = await user_repository.get(created_user.id)

        assert user is not None
        assert user.id == created_user.id
        assert user.email == created_user.email
        assert user.first_name == created_user.first_name

    async def test_get_user_by_id_not_found(self, user_repository: UserRepository):
        """test retrieving non-existent user returns none"""
        user = await user_repository.get(99999)
        assert user is None

    async def test_get_user_by_email(
        self, user_repository: UserRepository, created_user: User
    ):
        """test retrieving user by email"""
        user = await user_repository.get_by_email(created_user.email)

        assert user is not None
        assert user.id == created_user.id
        assert user.email == created_user.email

    async def test_get_user_by_email_case_insensitive(
        self, user_repository: UserRepository, created_user: User
    ):
        """test email lookup is case insensitive"""
        # test uppercase
        user = await user_repository.get_by_email(created_user.email.upper())
        assert user is not None
        assert user.id == created_user.id

        # test mixed case
        mixed_case_email = (
            "TeSt@ExAmPlE.cOm"
            if created_user.email == "test@example.com"
            else created_user.email
        )
        if created_user.email == "test@example.com":
            user = await user_repository.get_by_email(mixed_case_email)
            assert user is not None

    async def test_get_user_by_email_not_found(self, user_repository: UserRepository):
        """test retrieving non-existent email returns none"""
        user = await user_repository.get_by_email("nonexistent@example.com")
        assert user is None

    async def test_update_user(
        self,
        user_repository: UserRepository,
        created_user: User,
        db_session: AsyncSession,
    ):
        """test updating user in database"""
        update_data = {"first_name": "Updated", "last_name": "Name", "is_active": False}

        updated_user = await user_repository.update(
            id=created_user.id, obj_in=update_data
        )
        await db_session.commit()

        assert updated_user is not None
        assert updated_user.id == created_user.id
        assert updated_user.first_name == "Updated"
        assert updated_user.last_name == "Name"
        assert updated_user.is_active is False
        assert updated_user.email == created_user.email  # unchanged

    async def test_update_user_not_found(self, user_repository: UserRepository):
        """test updating non-existent user returns none"""
        update_data = {"first_name": "Updated"}
        result = await user_repository.update(id=99999, obj_in=update_data)
        assert result is None

    async def test_delete_user(
        self,
        user_repository: UserRepository,
        created_user: User,
        db_session: AsyncSession,
    ):
        """test deleting user from database"""
        deleted_user = await user_repository.delete(id=created_user.id)
        await db_session.commit()

        assert deleted_user is not None
        assert deleted_user.id == created_user.id

        # verify user is deleted
        user = await user_repository.get(created_user.id)
        assert user is None

    async def test_delete_user_not_found(self, user_repository: UserRepository):
        """test deleting non-existent user returns none"""
        result = await user_repository.delete(id=99999)
        assert result is None
