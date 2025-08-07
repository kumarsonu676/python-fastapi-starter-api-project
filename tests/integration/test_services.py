import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User
from app.core.security import verify_password


@pytest.mark.integration
class TestUserService:
    async def test_create_user_password_hashing(
        self,
        user_service: UserService,
        test_user_data: dict[str, str],
        db_session: AsyncSession,
    ) -> None:
        user_create = UserCreate(**test_user_data)
        user = await user_service.create(user_create)
        await db_session.commit()

        # verify password is hashed and original is not stored
        assert user.hashed_password is not None
        assert user.hashed_password != test_user_data["password"]
        assert len(user.hashed_password) > 20  # bcrypt hash length
        assert user.hashed_password.startswith("$2b$")

        # verify password verification works
        assert verify_password(test_user_data["password"], user.hashed_password) is True
        assert verify_password("wrongpassword", user.hashed_password) is False

    async def test_get_all_users(
        self, user_service: UserService, db_session: AsyncSession
    ) -> None:
        # create multiple users
        users_data = [
            {
                "email": f"bulk{i}@example.com",
                "password": "Password123",
                "first_name": f"User{i}",
            }
            for i in range(9)
        ]

        for user_data in users_data:
            user_create = UserCreate(**user_data)
            await user_service.create(user_create)
        await db_session.commit()

        all_users = await user_service.get_all_users()

        assert len(all_users) == 9
        assert all(user.email.startswith("bulk") for user in all_users)

    async def test_update_user_password_handling(
        self, user_service: UserService, created_user: User, db_session: AsyncSession
    ) -> None:
        new_password = "NewPassword123"
        update_data = {"password": new_password}

        updated_user = await user_service.update(created_user.id, update_data)
        await db_session.commit()

        # verify password was properly hashed and updated
        assert updated_user is not None
        assert updated_user.hashed_password is not None
        assert updated_user.hashed_password != new_password  # should be hashed
        assert updated_user.hashed_password.startswith("$2b$")  # bcrypt hash format
        # verify new password works
        assert verify_password(new_password, updated_user.hashed_password)

    async def test_update_user_ignore_none_values(
        self, user_service: UserService, created_user: User, db_session: AsyncSession
    ) -> None:
        original_first_name = created_user.first_name

        update_data = UserUpdate(first_name=None, last_name="ValidUpdate")

        updated_user = await user_service.update(created_user.id, update_data)
        await db_session.commit()

        assert updated_user is not None
        assert updated_user.first_name == original_first_name  # unchanged due to none
        assert updated_user.last_name == "ValidUpdate"
