# GraphFleet

GraphRAG implementation for fleet management using FastAPI and PostgreSQL.

## Features

- GraphRAG-powered search functionality
- Async PostgreSQL database integration
- FastAPI REST API with OpenAPI documentation
- Environment-based configuration
- Poetry dependency management

## Prerequisites

- Python 3.11 or higher
- PostgreSQL 13 or higher
- Poetry for dependency management

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/GraphFleet.git
cd GraphFleet
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Copy the example environment file and update it with your settings:
```bash
cp .env.example .env
```

4. Update the `.env` file with your configuration:
- Set your PostgreSQL connection details
- Add your OpenAI API key
- Configure other settings as needed

## Development

1. Start the PostgreSQL database

2. Run the development server:
```bash
poetry run uvicorn app.main:app --reload
```

3. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
GraphFleet/
├── app/
│   ├── api/
│   │   └── api_v1/
│   │       └── endpoints/
│   │           └── search.py
│   ├── core/
│   │   └── config.py
│   ├── db/
│   │   ├── base.py
│   │   ├── init_db.py
│   │   └── session.py
│   ├── models/
│   ├── schemas/
│   │   └── search.py
│   ├── services/
│   │   └── search.py
│   └── main.py
├── tests/
├── .env
├── .env.example
├── pyproject.toml
└── README.md
```

## Testing

Run the test suite:
```bash
poetry run pytest
```

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.
