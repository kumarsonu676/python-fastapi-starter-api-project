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
- use real database (sqlite for speed) with proper cleanup
- create/destroy schema for each test session
- use transactions for test isolation

### Partial Mocking
- mock external apis while keeping database real
- use partial mocking for controlled testing
- verify service-repository interactions


## Best Practices

- **use real dependencies**: real database, not mocked repositories
- **test data isolation**: unique data per test, dont use shared state
- **test business logic, not implementation**: focus on behavior, not internal calls
- **test error conditions**: duplicate keys, constraint violations, invalid data
- **use meaningful assertions**: specific checks, not just "not none"

## Common Pitfalls

- **testing too little**: only happy path, missing error scenarios
- **improper test isolation**: tests depending on each other
- **slow tests**: creating excessive test data, not optimizing queries

## Running Integration Tests

**all integration tests**: `pytest -m integration`
**specific file**: `pytest tests/integration/test_repositories.py`
**with database output**: `pytest -m integration -s --log-cli-level=DEBUG`
**with coverage**: `pytest -m integration --cov=app --cov-report=html`

## Test Database Setup

**sqlite for speed**: `sqlite+aiosqlite:///./test.db`
**postgresql for production similarity**: `postgresql+asyncpg://test_user:test_pass@localhost/test_db`

## Quality Metrics

- **coverage**: >80% line coverage for business logic
- **performance**: <30 seconds total, <1 second per test
- **data quality**: realistic volumes, integrity constraints, concurrent access

## Integration Test Checklist

- [ ] uses real database or external service
- [ ] tests multiple components working together
- [ ] proper test data isolation
- [ ] cleans up after itself
- [ ] tests success and failure scenarios
- [ ] verifies data persistence/changes
- [ ] meaningful assertions
- [ ] runs in reasonable time (<1 second) 