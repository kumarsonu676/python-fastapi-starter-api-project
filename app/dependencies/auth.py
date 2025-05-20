from typing import List, Optional
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.security import verify_token
from app.core.config import settings
from app.dependencies.services import get_user_service
from app.exceptions.http_exceptions import BadRequestError, UnauthorizedError
from app.schemas.user import UserResponse
from app.services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),    
    user_service: UserService = Depends(get_user_service)
):
    """
    Get the current authenticated user from the token.    
    
    Args:
        token: JWT access token
        user_service: User service for database operations

    Returns:
        Current authenticated user
        
    Raises:
        UnauthorizedError: If authentication fails
    """
    payload = verify_token(token)
    if payload is None:
        raise UnauthorizedError(
            error_code="INVALID_CREDENTIALS",
            detail="Could not validate credentials"
        )

    user = await user_service.get_by_email(payload.get("email"))
    if user is None:
        raise UnauthorizedError(
            error_code="INVALID_CREDENTIALS",
            detail="Could not validate credentials"
        )
    
    return user


async def get_current_active_user(current_user: UserResponse = Depends(get_current_user)):
    """
    Get the current active user from the token.
    Args:
        current_user: Current authenticated user
    Returns:
        Current active user
    Raises:
        BadRequestError: If the user is inactive
    """
    if current_user.is_active is False:
        raise BadRequestError(
            error_code="INACTIVE_USER",
            detail="Inactive user"
        )
    
    #delete hashed_password
    del current_user.hashed_password
    
    return current_user



# Usage example:

# @router.get("/admin")
# async def read_admin_data(current_user: UserResponse = Depends(authorize(allowed_roles=["admin"]))):
#     return {"message": "Welcome, admin!"}
#

# @router.get("/user")
# async def read_user_data(current_user: UserResponse = Depends(authorize(allowed_roles=["user"]))):
#     return {"message": "Welcome, user!"}

#multiple roles
# @router.get("/admin_or_user")
# async def read_admin_or_user_data(current_user: UserResponse = Depends(authorize(allowed_roles=["admin", "user"]))):
#     return {"message": "Welcome, admin or user!"}

# @router.get("/any")
# async def read_any_data(current_user: UserResponse = Depends(authorize())):
#     return {"message": "Welcome, any authenticated user!"}

# This allows you to specify which roles are allowed to access certain endpoints.
# You can also create a route that is accessible to any authenticated user by not passing any roles to the authorize function.
def authorize(allowed_roles: Optional[List[str]] = None):
    """
    Dependency for role-based access control.
    If no roles are provided, any authenticated active user is allowed.
    """
    def role_checker(current_user: UserResponse = Depends(get_current_active_user)):
        if allowed_roles:
            user_role = current_user.role
            if user_role not in allowed_roles:
                raise UnauthorizedError(
                    error_code="ACCESS_FORBIDDEN",
                    detail="Access forbidden: insufficient role"
                )
            
        return current_user

    return role_checker