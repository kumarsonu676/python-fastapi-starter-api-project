# FastAPI Testing Suite

basic guide to get started with diff layers of testing.

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

**Examples**:
- `test_security.py`: Password hashing functions, JWT token creation/verification
- `test_schemas.py`: Pydantic model validation rules
- `test_utils.py`: Response formatting logic

### 2. Integration Tests (`tests/integration/`)
**Purpose**: Test multiple components working together  
**Dependencies**: Real database, real services

**Examples**:
- `test_repositories.py`: Database operations with real SQLite
- `test_services.py`: Business logic using real repositories


### 3. Functional Tests (`tests/functional/`)
**Purpose**: Test complete user workflows end-to-end  
**Dependencies**: Full running application

**Examples**:
- `test_user_endpoints.py`: Complete API workflows including authentication

- Testing authentication and authorization flows
- Validating complete user journeys
- Error handling and edge cases

## Test Configuration

### pytest.ini
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

## Further Reading

- [Testing Guide](docs/testing_guide.md) - Comprehensive testing overview
- [Unit Testing](docs/unit_testing.md) - Detailed unit testing guide
- [Integration Testing](docs/integration_testing.md) - Integration testing best practices
- [Functional Testing](docs/functional_testing.md) - End-to-end testing guide
