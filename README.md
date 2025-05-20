# FastAPI Project

A scalable FastAPI project template with SQLAlchemy, PostgreSQL, and best practices for building robust APIs.

## Features

- **FastAPI framework** with all its features
- **Async SQLAlchemy** with PostgreSQL
- **Repository pattern** for data access
- **Service layer** for business logic
- **Pydantic models** for validation
- **Modular project structure** following best practices
- **Dependency injection** for clean code organization
- **Custom exception handling** for consistent error responses
- **Docker support** for easy development and deployment
- **Automatic API documentation** with Swagger/OpenAPI
- **Comprehensive test suite** with pytest
- **Authentication** with JWT tokens

## Project Structure

```
.
├── alembic/                # Database migrations
├── app/                    # Application code
│   ├── api/                # API routes
│   │   └── v1/             # API version 1
│   │       ├── endpoints/  # API endpoints
│   │       └── api.py      # API router
│   ├── core/               # Core configuration
│   ├── db/                 # Database models and session
│   ├── dependencies/       # Dependency injection
│   ├── exceptions/         # Custom exceptions
│   ├── middlewares/        # Middleware functions
│   ├── models/             # SQLAlchemy models
│   ├── repositories/       # Data access layer
│   ├── schemas/            # Pydantic schemas
│   ├── services/           # Business logic
│   ├── utils/              # Utility functions
│   └── main.py             # FastAPI application
├── docs/                   # Documentation
├── tests/                  # Tests
│   ├── integration/        # Integration tests
│   └── unit/               # Unit tests
├── .env.example            # Example environment variables
├── .gitignore              # Git ignore file
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile              # Docker configuration
├── main.py                 # Application entry point
├── pytest.ini              # Pytest configuration
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
└── setup.py                # Package setup
```

## Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL
- Docker (optional)

### Installation

#### Local Development

1. Clone the repository:

```bash
git clone https://github.com/yourusername/fastapi-project.git
cd fastapi-project
```

2. Create and activate a virtual environment:

```bash
py -m venv venv
venv\\Scripts\\activate #venv\scripts\activate for windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

OR

```bash
py -m pip install -r requirements.txt
```

```bash
#to update requirements.txt file =>
py -m pip freeze > requirements.txt
```

4. Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

5. Start the application:

```bash
python main.py
```

OR

```bash
py -m main
```

#### Docker Development

1. Clone the repository:

```bash
git clone https://github.com/yourusername/fastapi-project.git
cd fastapi-project
```

2. Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

3. Start the containers:

```bash
docker-compose up -d
```

### Access the API

The API will be available at [http://localhost:8000](http://localhost:8000).

API documentation is available at:

- Swagger UI: [http://localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs)
- ReDoc: [http://localhost:8000/api/v1/redoc](http://localhost:8000/api/v1/redoc)

## Development

### Adding a New Endpoint

1. Create a new file in `app/api/v1/endpoints/`
2. Create Pydantic models in `app/schemas/`
3. Add SQLAlchemy models in `app/models/` if needed
4. Implement business logic in `app/services/`
5. Create repository in `app/repositories/` for data access
6. Add the router to `app/api/v1/api.py`

### Database Migrations

```bash
# Initialize migrations (first time only)
py -m alembic init alembic

# Create a new migration
py -m alembic revision --autogenerate -m "Migration message"

# Run migrations
py -m alembic upgrade head
```

# Generate SQL Script from migration/revision name

```bash
#  For the first migration— When it has no parent (Revises: is empty).
py -m alembic upgrade base:<revision_name> --sql > migration_script.sql
```

```bash
# If you want to generate a script that can be used to downgrade from the current revision to the base revision, you can use:
py -m alembic downgrade base --sql > migration_script.sql
```

```bash
# For the subsequent migration— When it has a parent (Revises: <revision_name>).
# This will generate a script that can be used to upgrade from the previous revision to the current one.
py -m alembic upgrade <from_rev>:<to_rev> --sql > migration_script.sql
```

```bash
# If you want the SQL to downgrade from to_rev back to from_rev, just reverse the order:
py -m alembic downgrade <to_rev>:<from_rev> --sql > migration_script.sql
```

```bash
# To list all revisions and order:
py -m alembic history --verbose
```

```bash
# To show the current revision:
py -m alembic current
```

```bash
# To inspect details of a specific revision:
py -m alembic show <revision_name>
```

---

### Environment Variables

Key environment variables for configuration:

- `API_V1_STR`: API version prefix
- `SECRET_KEY`: Secret key for JWT tokens
- `POSTGRES_SERVER`: PostgreSQL server address
- `POSTGRES_USER`: PostgreSQL username
- `POSTGRES_PASSWORD`: PostgreSQL password
- `POSTGRES_DB`: PostgreSQL database name

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [Alembic](https://alembic.sqlalchemy.org/)

2. Activate the virtual environment:

   ```bash
   # On Windows
   venv\Scripts\activate

   # On Linux/Mac
   source venv/bin/activate
   ```

3. Run the application:

   ```bash
   python main.py
   ```

4. Access the API at http://localhost:8000
