# Unit Testing Guide

Unit tests are the foundation of your testing strategy. They test individual functions, methods, or classes in complete isolation from external dependencies.

## What Are Unit Tests?

Unit tests focus on testing the smallest testable parts of your application. They should:
- Test a single function or method
- Run very fast (< 1ms each)
- Have no external dependencies
- Be completely isolated and independent
- Test pure logic and algorithms

## When to Write Unit Tests

Write unit tests for:
- **Complex business logic**: Password validation, data transformation
- **Pure functions**: Utility functions, calculations, formatters
- **Edge cases**: Error conditions, boundary values, null inputs
- **Critical security functions**: Authentication, authorization, encryption
- **Validation logic**: Schema validators, input sanitizers

## Examples from the Project

### 1. Security Functions (`test_security.py`)

Testing password hashing and JWT token operations:

```python
def test_get_password_hash_returns_hash(self):
    """test password hashing produces non-empty hash"""
    password = "TestPassword123"
    hashed = get_password_hash(password)
    
    assert hashed is not None
    assert hashed != password
    assert len(hashed) > 20  # bcrypt hashes are long
    assert hashed.startswith("$2b$")  # bcrypt format
```

**Why this is a good unit test**:
- Tests a single function (`get_password_hash`)
- No external dependencies
- Tests the expected behavior (hash format, length)
- Fast execution

### 2. Schema Validation (`test_schemas.py`)

Testing Pydantic model validation:

```python
def test_password_validation_no_digit(self):
    """test password validation fails without digit"""
    data = {
        "email": "test@example.com",
        "password": "NoDigitPassword",  # Invalid: no digit
        "first_name": "Test",
        "last_name": "User"
    }
    
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(**data)
    
    assert "Password must contain at least one digit" in str(exc_info.value)
```

**Why this is a good unit test**:
- Tests validation logic in isolation
- Verifies specific error messages
- No database or network calls
- Tests edge cases (missing digit)

### 3. Utility Functions (`test_utils.py`)

Testing response formatting:

```python
def test_create_response_success_default(self):
    """test creating successful response with defaults"""
    data = {"user_id": 1, "name": "test"}
    response = create_response(data=data)
    
    assert isinstance(response, JSONResponse)
    assert response.status_code == 200
    
    content = response.body.decode()
    assert '"success":true' in content
    assert '"data":{"user_id":1,"name":"test"}' in content
```

## Unit Testing Patterns

### 1. Arrange-Act-Assert (AAA)

Structure your tests clearly:

```python
def test_example():
    # Arrange: Set up test data
    input_data = "test input"
    expected = "expected output"
    
    # Act: Execute the function
    result = function_under_test(input_data)
    
    # Assert: Verify the result
    assert result == expected
```

### 2. Test Edge Cases

Always test boundary conditions:

```python
def test_password_validation_edge_cases(self):
    # Empty password
    with pytest.raises(ValidationError):
        UserCreate(email="test@test.com", password="")
    
    # Minimum length
    with pytest.raises(ValidationError):
        UserCreate(email="test@test.com", password="Short1")
    
    # Maximum length (if applicable)
    long_password = "A" * 1000 + "1"
    # Test behavior with very long passwords
```

### 3. Parameterized Tests

Test multiple scenarios efficiently:

```python
@pytest.mark.parametrize("password,should_pass", [
    ("ValidPass123", True),
    ("nodigits", False),
    ("NOLOWERCASE123", False),
    ("nouppercase123", False),
    ("", False),
])
def test_password_validation(password, should_pass):
    data = {"email": "test@test.com", "password": password}
    
    if should_pass:
        user = UserCreate(**data)
        assert user.password == password
    else:
        with pytest.raises(ValidationError):
            UserCreate(**data)
```

### 4. Mocking External Dependencies

Use `unittest.mock` to isolate units:

```python
@patch('app.core.security.settings')
def test_create_access_token_basic(self, mock_settings):
    # Arrange: Mock external dependencies
    mock_settings.SECRET_KEY = "test-secret-key"
    mock_settings.ALGORITHM = "HS256"
    mock_settings.JWT_AUDIENCE = "test-audience"
    
    # Act: Call function
    data = {"sub": "test@example.com"}
    token = create_access_token(data)
    
    # Assert: Verify behavior
    assert token is not None
    assert isinstance(token, str)
    assert token.count(".") == 2  # JWT format
```

