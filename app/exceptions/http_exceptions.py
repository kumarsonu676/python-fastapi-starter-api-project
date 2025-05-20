from fastapi import status

class BaseCustomError(Exception):
    """Base class for all custom exceptions"""
    def __init__(self, detail: str, status_code: int, error_code: str = None):
        self.detail = detail
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.detail)

class NotFoundError(BaseCustomError):
    """Exception raised when resource is not found"""
    def __init__(self, detail: str = "Resource not found", error_code: str = "NOT_FOUND"):
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND, error_code=error_code)

class ConflictError(BaseCustomError):
    """Exception raised when there's a resource conflict"""
    def __init__(self, detail: str = "Resource conflict", error_code: str = "CONFLICT"):
        super().__init__(detail=detail, status_code=status.HTTP_409_CONFLICT, error_code=error_code)

class UnauthorizedError(BaseCustomError):
    """Exception raised for authentication failures"""
    def __init__(self, detail: str = "Unauthorized", headers: dict = None, error_code: str = "UNAUTHORIZED"):
        self.headers = headers or {}
        super().__init__(detail=detail, status_code=status.HTTP_401_UNAUTHORIZED, error_code=error_code)

class ForbiddenError(BaseCustomError):
    """Exception raised for permission issues"""
    def __init__(self, detail: str = "Forbidden", error_code: str = "FORBIDDEN"):
        super().__init__(detail=detail, status_code=status.HTTP_403_FORBIDDEN, error_code=error_code)

class BadRequestError(BaseCustomError):
    """Exception raised for invalid requests"""
    def __init__(self, detail: str = "Bad request", error_code: str = "BAD_REQUEST"):
        super().__init__(detail=detail, status_code=status.HTTP_400_BAD_REQUEST, error_code=error_code)

class ServerError(BaseCustomError):
    """Exception raised for server errors"""
    def __init__(self, detail: str = "Internal server error", error_code: str = "SERVER_ERROR"):
        super().__init__(detail=detail, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error_code=error_code)