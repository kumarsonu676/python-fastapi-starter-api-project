from typing import Any, Dict, List, Optional, Union
import os
import secrets
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

class Settings:
    """Application settings"""

    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    SECRET_KEY: str = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 24 * 8))  # 8 days
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    JWT_AUDIENCE: str = os.getenv("JWT_AUDIENCE", "*")
    JWT_ISSUER: str = os.getenv("JWT_ISSUER", "http://localhost:8000")

    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    def __init__(self):
        cors_origins = os.getenv("BACKEND_CORS_ORIGINS", "*")
        if cors_origins != "*":
            if cors_origins.startswith("[") and cors_origins.endswith("]"):
                # Parse JSON-formatted list
                import json
                self.BACKEND_CORS_ORIGINS = json.loads(cors_origins)
            else:
                # Parse comma-separated list
                self.BACKEND_CORS_ORIGINS = [i.strip() for i in cors_origins.split(",")]

    # Database settings
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "app")
    
    CLIENT_IDS: str = os.getenv("CLIENT_IDS", "")
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        """Construct database URI from components using standard psycopg2"""
        # Using synchronous driver for Python 3.13 compatibility
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"

settings = Settings()