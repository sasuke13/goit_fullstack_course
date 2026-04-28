# FastAPI Practice App

Production-style FastAPI demo project for quick presentation.

## Why this structure

- Clear layers: `api` -> `services` -> `repositories` -> `models`
- Async SQLAlchemy 2.0 with explicit session dependency
- Pydantic schemas for request/response validation
- Startup lifespan initializes tables
- Dedicated `db_init.py` for deterministic demo seed data

## Project structure

```text
fastapi_practice_app/
  pyproject.toml
  README.md
  app/
    main.py
    db_init.py
    core/
      config.py
      database.py
    models/
      base.py
      user.py
      task.py
    schemas/
      user.py
      task.py
    repositories/
      user_repository.py
      task_repository.py
    services/
      user_service.py
      task_service.py
    api/
      deps.py
      v1/
        router.py
        health.py
        users.py
        tasks.py
```

## Setup

```bash
cd fastapi_practice_app
poetry install
```

## Prepare demo data

```bash
poetry run python -m app.db_init
```

## Run server

```bash
poetry run uvicorn app.main:app --reload
```

## API endpoints

- `GET /api/v1/health`
- `POST /api/v1/users`
- `GET /api/v1/users`
- `GET /api/v1/users/{user_id}`
- `POST /api/v1/tasks`
- `GET /api/v1/tasks`
- `PATCH /api/v1/tasks/{task_id}`
- `DELETE /api/v1/tasks/{task_id}`

## Quick presentation flow

1. Run `poetry run python -m app.db_init`
2. Start server with `poetry run uvicorn app.main:app --reload`
3. Open docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
4. Create user -> create task -> update task -> list results
