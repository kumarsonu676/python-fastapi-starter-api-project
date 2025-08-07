# Unit Testing Guide

## What Are Unit Tests?

- test individual functions/methods in complete isolation
- run very fast (< 1ms each)
- no external dependencies
- completely isolated and independent
- test pure logic and algorithms

## When to Write Unit Tests

- **complex business logic**: password validation, data transformation
- **pure functions**: utility functions, calculations, formatters
- **edge cases**: error conditions, boundary values, null inputs
- **critical security functions**: authentication, authorization, encryption
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
- **use descriptive test names**: explain what is tested and expected outcome
- **test error conditions**: empty strings, invalid inputs, edge cases
- **group related tests**: use test classes for organization

## Common Pitfalls

- **testing too much**: focus on single function, not integration workflows
- **not mocking dependencies**: avoid calling real databases/apis
- **over-mocking**: don't mock built-in functions like `str.lower()`

## Running Unit Tests

**all unit tests**: `pytest -m unit`
**specific file**: `pytest tests/unit/test_security.py`
**specific test**: `pytest tests/unit/test_security.py::TestPasswordSecurity::test_verify_password_correct`
**with coverage**: `pytest -m unit --cov=app --cov-report=html`
**verbose**: `pytest -m unit -v`

## Quality Metrics

- **coverage**: >90% line coverage on business logic, 100% on security functions
- **speed**: <1ms per test, <5 seconds for full suite
- **maintainability**: easy to understand, implementation changes don't break tests

## Unit Test Checklist

- [ ] tests single function/method
- [ ] all dependencies mocked
- [ ] runs fast (<1ms)
- [ ] descriptive test name
- [ ] tests expected behavior
- [ ] edge cases covered
- [ ] clear assertions
- [ ] understandable in 30 seconds 