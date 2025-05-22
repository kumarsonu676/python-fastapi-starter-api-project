from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import create_access_token, verify_password
from app.dependencies.services import get_user_service
from app.dtos.custom_response_dto import CustomResponse
from app.exceptions.http_exceptions import BadRequestError, UnauthorizedError
from app.models.user import UserRole
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.user_service import UserService
from app.utils.response import create_response

router = APIRouter()

@router.post(
    "/register",
    response_model=CustomResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user with the provided details"
)
async def create_user(
    user_in: UserCreate,
    user_service: UserService = Depends(get_user_service)
) -> CustomResponse[UserResponse]:
    
    existing_user = await user_service.get_by_email(user_in.email)

    if existing_user:
        raise BadRequestError(
            error_code="USER_ALREADY_EXISTS",
            detail="User with this email already exists"            
        )

    user_in.role = UserRole.USER.value
    user = await user_service.create(user_in)
    return create_response(
        data=UserResponse.from_orm(user),
        message="User created successfully",
        status_code=status.HTTP_201_CREATED
    )

# login
@router.post(
    "/login",
    response_model=CustomResponse[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Login a user",
    description="Login a user with the provided credentials"
)
async def login_user(
    user_in: UserLogin,
    user_service: UserService = Depends(get_user_service)
) -> CustomResponse[str]:
    user = await user_service.get_by_email(user_in.email)

    if not user or not verify_password(user_in.password, user.hashed_password):
        raise UnauthorizedError(
            error_code="INVALID_CREDENTIALS",
            detail="Invalid email or password"
        )
    
    user_dict = {
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name
    }

    token = create_access_token(data=user_dict)

    return create_response(
        data=token,
        message="User logged in successfully",
        status_code=status.HTTP_200_OK
    )


@router.post("/token")
async def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserService = Depends(get_user_service)
):
    user = await user_service.get_by_email(form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise UnauthorizedError(
            error_code="INVALID_CREDENTIALS",
            detail="Invalid email or password"
        )
    
    user_dict = {
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name
    }

    token = create_access_token(data=user_dict)

    return {"access_token": token, "token_type": "bearer"}