## Best Practices

### 1. Keep Tests Simple
- One logical assertion per test
- Clear test names that describe the scenario
- Minimal test setup

### 2. Test Behavior, Not Implementation
```python
# Good: Tests the behavior
def test_user_creation_sets_default_role():
    user = UserCreate(email="test@test.com", password="Pass123")
    assert user.role == UserRole.USER.value

# Bad: Tests implementation details
def test_user_creation_calls_enum_value():
    # Too tied to how the code works internally
```

### 3. Use Descriptive Test Names
```python
# Good: Describes what and why
def test_password_validation_fails_when_missing_uppercase()

# Bad: Vague and unclear
def test_password()
```

### 4. Test Error Conditions
```python
def test_verify_password_handles_empty_strings():
    assert verify_password("", "") is False
    assert verify_password("password", "") is False
    assert verify_password("", "hash") is False
```

### 5. Group Related Tests
```python
class TestPasswordSecurity:
    """test password hashing and verification functions"""
    
    def test_get_password_hash_returns_hash(self):
        # Test hash generation
    
    def test_verify_password_correct(self):
        # Test correct password verification
    
    def test_verify_password_incorrect(self):
        # Test incorrect password verification
```

## Common Pitfalls

### 1. Testing Too Much
```python
# Bad: Testing multiple things
def test_user_creation_and_validation_and_storage():
    # This is actually an integration test
    
# Good: Focus on one thing
def test_user_schema_validation():
    # Just test validation logic
```

### 2. Not Mocking Dependencies
```python
# Bad: Calls real database
def test_user_service_create():
    user = user_service.create(user_data)  # Hits real DB!
    
# Good: Mock the repository
@patch('app.services.UserRepository')
def test_user_service_create(mock_repo):
    mock_repo.create.return_value = mock_user
    # Test service logic only
```

### 3. Over-Mocking
```python
# Bad: Mocking too much
@patch('str.lower')  # Don't mock built-in functions
@patch('len')
def test_something():
    # Test becomes meaningless
    
# Good: Mock only external dependencies
@patch('app.services.external_api_call')
def test_something():
    # Mock only what you need
```

## Running Unit Tests

### Run All Unit Tests
```bash
pytest -m unit
```

### Run Specific Test File
```bash
pytest tests/unit/test_security.py
```

### Run Specific Test
```bash
pytest tests/unit/test_security.py::TestPasswordSecurity::test_verify_password_correct
```

### Run with Coverage
```bash
pytest -m unit --cov=app --cov-report=html
```

### Verbose Output
```bash
pytest -m unit -v
```

## Measuring Quality

### Coverage Metrics
- Aim for > 90% line coverage on business logic
- 100% coverage on critical security functions
- Don't chase 100% coverage on trivial code

### Speed Metrics
- Unit tests should run in < 1ms each
- Full unit test suite should complete in < 5 seconds
- If tests are slow, you're probably testing too much

### Maintainability
- Tests should be easy to understand
- Changing implementation shouldn't break tests
- Adding new features should require minimal test changes

## Unit Test Checklist

For each unit test, ask:
- [ ] Does it test a single function/method?
- [ ] Are all dependencies mocked?
- [ ] Does it run fast (< 1ms)?
- [ ] Is the test name descriptive?
- [ ] Does it test the expected behavior?
- [ ] Are edge cases covered?
- [ ] Is the assertion clear and specific?
- [ ] Can I understand what it does in 30 seconds?

## Conclusion

Unit tests are your first line of defense against bugs. They should be:
- **Fast**: Enable rapid feedback during development
- **Isolated**: Test one thing at a time
- **Comprehensive**: Cover all edge cases and error conditions
- **Maintainable**: Easy to understand and modify

Good unit tests make refactoring fearless and debugging faster. They catch bugs early when they're cheapest to fix and provide living documentation of how your code should behave. 