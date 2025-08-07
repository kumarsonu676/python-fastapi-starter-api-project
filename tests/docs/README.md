# FastAPI Testing Suite

## Overview

the illuminati testing pyramid:

```
     /\
    /  \    Functional Tests
   /____\   - Complete user workflows
  /      \  - Full HTTP request/response cycle
 /        \ - Real API testing
/__________\
Integration Tests
- Service + Repository interactions
- Database operations
- Cross-component testing

Unit Tests
- Individual function testing
- Pure logic validation
- Fast, isolated tests
```

## Test Structure

```
pytest.ini
tests/
├── conftest.py              
├── unit/                    
├── integration/             
├── functional/             
```


### Run Tests by Layer
```bash
pytest -m unit
pytest -m integration
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
**Dependencies**: Real database, real services

**Examples**:
- `test_repositories.py`: Database operations with real SQLite
- `test_services.py`: Business logic using real repositories


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
## Further Reading

- [Testing Guide](docs/testing_guide.md) - Comprehensive testing overview
- [Unit Testing](docs/unit_testing.md) - Detailed unit testing guide
- [Integration Testing](docs/integration_testing.md) - Integration testing best practices
- [Functional Testing](docs/functional_testing.md) - End-to-end testing guide
