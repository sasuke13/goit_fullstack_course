# FastAPI Notes API Demo

Проєкт реалізує REST API для `tags` та `notes` на основі багаторівневої архітектури:
- API layer (`src/api`)
- Service layer (`src/services`)
- Repository layer (`src/repository`)
- Infrastructure layer (`src/db`, `src/settings.py`)
- Schemas layer (`src/schemas`)

## Швидкий старт

1. Встановіть залежності:
```bash
poetry install
```

2. Запустіть PostgreSQL через Docker Compose:
```bash
docker compose up -d
```

3. Перевірте статус контейнера:
```bash
docker compose ps
```

4. Запустіть застосунок:
```bash
poetry run start
```

5. Відкрийте Swagger:
- `http://127.0.0.1:8000/docs`

6. Заповніть базу тестовими даними:
```bash
poetry run seed
```

Для пагінації у списках використовуйте query-параметри:
- `/api/notes?page=1&per_page=10`
- `/api/tags?page=1&per_page=10`

## Міграції (Alembic)

Після ініціалізації:
```bash
poetry run alembic init migrations
```

У `migrations/env.py`:
- імпортуйте `Base` з `src.db.models`
- імпортуйте `settings` з `src.settings`
- встановіть:
```python
target_metadata = Base.metadata
config.set_main_option("sqlalchemy.url", settings.DB_URL)
```
У `alembic.ini` можна залишити `sqlalchemy.url` порожнім, бо фактичне значення береться з налаштувань проєкту.

Далі:
```bash
poetry run alembic revision --autogenerate -m "Init"
poetry run alembic upgrade head
```
