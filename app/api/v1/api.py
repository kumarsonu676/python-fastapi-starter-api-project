from fastapi import APIRouter

from app.api.v1.endpoints import health
from app.api.v1.endpoints import users
from app.api.v1.endpoints import auth

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# This is the main API router that includes all endpoint routers