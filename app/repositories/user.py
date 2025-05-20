from typing import Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base import BaseRepository

class UserRepository(BaseRepository[User]):
    """Repository for user-related database operations"""
    
    def __init__(self, db: AsyncSession):
        """
        Initialize the repository with database session.
        
        Args:
            db: SQLAlchemy async session
        """
        super().__init__(db, User)
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Get a user by email.
        
        Args:
            email: User email address
            
        Returns:
            User if found, None otherwise
        """
        # Perform a query to find the user by email
        # make case insensitive        
        query = select(User).where(func.lower(User.email) == email.lower())
        result = await self.db.execute(query)
        return result.scalars().first()