# Testing Guide

## Testing Pyramid

- **Unit Tests**: individual functions, fast, isolated
- **Integration Tests**: multi-component interactions, database operations
- **Functional Tests**: end-to-end workflows, real HTTP requests

## Unit Tests
- test individual functions/methods in isolation
- mock all external dependencies
- **what to test**:
  - complex business logic
  - validation logic
  - utility functions
  - edge cases and error conditions
- **examples**: [test_security.py](../unit/test_security.py), [test_schemas.py](../unit/test_schemas.py), [test_utils.py](../unit/test_utils.py)

## Integration Tests 
- test multiple components working together
- speed: 100ms - 1s per test
- use real database/services
- **what to test**:
  - repository database operations
  - service layer business logic
  - cross-component workflows
- **examples**: [test_services.py](../integration/test_services.py), [test_user_repository.py](../integration/test_user_repository.py), [test_repository.py](../integration/test_repository.py)

## Functional Tests 
- test complete user workflows end-to-end
- speed: 1s+ per test
- real HTTP requests to full application
- **what to test**:
  - api endpoint workflows
  - authentication and authorization
  - error handling and edge cases
  - complete user journeys
- **examples**: [test_user_endpoints.py](../functional/test_user_endpoints.py), [test_user_login.py](../functional/test_user_login.py), [test_user_register.py](../functional/test_user_register.py)

## Running Tests

**all tests**: `pytest`
**by layer**: `pytest -m unit/integration/functional`
**with coverage**: `pytest --cov=app --cov-report=html`
**parallel**: `pytest -n auto`

## Test Organization

- **unit/**: [test_security.py](../unit/test_security.py), [test_schemas.py](../unit/test_schemas.py), [test_utils.py](../unit/test_utils.py), [test_user_service.py](../unit/test_user_service.py)
- **integration/**: [test_services.py](../integration/test_services.py), [test_user_repository.py](../integration/test_user_repository.py), [test_repository.py](../integration/test_repository.py)
- **functional/**: [test_user_endpoints.py](../functional/test_user_endpoints.py), [test_user_login.py](../functional/test_user_login.py), [test_user_register.py](../functional/test_user_register.py), [test_app.py](../functional/test_app.py), [test_middleware_functional.py](../functional/test_middleware_functional.py)

## Best Practices

- follow testing pyramid: many unit → some integration → few functional
- test behavior, not implementation
- use descriptive test names
- arrange-act-assert structure
- one assertion per test
- fast and deterministic execution

## Quick Commands

**run specific test**: `pytest tests/unit/test_security.py::TestPasswordSecurity::test_verify_password_correct -v`
**debug mode**: `pytest --pdb`
**verbose**: `pytest -v -s`

## Coverage Goals

- unit tests: >90% line coverage
- integration tests: >80% feature coverage  
- functional tests: >70% user journey coverage 