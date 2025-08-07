# Unit Testing Guide

## What Are Unit Tests?

- test individual functions/methods in complete isolation
- no external dependencies
- completely isolated and independent
- test pure logic and algorithms

## When to Write Unit Tests

- **pure functions**: utility functions, calculations, formatters
- **edge cases**: error conditions, boundary values, null inputs
- **validation logic**: schema validators, input sanitizers

## Examples from the Project

### Security Functions
**see**: [test_security.py](../unit/test_security.py)
- password hashing and verification
- jwt token operations
- authentication utilities

### Schema Validation  
**see**: [test_schemas.py](../unit/test_schemas.py)
- pydantic model validation
- input sanitization
- error message verification

### Utility Functions
**see**: [test_utils.py](../unit/test_utils.py)
- response formatting
- common helper functions
- data transformation utilities

### Service Layer (Unit)
**see**: [test_user_service.py](../unit/test_user_service.py)
- business logic with mocked dependencies
- service method behavior
- error handling

## Unit Testing Patterns

### Arrange-Act-Assert (AAA)
- **arrange**: set up test data
- **act**: execute the function
- **assert**: verify the result

### Test Edge Cases
- empty/null inputs
- boundary values
- minimum/maximum lengths
- invalid data formats

### Parameterized Tests
- use `@pytest.mark.parametrize` for multiple scenarios
- test valid/invalid combinations efficiently

### Mocking External Dependencies
- use `unittest.mock` to isolate units
- mock only external dependencies, not built-ins
- verify mock interactions when needed

## Best Practices

- **keep tests simple**: one assertion per test, clear names, minimal setup
- **test behavior, not implementation**: focus on what code should do
- **mock external modules/function calls**


## Running Unit Tests

**all unit tests**: `pytest -m unit`
**specific file**: `pytest tests/unit/test_security.py`
**with coverage**: `pytest -m unit --cov=app --cov-report=html`
**verbose**: `pytest -m unit -v`