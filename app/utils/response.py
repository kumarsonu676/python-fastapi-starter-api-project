import json
from fastapi.responses import JSONResponse
from typing import Any, Dict, Optional, TypeVar, List
from app.dtos.custom_response_dto import CustomResponse
from fastapi.encoders import jsonable_encoder

T = TypeVar('T')

def create_response(
    data: Optional[T] = None,
    message: Optional[str] = None,
    errors: Optional[List[str]] = None,
    error_code: Optional[str] = None,
    success: bool = True,
    status_code: int = 200,
):
    response = CustomResponse[T](
        success=success,
        data=data,
        message=message,
        errors=errors,
        error_code=error_code
    )
    return JSONResponse(status_code=status_code, content=jsonable_encoder(response))