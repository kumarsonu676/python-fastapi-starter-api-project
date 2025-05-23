from typing import Dict, Generic, List, Optional, Type, TypeVar, Any, Tuple
from sqlalchemy import func, select, update, delete, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Any)

class BaseRepository(Generic[ModelType]):
    """
    Base repository with common database operations.
    
    Generic repository that provides basic CRUD operations for SQLAlchemy models.
    """
    
    def __init__(self, db: AsyncSession, model: Type[ModelType]):
        """
        Initialize the repository with database session and model class.
        
        Args:
            db: SQLAlchemy async session
            model: SQLAlchemy model class
        """
        self.db = db
        self.model = model
    
    async def get(self, id: Any) -> Optional[ModelType]:
        """
        Get a record by ID.
        
        Args:
            id: Record ID
            
        Returns:
            Record if found, None otherwise
        """
        query = select(self.model).where(self.model.id == id)
        result = await self.db.execute(query)
        return result.scalars().first()
    
    async def get_multi(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        filters: Dict[str, Any] = None
    ) -> Tuple[List[ModelType], int]:
        """
        Get multiple records with pagination and filtering.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            filters: Optional filters dictionary
            
        Returns:
            Tuple of (list of records, total count)
        """
        # Create base query
        query = select(self.model)
        
        # Apply filters if provided
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field) and value is not None:
                    # Handle special case for search fields
                    if field.endswith("_contains") and value:
                        field_name = field.replace("_contains", "")
                        if hasattr(self.model, field_name):
                            query = query.where(getattr(self.model, field_name).ilike(f"%{value}%"))
                    # Handle boolean fields
                    elif isinstance(value, bool):
                        query = query.where(getattr(self.model, field) == value)
                    # Handle list values (IN operator)
                    elif isinstance(value, list):
                        query = query.where(getattr(self.model, field).in_(value))
                    # Default exact match
                    else:
                        query = query.where(getattr(self.model, field) == value)
        
        # Count total records
        count_query = select(func.count()).select_from(query.subquery())
        total = await self.db.execute(count_query)
        total = total.scalar_one()
        
        # Apply pagination
        query = query.offset(skip).limit(limit)
        
        # Execute query
        result = await self.db.execute(query)
        items = result.scalars().all()
        
        return items, total
    
    async def create(self, *, obj_in: Dict[str, Any], commit_txn: Optional[bool] = True) -> ModelType:
        """
        Create a new record.
        
        Args:
            obj_in: Dictionary with field values
            commit_txn: Whether to commit the transaction

        Returns:
            Created record
        """
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)

        if commit_txn and commit_txn == True:
            await self.db.commit()
            await self.db.refresh(db_obj)

        return db_obj

    async def update(
        self,
        *,
        id: Any,
        obj_in: Dict[str, Any], 
        commit_txn: Optional[bool] = True
    ) -> Optional[ModelType]:
        """
        Update a record by ID.
        
        Args:
            id: Record ID
            obj_in: Dictionary with field values to update
            
        Returns:
            Updated record if found, None otherwise
        """
        # Check if record exists
        db_obj = await self.get(id)
        if db_obj is None:
            return None
        
        # Update fields
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
                
        if commit_txn and commit_txn == True:
            await self.db.commit()
            await self.db.refresh(db_obj)

        return db_obj
    
    async def delete(self, *, id: Any, commit_txn: Optional[bool] = True) -> Optional[ModelType]:
        """
        Delete a record by ID.
        
        Args:
            id: Record ID
            
        Returns:
            Deleted record if found, None otherwise
        """
        # Check if record exists
        db_obj = await self.get(id)
        if db_obj is None:
            return None
        
        await self.db.delete(db_obj)

        if commit_txn and commit_txn == True:
            await self.db.commit()

        return db_obj