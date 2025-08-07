# Functional Testing Guide

## What Are Functional Tests?

- test complete application stack (http → controllers → services → database)
- make actual http requests to api endpoints
- test user workflows end-to-end
- verify authentication and authorization
- test error handling and edge cases
- run slowest but provide highest confidence

## When to Write Functional Tests

- **complete user workflows**: registration → login → access protected resources
- **api endpoint behavior**: request/response formats, status codes, headers
- **authentication flows**: login, token validation, role-based access
- **error scenarios**: invalid inputs, unauthorized access, not found cases
- **business workflows**: multi-step processes spanning several endpoints

## Examples from the Project

### User Registration Workflow
**see**: [test_user_register.py](../functional/test_user_register.py), [test_user_endpoints.py](../functional/test_user_endpoints.py)
- complete user registration flow
- api contract verification (status codes, response format)
- data validation and business logic
- sensitive data exclusion from responses

### Authentication and Authorization
**see**: [test_user_login.py](../functional/test_user_login.py), [test_user_endpoints.py](../functional/test_user_endpoints.py)
- login and protected endpoint access
- jwt token validation
- role-based access control
- authentication flows

### Complete User Journey
**see**: [test_user_endpoints.py](../functional/test_user_endpoints.py)
- full workflow from registration to authenticated access
- multi-step processes
- end-to-end user experience

## Functional Testing Patterns

### HTTP Client Setup
- use asyncclient for making real http requests
- override dependencies for testing
- proper setup and teardown

### Authentication Helper
- create utilities for authenticated requests
- jwt token generation for testing
- authorization header management

### Role-Based Access Testing
- test authorization for different user roles
- admin vs user permissions
- forbidden access scenarios

### Error Handling Testing
- 404 endpoints, invalid json payloads
- unauthorized access attempts
- malformed requests

## Running Functional Tests

**all functional tests**: `pytest -m functional`
**specific test class**: `pytest tests/functional/test_user_endpoints.py::TestUserRegistration -v`
**slow tests**: `pytest -m "functional and slow"`
**with http logging**: `pytest -m functional -s --log-cli-level=DEBUG`
**with coverage**: `pytest -m functional --cov=app --cov-report=html`

## Test Environment Setup

**override dependencies**: database overrides for testing
**environment variables**: testing=true, test secret keys
**parallel execution**: `pytest -m functional -n auto`

## Functional Test Checklist

- [ ] makes real http requests to api
- [ ] tests endpoint or complete user workflow
- [ ] validates http status codes and headers
- [ ] tests success and error scenarios
- [ ] includes authentication/authorization
- [ ] uses realistic test data
- [ ] proper cleanup/isolation