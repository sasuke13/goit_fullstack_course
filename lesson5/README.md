# SQLAlchemy Practice Project (Topic 5)

This project is a complete practical template for the presentation:
**"Основи роботи з ORM SQLAlchemy"**.

It includes:
- PEP 249 (`sqlite3`) baseline CRUD examples (`Connection`, `Cursor`, `execute`)
- SQLAlchemy Core table definition + inserts + join query
- ORM models with SQLAlchemy 2.0 typed syntax (`Mapped`, `mapped_column`)
- Relationship types:
  - one-to-many (`User` -> `Address`)
  - one-to-one (`User` -> `Profile`)
  - many-to-many (`Student` <-> `Course`)
- Session lifecycle, CRUD operations, commit/rollback examples
- Modern query style with `select()`, `func`, `join`, eager loading
- SQLAlchemy 2.0 `execute()` flow for insert/select/update/delete without ORM session state
- Async SQLAlchemy with `create_async_engine` and `async_sessionmaker`

## Project structure

```text
lesson5/
  pyproject.toml
  README.md
  data/                    # sqlite db files are created here automatically
  src/
    pep249_demo.py
    db.py
    models.py
    core_demo.py
    orm_sync_demo.py
    execute_demo.py
    orm_async_demo.py
    main.py
```

## Setup

```bash
poetry install
```

## Run

Run all demos:

```bash
poetry run python src/main.py --mode all
```

Run specific sections:

```bash
poetry run python src/main.py --mode core
poetry run python src/main.py --mode sync
poetry run python src/main.py --mode pep249
poetry run python src/main.py --mode execute
poetry run python src/main.py --mode async
```

## Assumptions and decisions

- SQLite is used to keep practice simple and fully local.
- `echo=True` is enabled by default to match learning goals and show generated SQL.
- Databases are recreated for each run of ORM demos, so output is predictable.
- The examples prioritize readability and coverage of lecture topics over production architecture.
- Poetry is used as the dependency and virtual environment manager.
