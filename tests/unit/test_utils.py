import pytest
from fastapi.responses import JSONResponse

from app.utils.response import create_response
from app.dtos.custom_response_dto import CustomResponse


@pytest.mark.unit
class TestResponseUtils:
    """test response utility functions"""
    
    def test_create_response_success_default(self):
        """test creating successful response with defaults"""
        data = {"user_id": 1, "name": "test"}
        response = create_response(data=data)
        
        assert isinstance(response, JSONResponse)
        assert response.status_code == 200
        
        # check response content structure
        content = response.body.decode()
        assert '"success":true' in content
        assert '"data":{"user_id":1,"name":"test"}' in content
        assert '"message":null' in content
        assert '"errors":null' in content
        assert '"error_code":null' in content
    
    def test_create_response_with_message(self):
        """test response with custom message"""
        data = {"id": 1}
        message = "operation completed successfully"
        response = create_response(data=data, message=message)
        
        assert response.status_code == 200
        content = response.body.decode()
        assert '"success":true' in content
        assert '"message":"operation completed successfully"' in content
    
    def test_create_response_error(self):
        """test creating error response"""
        errors = ["validation failed", "invalid email"]
        error_code = "VALIDATION_ERROR"
        response = create_response(
            data=None,
            success=False,
            errors=errors,
            error_code=error_code,
            status_code=400
        )
        
        assert response.status_code == 400
        content = response.body.decode()
        assert '"success":false' in content
        assert '"data":null' in content
        assert '"errors":["validation failed","invalid email"]' in content
        assert '"error_code":"VALIDATION_ERROR"' in content
    
    def test_create_response_none_data(self):
        """test response with none data"""
        response = create_response(data=None, message="no data found")
        
        assert response.status_code == 200
        content = response.body.decode()
        assert '"success":true' in content
        assert '"data":null' in content
        assert '"message":"no data found"' in content
    
    def test_create_response_list_data(self):
        """test response with list data"""
        data = [{"id": 1}, {"id": 2}]
        response = create_response(data=data)
        
        assert response.status_code == 200
        content = response.body.decode()
        assert '"success":true' in content
        assert '"data":[{"id":1},{"id":2}]' in content
    
    def test_create_response_custom_status_code(self):
        """test response with custom status code"""
        data = {"created": True}
        response = create_response(data=data, status_code=201)
        
        assert response.status_code == 201
        content = response.body.decode()
        assert '"success":true' in content
        assert '"data":{"created":true}' in content
    
    def test_create_response_complex_data(self):
        """test response with complex nested data"""
        data = {
            "user": {
                "id": 1,
                "profile": {
                    "name": "test user",
                    "settings": {"theme": "dark"}
                }
            },
            "metadata": {"version": "1.0"}
        }
        response = create_response(data=data)
        
        assert response.status_code == 200
        content = response.body.decode()
        assert '"success":true' in content
        assert '"user"' in content
        assert '"profile"' in content
        assert '"metadata"' in content
    
    def test_create_response_empty_errors_list(self):
        """test response with empty errors list"""
        response = create_response(
            data=None,
            success=False, 
            errors=[],
            status_code=400
        )
        
        assert response.status_code == 400
        content = response.body.decode()
        assert '"success":false' in content
        assert '"errors":[]' in content
    
    def test_create_response_single_error(self):
        """test response with single error in list"""
        response = create_response(
            data=None,
            success=False,
            errors=["single error"],
            error_code="ERROR",
            status_code=500
        )
        
        assert response.status_code == 500
        content = response.body.decode()
        assert '"success":false' in content
        assert '"errors":["single error"]' in content
        assert '"error_code":"ERROR"' in content


@pytest.mark.unit
class TestCustomResponseDTO:
    """test custom response dto structure"""
    
    def test_custom_response_dto_defaults(self):
        """test dto with default values"""
        response = CustomResponse()
        
        assert response.success is True
        assert response.data is None
        assert response.message is None
        assert response.errors is None
        assert response.error_code is None
    
    def test_custom_response_dto_with_data(self):
        """test dto with typed data"""
        data = {"user_id": 1, "username": "test"}
        response = CustomResponse[dict](
            success=True,
            data=data,
            message="user retrieved"
        )
        
        assert response.success is True
        assert response.data == data
        assert response.message == "user retrieved"
        assert response.errors is None
        assert response.error_code is None
    
    def test_custom_response_dto_error_state(self):
        """test dto in error state"""
        errors = ["field required", "invalid format"]
        response = CustomResponse(
            success=False,
            data=None,
            errors=errors,
            error_code="VALIDATION_FAILED"
        )
        
        assert response.success is False
        assert response.data is None
        assert response.errors == errors
        assert response.error_code == "VALIDATION_FAILED"
        assert response.message is None 