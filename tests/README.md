# FastAPI Testing Suite

This testing suite demonstrates three essential layers of testing for modern web applications, specifically designed to teach junior developers different testing strategies and best practices.

## Overview

The test suite is organized into three layers following the testing pyramid:

```
     /\
    /  \    Functional Tests (Few)
   /____\   - Complete user workflows
  /      \  - Full HTTP request/response cycle
 /        \ - Real API testing
/__________\
Integration Tests (Some)
- Service + Repository interactions
- Database operations
- Cross-component testing

Unit Tests (Many)
- Individual function testing
- Pure logic validation
- Fast, isolated tests
```

## Test Structure

```
tests/
├── conftest.py              # Shared test fixtures and configuration
├── unit/                    # Unit Tests - Fast, isolated, mocked dependencies
│   ├── test_security.py     # Password hashing, JWT token functions
│   ├── test_schemas.py      # Pydantic validation logic
│   └── test_utils.py        # Response formatting utilities
├── integration/             # Integration Tests - Real DB, multiple components
│   ├── test_repositories.py # Database CRUD operations
│   └── test_services.py     # Business logic with DB interactions
├── functional/              # Functional Tests - Full app, HTTP requests
│   └── test_user_endpoints.py # Complete API workflows
└── docs/                    # Testing Documentation
    ├── testing_guide.md     # Comprehensive testing overview
    ├── unit_testing.md      # Unit testing best practices
    ├── integration_testing.md # Integration testing guide
    └── functional_testing.md  # Functional testing guide
```

## Quick Start

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run All Tests
```bash
pytest
```

### Run Tests by Layer
```bash
# Unit tests only (fast - < 5 seconds)
pytest -m unit

# Integration tests only (medium speed)
pytest -m integration

# Functional tests only (slower - full app)
pytest -m functional
```

### Run with Coverage
```bash
pytest --cov=app --cov-report=html
```

## What Each Layer Demonstrates

### 1. Unit Tests (`tests/unit/`)
**Purpose**: Test individual functions in complete isolation  
**Speed**: Very fast (< 1ms per test)  
**Dependencies**: Mocked/stubbed

**Examples**:
- `test_security.py`: Password hashing functions, JWT token creation/verification
- `test_schemas.py`: Pydantic model validation rules
- `test_utils.py`: Response formatting logic

**Key Learning Points**:
- How to mock external dependencies
- Testing pure functions and business logic
- Validating edge cases and error conditions
- Using pytest fixtures for test data

### 2. Integration Tests (`tests/integration/`)
**Purpose**: Test multiple components working together  
**Speed**: Medium (100ms - 1s per test)  
**Dependencies**: Real database, real services

**Examples**:
- `test_repositories.py`: Database operations with real SQLite
- `test_services.py`: Business logic using real repositories

**Key Learning Points**:
- Testing with real database operations
- Managing test data isolation
- Transaction handling and rollbacks
- Testing cross-component interactions

### 3. Functional Tests (`tests/functional/`)
**Purpose**: Test complete user workflows end-to-end  
**Speed**: Slower (1s+ per test)  
**Dependencies**: Full running application

**Examples**:
- `test_user_endpoints.py`: Complete API workflows including authentication

**Key Learning Points**:
- Making real HTTP requests to APIs
- Testing authentication and authorization flows
- Validating complete user journeys
- Error handling and edge cases

## Test Configuration

### pytest.ini
The project uses pytest with async support:
- Async test mode enabled
- Custom markers for test categorization
- Test discovery configuration

### conftest.py
Shared fixtures including:
- Test database setup with SQLite
- Async session management
- Test data factories
- HTTP client setup

## Running Examples

### Run a Specific Test
```bash
pytest tests/unit/test_security.py::TestPasswordSecurity::test_verify_password_correct -v
```

### Run Tests with Output
```bash
pytest -v -s
```

### Run Only Fast Tests
```bash
pytest -m "unit"
```

### Run Tests in Parallel
```bash
pytest -n auto  # Requires pytest-xdist
```

### Debug Mode
```bash
pytest --pdb  # Drop into debugger on failure
```

## Understanding Test Output

### Successful Test Run
```
tests/unit/test_security.py::TestPasswordSecurity::test_get_password_hash_returns_hash PASSED
tests/unit/test_schemas.py::TestUserCreateSchema::test_valid_user_create PASSED
```

### Test Markers
- `@pytest.mark.unit` - Unit test
- `@pytest.mark.integration` - Integration test
- `@pytest.mark.functional` - Functional test
- `@pytest.mark.slow` - Slow running test

## Learning Path

For junior developers, we recommend studying the tests in this order:

1. **Start with Unit Tests** (`tests/unit/`)
   - Learn basic test structure
   - Understand assertions and fixtures
   - Practice mocking dependencies

2. **Move to Integration Tests** (`tests/integration/`)
   - Understand database testing
   - Learn test data management
   - Practice testing component interactions

3. **Finish with Functional Tests** (`tests/functional/`)
   - Learn API testing
   - Understand end-to-end workflows
   - Practice testing complete user journeys

## Key Testing Concepts Demonstrated

### 1. Test Isolation
Each test runs independently with clean state

### 2. Test Data Management
Using factories and fixtures for consistent test data

### 3. Mocking Strategies
- Unit tests: Mock external dependencies
- Integration tests: Use real dependencies
- Functional tests: Test complete system

### 4. Assertion Patterns
- Specific assertions over general ones
- Testing both positive and negative cases
- Meaningful error messages

### 5. Test Organization
- Group related tests in classes
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)

## Common Commands

```bash
# Run all tests with verbose output
pytest -v

# Run tests with coverage report
pytest --cov=app --cov-report=term-missing

# Run only failed tests from last run
pytest --lf

# Run tests matching a pattern
pytest -k "test_user"

# Run tests and stop on first failure
pytest -x

# Run tests with timing information
pytest --durations=10
```

## Troubleshooting

### Database Issues
If you encounter database-related test failures:
```bash
# Remove test database file
rm test.db

# Run tests again
pytest
```

### Async Issues
If async tests are not running:
```bash
# Check pytest-asyncio is installed
pip install pytest-asyncio

# Verify asyncio mode in pytest.ini
```

### Import Errors
If you see import errors:
```bash
# Install project in development mode
pip install -e .

# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

## Further Reading

- [Testing Guide](docs/testing_guide.md) - Comprehensive testing overview
- [Unit Testing](docs/unit_testing.md) - Detailed unit testing guide
- [Integration Testing](docs/integration_testing.md) - Integration testing best practices
- [Functional Testing](docs/functional_testing.md) - End-to-end testing guide

## Contributing

When adding new tests:
1. Place them in the appropriate layer directory
2. Use the correct pytest marker
3. Follow the existing naming conventions
4. Include both positive and negative test cases
5. Update documentation if needed

Remember: Good tests are fast, isolated, repeatable, and self-validating! 