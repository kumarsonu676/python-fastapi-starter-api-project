from typing import Any
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.declarative import declarative_base

class CustomBase:
    """Base class for all database models"""
    
    # Generate __tablename__ automatically based on class name
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

# Create the base class for all models
Base = declarative_base(cls=CustomBase)