from sqlalchemy import Boolean, Column, DateTime, Integer, String, func, Enum
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base


class UserRole(enum.Enum):
    ADMIN = "ADMIN"
    USER = "USER"

class User(Base):
    """User model for database"""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(300), unique=True, index=True)
    hashed_password: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(300), index=True, nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(300), index=True, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    role: Mapped[Optional[str]] = mapped_column(String(20), default=UserRole.USER.value, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())