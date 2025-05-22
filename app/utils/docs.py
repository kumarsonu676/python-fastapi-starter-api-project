from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from starlette.responses import HTMLResponse
from fastapi.openapi.utils import get_openapi
from app.core.config import settings

def setup_swagger_documentation(app: FastAPI, api_prefix: str) -> None:
    """
    Set up custom Swagger and ReDoc documentation endpoints.
    
    Args:
        app: FastAPI application
        api_prefix: API prefix for documentation endpoints
    """

    # Override OpenAPI schema
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        
        openapi_schema = get_openapi(
            title="FastAPI Application",
            version="1.0.0",
            description="FastAPI application with SQLAlchemy and PostgreSQL",
            routes=app.routes
        )
        # Add global parameter
        for path in openapi_schema["paths"].values():
            for method in path.values():
                parameters = method.get("parameters", [])
                parameters.append({
                    "name": "X-Client-ID",
                    "in": "header",
                    "required": False,
                    "description": "Client ID for authentication",
                    "schema": {"type": "string"},
                })
                method["parameters"] = parameters
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    # Set the custom OpenAPI schema
    app.openapi = custom_openapi
    
    @app.get(f"{api_prefix}/docs", include_in_schema=False)
    async def custom_swagger_ui_html() -> HTMLResponse:
        """Custom Swagger UI endpoint"""
        return get_swagger_ui_html(
            openapi_url=f"{api_prefix}/openapi.json",
            title=f"{app.title} - Swagger UI",
            swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
            swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
            swagger_favicon_url="/favicon.ico",
        )
    
    @app.get(f"{api_prefix}/redoc", include_in_schema=False)
    async def custom_redoc_html() -> HTMLResponse:
        """Custom ReDoc endpoint"""
        return get_redoc_html(
            openapi_url=f"{api_prefix}/openapi.json",
            title=f"{app.title} - ReDoc",
            redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js",
            redoc_favicon_url="/favicon.ico",
        )