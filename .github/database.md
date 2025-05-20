# Database Best Practices

Database best practices focusing on Python FastAPI with PostgreSQL and SQLAlchemy

## Database Setup

- Use SQLAlchemy as the ORM (Object-Relational Mapper)
- Configure database connection using environment variables
- Use connection pooling for efficient resource management
- Implement database migration with Alembic
- Set up proper logging for database operations
- Use async database drivers where applicable (asyncpg)

## Database Models

- Create clear SQLAlchemy models with proper type annotations
- Follow consistent naming conventions (snake_case for tables/columns)
- Properly define relationships between models
- Use appropriate column types and constraints
- Define indexes for frequently queried columns
- Use SQLAlchemy declarative base for model definitions

## Query Patterns

- Use SQLAlchemy Core for complex queries
- Implement proper filtering methods
- Handle pagination efficiently
- Use eager loading to avoid N+1 query problems
- Implement proper transaction management
- Create reusable query components

## Database Design

- Apply proper normalization techniques
- Design tables with appropriate primary keys
- Implement foreign key constraints
- Consider using UUIDs instead of sequential IDs for public resources
- Use proper composite keys where applicable
- Design with scalability in mind

## Performance

- Create appropriate indexes for frequently queried columns
- Optimize query patterns for common operations
- Implement connection pooling
- Use query batching for bulk operations
- Monitor query performance
- Implement caching strategies (Redis) for frequently accessed data

## Security

- Store connection strings securely in environment variables
- Implement proper database user permissions
- Use parameterized queries to prevent SQL injection
- Hash sensitive data before storing
- Encrypt personally identifiable information (PII)
- Implement proper error handling without exposing database details

## Repository Pattern

- Implement the repository pattern to abstract database operations
- Create dedicated repository classes for each domain entity
- Define clear interface methods for CRUD operations
- Separate business logic from data access code
- Use dependency injection for repositories
- Create unit tests for repository methods

## FastAPI Integration

- Use dependency injection for database sessions
- Create Pydantic models for request/response schemas
- Implement proper validation with Pydantic
- Create database middleware for consistent session handling
- Use background tasks for long-running database operations
- Properly document database-related endpoints with OpenAPI

## Migrations and Versioning

- Use Alembic for database migrations
- Create migration scripts for schema changes
- Test migrations in development before deploying
- Implement version control for database schemas
- Create rollback plans for migrations
- Document migration processes

## Best Practices

- Follow consistent coding standards
- Document database schema and relationships
- Implement proper error handling for database operations
- Use environment-specific configurations
- Regular database maintenance (vacuum, analyze)
- Implement proper backup and recovery strategies
