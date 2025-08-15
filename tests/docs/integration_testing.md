# Integration Testing Guide

## What Are Integration Tests?

- test multiple classes/modules working together or use real external dependencies (databases, apis)
- verify data flows between components
- test business logic with real data persistence

## When to Write Integration Tests

- **repository database operations**: complex crud operations, queries, transactions
- **service layer interactions**: business logic that uses repositories
- **external api integrations**: third-party service calls
- **cross-component workflows**: features spanning multiple modules / classes

## Examples from the Project

### Repository Testing
**see**: [test_user_repository.py](../integration/test_user_repository.py), [test_repository.py](../integration/test_repository.py)
- database operations with real database
- crud operations
- data persistence verification
- database constraints and relationships

### Service Layer Testing
**see**: [test_services.py](../integration/test_services.py)
- business logic with repository interactions
- service and repository working together
- password hashing integration
- real database transaction handling

## Integration Testing Patterns

### if using a database
- use real database (sqlite for speed, test postgres/mssql db if needed) with proper cleanup
- create/destroy schema for each test session
- use transactions for test isolation

### Partial Mocking
- mock external apis while keeping database real
- use partial mocking for controlled testing
- verify service-repository interactions


## Running Integration Tests

**all integration tests**: `pytest -m integration`
**specific file**: `pytest tests/integration/test_repositories.py`
**with database output**: `pytest -m integration -s --log-cli-level=DEBUG`

## Test Database Setup

**sqlite to file**: `sqlite+aiosqlite:///./test.db`
also possible in //memory