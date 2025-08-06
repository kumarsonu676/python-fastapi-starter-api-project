from typing import List, Optional, Union

from app.core.security import get_password_hash
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class UserService:    

    def __init__(self, db: AsyncSession, user_repo: UserRepository):
        """Initialize with user repository"""
        self.db = db
        self.user_repo = user_repo

    async def get(self, user_id: int) -> Optional[User]:
        """Get a user by ID"""
        result = await self.user_repo.get(user_id)
        return result

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by email"""
        result = await self.user_repo.get_by_email(email)
        return result

    async def get_all_users(self) -> List[User]:
        """Get all users"""
        users, _ = await self.user_repo.get_multi()
        return users

    async def create(self, obj_in: UserCreate) -> User:
        """Create a new user"""
        hashed_password = get_password_hash(obj_in.password)        

        # Create user object
        db_obj = obj_in.dict()
        db_obj["hashed_password"] = hashed_password

        # Remove password field as we don't store it directly
        if "password" in db_obj:
            del db_obj["password"]

        return await self.user_repo.create(obj_in=db_obj)

    async def update(self, user_id: int, obj_in: Union[UserUpdate, dict]) -> Optional[User]:
        """Update a user"""
        # Get current user
        db_obj = await self.user_repo.get(user_id)
        if not db_obj:
            return None

        # Convert to dict if it's a Pydantic model
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.dict(exclude_unset=True)

        # Update user attributes
        for field, value in update_data.items():
            if field != "password" and hasattr(db_obj, field) and value is not None:
                setattr(db_obj, field, value)

        # Handle password update separately
        if "password" in update_data and update_data["password"]:
            db_obj.hashed_password = update_data["password"]
        
        return await self.user_repo.update(db_obj)

    async def delete(self, user_id: int) -> Optional[User]:
        """Delete a user"""
        db_obj = await self.user_repo.get(user_id)
        if not db_obj:
            return None

        await self.user_repo.delete(id=user_id)

        return db_obj