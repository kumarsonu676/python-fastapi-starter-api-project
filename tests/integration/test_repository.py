import pytest
import pytest_asyncio
import uuid
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user import UserRepository
from app.models.user import User, UserRole


@pytest_asyncio.fixture
async def populated_repository(self, user_repository: UserRepository, db_session: AsyncSession) -> tuple[UserRepository, list[Any]]:
    # create some variatio of users
    test_users = [
        {
            "email": f"alice.smith@techcorp.com",
            "hashed_password": "hash1",
            "first_name": "Alice",
            "last_name": "Smith",
            "role": UserRole.USER,
            "is_active": True
        },
        {
            "email": f"bob.jones@techcorp.com", 
            "hashed_password": "hash2",
            "first_name": "Bob",
            "last_name": "Jones",
            "role": UserRole.ADMIN,
            "is_active": True
        },
        {
            "email": f"charlie.brown@startup.io",
            "hashed_password": "hash3", 
            "first_name": "Charlie",
            "last_name": "Brown",
            "role": UserRole.USER,
            "is_active": False
        }
    ]
    
    created_users = []
    for user_data in test_users:
        user = await user_repository.create(obj_in=user_data)
        created_users.append(user)
    
    await db_session.commit()
    return user_repository, created_users


@pytest.mark.integration
class TestBaseRepository:
    """test base repository functionality with user model"""
    

    async def test_get_multi_no_filters(self, user_repository: UserRepository, db_session: AsyncSession):
        # create multiple users
        users_data = [
            {"email": f"user{i}@example.com", "hashed_password": "hash", "first_name": f"User{i}"}
            for i in range(5)
        ]
        
        for user_data in users_data:
            await user_repository.create(obj_in=user_data)
        await db_session.commit()
        
        users, total = await user_repository.get_multi()
        
        assert len(users) == 5
        assert total == 5
        assert all(user.email.startswith("user") for user in users)

    async def test_contains_filter(self, populated_repository: tuple[UserRepository, list[Any]], db_session):
        """test contains filter works case insensitively"""
        user_repository, created_users = populated_repository
        
        # search for "TECHCORP" (uppercase) should match "techcorp.com" emails
        users, total = await user_repository.get_multi(
            filters={"email_contains": "TECHCORP"}
        )
        
        assert total == 2  # alice, bob from techcorp.com
        assert len(users) == 2
        
        # verify all returned users have techcorp in email
        for user in users:
            assert "techcorp" in user.email.lower()

    async def test_combined_filters(self, populated_repository: tuple[UserRepository, list[Any]], db_session):
        """test multiple filters applied together"""
        user_repository, created_users = populated_repository
        
        # get active admin users
        users, total = await user_repository.get_multi(
            filters={
                "is_active": True,
                "role": UserRole.ADMIN
            }
        )
        
        assert total == 1  # only bob is active admin
        assert len(users) == 1
        
        for user in users:
            assert user.is_active is True
            assert user.role == UserRole.ADMIN

    async def test_pagination_with_filters(self, populated_repository: tuple[UserRepository, list[Any]], db_session):
        """test pagination works correctly with filters"""
        user_repository, created_users = populated_repository
        
        # get first 1 active user
        page1_users, total = await user_repository.get_multi(
            skip=0,
            limit=1,
            filters={"is_active": True}
        )
        
        assert total == 2  # total active users (alice, bob)
        assert len(page1_users) == 1  # but only 1 returned due to limit
        
        # get next page
        page2_users, total = await user_repository.get_multi(
            skip=1,
            limit=1,
            filters={"is_active": True}
        )
        
        assert total == 2  # total still 2
        assert len(page2_users) == 1  # 1 remaining user
        
        # verify no overlap between pages
        page1_ids = {user.id for user in page1_users}
        page2_ids = {user.id for user in page2_users}
        assert page1_ids.isdisjoint(page2_ids) 