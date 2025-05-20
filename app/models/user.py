from sqlalchemy import Boolean, Column, DateTime, Integer, String, func, Enum
from sqlalchemy.orm import relationship
import enum
from app.db.base_class import Base

class UserRole(enum.Enum):
    ADMIN = "ADMIN"
    USER = "USER"

class User(Base):
    """User model for database"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(300), unique=True, index=True, nullable=False)
    hashed_password = Column(String(300), nullable=True)
    first_name = Column(String(300), index=True)
    last_name = Column(String(300), index=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    role = Column(String(20), default=UserRole.USER.value, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())