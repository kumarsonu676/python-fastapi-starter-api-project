import pytest
from sqlalchemy import func

from app.models.user import User, UserRole
from app.repositories.user import UserRepository
from app.repositories.base import BaseRepository


@pytest.mark.integration 
class TestUserRepository:
    """test user repository database operations"""
    
    async def test_create_user(self, user_repository, test_user_data):
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
    
    async def test_get_user_by_id(self, user_repository, created_user):
        """test retrieving user by id"""
        user = await user_repository.get(created_user.id)
        
        assert user is not None
        assert user.id == created_user.id
        assert user.email == created_user.email
        assert user.first_name == created_user.first_name
    
    async def test_get_user_by_id_not_found(self, user_repository):
        """test retrieving non-existent user returns none"""
        user = await user_repository.get(99999)
        assert user is None
    
    async def test_get_user_by_email(self, user_repository, created_user):
        """test retrieving user by email"""
        user = await user_repository.get_by_email(created_user.email)
        
        assert user is not None
        assert user.id == created_user.id
        assert user.email == created_user.email
    
    async def test_get_user_by_email_case_insensitive(self, user_repository, created_user):
        """test email lookup is case insensitive"""
        # test uppercase
        user = await user_repository.get_by_email(created_user.email.upper())
        assert user is not None
        assert user.id == created_user.id
        
        # test mixed case
        mixed_case_email = "TeSt@ExAmPlE.cOm" if created_user.email == "test@example.com" else created_user.email
        if created_user.email == "test@example.com":
            user = await user_repository.get_by_email(mixed_case_email)
            assert user is not None
    
    async def test_get_user_by_email_not_found(self, user_repository):
        """test retrieving non-existent email returns none"""
        user = await user_repository.get_by_email("nonexistent@example.com")
        assert user is None
    
    async def test_update_user(self, user_repository, created_user, db_session):
        """test updating user in database"""
        update_data = {
            "first_name": "Updated",
            "last_name": "Name",
            "is_active": False
        }
        
        updated_user = await user_repository.update(
            id=created_user.id,
            obj_in=update_data
        )
        await db_session.commit()
        
        assert updated_user is not None
        assert updated_user.id == created_user.id
        assert updated_user.first_name == "Updated"
        assert updated_user.last_name == "Name"
        assert updated_user.is_active is False
        assert updated_user.email == created_user.email  # unchanged
    
    async def test_update_user_not_found(self, user_repository):
        """test updating non-existent user returns none"""
        update_data = {"first_name": "Updated"}
        result = await user_repository.update(id=99999, obj_in=update_data)
        assert result is None
    
    async def test_delete_user(self, user_repository, created_user, db_session):
        """test deleting user from database"""
        deleted_user = await user_repository.delete(id=created_user.id)
        await db_session.commit()
        
        assert deleted_user is not None
        assert deleted_user.id == created_user.id
        
        # verify user is deleted
        user = await user_repository.get(created_user.id)
        assert user is None
    
    async def test_delete_user_not_found(self, user_repository):
        """test deleting non-existent user returns none"""
        result = await user_repository.delete(id=99999)
        assert result is None


@pytest.mark.integration
class TestBaseRepository:
    """test base repository functionality with user model"""
    
    async def test_get_multi_no_filters(self, user_repository, db_session):
        """test getting multiple users without filters"""
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
    
    async def test_get_multi_with_pagination(self, user_repository, db_session):
        """test pagination in get_multi"""
        # create multiple users
        users_data = [
            {"email": f"page{i}@example.com", "hashed_password": "hash", "first_name": f"Page{i}"}
            for i in range(10)
        ]
        
        for user_data in users_data:
            await user_repository.create(obj_in=user_data)
        await db_session.commit()
        
        # get first page
        users_page1, total = await user_repository.get_multi(skip=0, limit=5)
        assert len(users_page1) == 5
        assert total == 10
        
        # get second page
        users_page2, total = await user_repository.get_multi(skip=5, limit=5)
        assert len(users_page2) == 5
        assert total == 10
        
        # ensure different users on different pages
        page1_ids = {user.id for user in users_page1}
        page2_ids = {user.id for user in users_page2}
        assert page1_ids.isdisjoint(page2_ids)
    
    async def test_get_multi_with_filters(self, user_repository, db_session):
        """test filtering in get_multi"""
        # create users with different statuses
        users_data = [
            {"email": "active1@example.com", "hashed_password": "hash", "is_active": True},
            {"email": "active2@example.com", "hashed_password": "hash", "is_active": True},
            {"email": "inactive1@example.com", "hashed_password": "hash", "is_active": False},
        ]
        
        for user_data in users_data:
            await user_repository.create(obj_in=user_data)
        await db_session.commit()
        
        # filter for active users only
        active_users, total = await user_repository.get_multi(filters={"is_active": True})
        
        assert len(active_users) == 2
        assert total == 2
        assert all(user.is_active for user in active_users)
    
    async def test_get_multi_contains_filter(self, user_repository, db_session):
        """test contains filter functionality"""
        # create users with different names
        users_data = [
            {"email": "john.doe@example.com", "hashed_password": "hash", "first_name": "John"},
            {"email": "jane.doe@example.com", "hashed_password": "hash", "first_name": "Jane"},
            {"email": "bob.smith@example.com", "hashed_password": "hash", "first_name": "Bob"},
        ]
        
        for user_data in users_data:
            await user_repository.create(obj_in=user_data)
        await db_session.commit()
        
        # search for users with "doe" in email
        doe_users, total = await user_repository.get_multi(filters={"email_contains": "doe"})
        
        assert len(doe_users) == 2
        assert total == 2
        assert all("doe" in user.email.lower() for user in doe_users)
    
    async def test_create_without_commit(self, user_repository, db_session):
        """test creating without committing transaction"""
        user_data = {
            "email": "nocommit@example.com",
            "hashed_password": "hash",
            "first_name": "NoCommit"
        }
        
        user = await user_repository.create(obj_in=user_data, commit_txn=False)
        
        # user should exist in session but not committed
        assert user is not None
        assert user.email == "nocommit@example.com"
        
        # rollback and verify user doesn't persist
        await db_session.rollback()
        
        found_user = await user_repository.get_by_email("nocommit@example.com")
        assert found_user is None
    
    async def test_update_without_commit(self, user_repository, created_user, db_session):
        """test updating without committing transaction"""
        original_name = created_user.first_name
        
        updated_user = await user_repository.update(
            id=created_user.id,
            obj_in={"first_name": "TempUpdate"},
            commit_txn=False
        )
        
        assert updated_user.first_name == "TempUpdate"
        
        # rollback and verify change doesn't persist
        await db_session.rollback()
        
        # refresh to get current state
        await db_session.refresh(created_user)
        assert created_user.first_name == original_name 