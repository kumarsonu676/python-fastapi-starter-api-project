from typing import TypeVar, Generic, Optional, List
from pydantic.generics import GenericModel

# Generic type for your data
T = TypeVar('T')

class CustomResponse(GenericModel, Generic[T]):
    success: bool = True
    data: Optional[T] = None
    message: Optional[str] = None
    errors: Optional[List[str]] = None
    error_code: Optional[str] = None