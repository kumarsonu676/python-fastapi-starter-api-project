import logging
from typing import Any, Dict, List, Optional, Union

logger = logging.getLogger(__name__)

def log_error(message: str, error: Optional[Exception] = None) -> None:
    """
    Log an error message and optionally the exception details.
    
    Args:
        message: Error message to log
        error: Optional exception object
    """
    if error:
        logger.error(f"{message}: {str(error)}")
    else:
        logger.info(message)

def format_query_params(
    params: Dict[str, Any], 
    exclude: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Format query parameters by removing None values and specific keys.
    
    Args:
        params: Dictionary of query parameters
        exclude: Optional list of keys to exclude
        
    Returns:
        Filtered dictionary of query parameters
    """
    exclude = exclude or []
    return {k: v for k, v in params.items() if v is not None and k not in exclude}

def snake_to_camel(snake_str: str) -> str:
    """
    Convert snake_case string to camelCase.
    
    Args:
        snake_str: String in snake_case format
        
    Returns:
        String in camelCase format
    """
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def camel_to_snake(camel_str: str) -> str:
    """
    Convert camelCase string to snake_case.
    
    Args:
        camel_str: String in camelCase format
        
    Returns:
        String in snake_case format
    """
    import re
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_str)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def paginate_response(
    items: List[Any], 
    total: int, 
    page: int, 
    page_size: int
) -> Dict[str, Any]:
    """
    Create a paginated response dictionary.
    
    Args:
        items: List of items for current page
        total: Total number of items
        page: Current page number
        page_size: Number of items per page
        
    Returns:
        Dictionary with pagination information
    """
    return {
        "items": items,
        "total": total,
        "page": page,
        "size": page_size,
        "pages": (total + page_size - 1) // page_size if page_size else 1
    }