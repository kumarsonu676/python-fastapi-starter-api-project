from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator

from app.models.user import UserRole

class UserBase(BaseModel):
    """Base User Schema with common attributes"""
    email: EmailStr
    role: Optional[str] = "USER"
    first_name: Optional[str] = Field(None, min_length=2, max_length=50, description="First name of the user")
    last_name: Optional[str] = Field(None, min_length=2, max_length=50, description="Last name of the user")
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    """Schema for creating a new user"""
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: Optional[str] = UserRole.USER.value

    @validator('password')
    def password_strength(cls, v):
        """Validate password strength"""
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        return v

class UserUpdate(BaseModel):
    """Schema for updating user information"""
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, min_length=2, max_length=50)
    is_active: Optional[bool] = None

class UserLogin(BaseModel):
    """Schema for user login"""
    email: str
    password: str

    # email required check
    @validator('email')
    def email_required(cls, v):
        """Validate email for required"""
        if not v:
            raise ValueError('Email is required')
        return v

    @validator('password')
    def password_required(cls, v):
        """Validate password for required"""
        if not v:
            raise ValueError('Password is required')
        return v

class UserResponse(UserBase):
    """Schema for user response"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True