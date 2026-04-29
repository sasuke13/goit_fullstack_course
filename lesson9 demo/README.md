# JWT Auth Lesson Demo

Навчальний проєкт за методичкою з теми "Аутентифікація та авторизація".

## Що входить

- `single_token/` — базовий приклад із одним `access_token`.
- `single_token_bearer/` — приклад, де Swagger `Authorize` приймає лише Bearer token.
- `pair_tokens/` — приклад із парою `access_token + refresh_token`.
- `pair_tokens_stateless/` — пара токенів без збереження `refresh_token` у БД.
- `pair_tokens_cookies/` — пара токенів у `HttpOnly` cookies.
- `hot_swap_bundle/` — один фінальний файл з робочим прикладом + коментовані блоки для hot swap.
- `lesson_plan.md` — план заняття з поясненням кожного кроку.

## Встановлення

```bash
poetry install
```

У прикладах використовується `pwdlib[argon2]` для хешування паролів.

## Запуск

### Варіант 1: Single token

```bash
cd single_token
uvicorn app:app --reload
```

Swagger: `http://127.0.0.1:8000/docs`

### Варіант 2: Pair tokens

```bash
cd pair_tokens
uvicorn app:app --reload --port 8001
```

Swagger: `http://127.0.0.1:8001/docs`

### Варіант 1b: Single token with HTTPBearer

```bash
cd single_token_bearer
uvicorn app:app --reload --port 8004
```

Swagger: `http://127.0.0.1:8004/docs`

### Варіант 3: Pair tokens (stateless refresh)

```bash
cd pair_tokens_stateless
uvicorn app:app --reload --port 8002
```

Swagger: `http://127.0.0.1:8002/docs`

### Варіант 4: Pair tokens in cookies

```bash
cd pair_tokens_cookies
uvicorn app:app --reload --port 8003
```

Swagger: `http://127.0.0.1:8003/docs`

### Варіант 5: Hot swap bundle

```bash
cd hot_swap_bundle
uvicorn app:app --reload --port 8005
```

Swagger: `http://127.0.0.1:8005/docs`

Конфіг у `hot_swap_bundle` реалізовано через `pydantic-settings`.
За потреби можна перевизначити значення через `.env`:

```env
DATABASE_URL=sqlite:///./hot_swap_bundle.db
SECRET_KEY=super_secret_value
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_MINUTES=10080
```

### Hot swap usage without manual code edits

У `hot_swap_bundle/config.py` є зона:

```python
ACTIVE_SCENARIO = "pair_tokens_stateless"
# ACTIVE_SCENARIO = "single_token"
# ACTIVE_SCENARIO = "pair_tokens_db"
# ACTIVE_SCENARIO = "pair_tokens_cookies"
# ACTIVE_SCENARIO = "single_token_bearer"
```

Потрібно лише залишити **один** активний рядок сценарію.  
`app.py` і `auth.py` автоматично підлаштовують:
- `response_model` для `/login` і `/refresh-token`;
- логіку refresh-токенів (stateless або DB);
- джерело токена (`Authorization` header або cookies);
- доступність `/logout`.

## Ключові маршрути

### Single token

- `POST /signup`
- `POST /login`
- `GET /secret` (потрібен access token)

### Single token bearer

- `POST /signup`
- `POST /login` (отримати `access_token`)
- `Authorize` у Swagger: вставити тільки токен `Bearer <access_token>`
- `GET /secret`

### Pair tokens

- `POST /signup`
- `POST /login` (повертає access + refresh)
- `POST /refresh-token` (новий access)
- `GET /secret` (потрібен access token)

### Pair tokens stateless

- `POST /signup`
- `POST /login` (повертає access + refresh)
- `POST /refresh-token` (новий access, refresh у БД не зберігається)
- `GET /secret` (потрібен access token)

### Pair tokens in cookies

- `POST /signup`
- `POST /login` (ставить `access_token` і `refresh_token` в `HttpOnly` cookies)
- `POST /refresh-token` (оновлює токени в cookies)
- `POST /logout` (очищає cookies)
- `GET /secret` (читає `access_token` з cookie)

## Важливо для продакшн-версії

- Винести `SECRET_KEY` у `.env`.
- Додати ротацію/відкликання refresh токенів.
- Додати rate limiting для `login`.
- Додати тести для сценаріїв безпеки.
- Для cookies-режиму додати CSRF-захист (double submit token або аналог).
