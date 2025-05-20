from typing import Any, Dict, Generic, List, Optional, TypeVar, Union
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from datetime import datetime

T = TypeVar('T')

class PaginatedResponse(GenericModel, Generic[T]):
    """
    Generic paginated response schema.
    
    This schema is used for API responses that return paginated lists of items.
    """
    items: List[T]
    total: int
    page: int
    size: int
    pages: int