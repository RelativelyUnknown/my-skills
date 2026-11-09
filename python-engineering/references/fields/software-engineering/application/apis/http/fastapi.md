# FastAPI

FastAPI is still 0.x and releases often; read the installed version from the lock file before using a recent feature. The patterns below hold across recent releases.

## Application layout

```
src/<pkg>/
├── main.py           # create_app(): app, routers, middleware, exception handlers, lifespan
├── settings.py       # Settings(BaseSettings) and get_settings()
├── deps.py           # shared dependencies: DB session, current user
├── <resource>/       # one package per resource: router.py, schemas.py, service.py, models.py
└── ...
```

- One `APIRouter` per resource, included with a prefix and tags. Handlers stay thin: parse, authorize, call a service function, return a response model.
- Business logic lives in plain functions or classes that take a session or client as a parameter, so tests call them without HTTP.

## Dependencies and settings

```python
from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_", env_file=".env")
    database_url: str
    jwt_audience: str

@lru_cache
def get_settings() -> Settings:
    return Settings()

SettingsDep = Annotated[Settings, Depends(get_settings)]
SessionDep = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

@router.get("/orders/{order_id}")
async def read_order(order_id: int, session: SessionDep, user: CurrentUser) -> OrderOut:
    order = await orders.get_for_user(session, order_id=order_id, user_id=user.id)
    return OrderOut.model_validate(order)
```

- Declare dependencies with `Annotated[T, Depends(fn)]` aliases; reuse the alias everywhere.
- Required settings have no default, so a missing variable fails at startup. Tests override `get_settings`.
- Dependencies with cleanup use `yield` (a session that commits or rolls back).

## Lifespan

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http = httpx.AsyncClient(timeout=10)
    yield
    await app.state.http.aclose()
    await engine.dispose()

app = FastAPI(lifespan=lifespan)
```

`@app.on_event("startup")` is deprecated; use `lifespan`.

## Models and responses

- Separate input and output models (`OrderCreate`, `OrderOut`); never one model with optional everything.
- Annotate the return type or set `response_model`; FastAPI filters the output to that model. Use `model_config = ConfigDict(from_attributes=True)` on output models built from ORM objects.
- Constrain fields: `Annotated[int, Field(gt=0)]`, `Literal[...]`, `EmailStr`, max lengths on strings and lists.
- Pagination has a maximum page size enforced by the model.
- Status codes are explicit on non-200 routes (`status_code=201`).

## Errors

- `raise HTTPException(status_code=404, detail="order not found")` for simple cases.
- Domain exceptions (`OrderNotFound`, `PermissionDenied`) raised by services, mapped once with `@app.exception_handler(...)` to a stable JSON shape (`{"error": {"code": "...", "message": "..."}}`).
- Never return stack traces or database messages to clients.

## Running

- Development: `fastapi dev src/<pkg>/main.py` (needs `fastapi[standard]`), or `uvicorn <pkg>.main:app --reload`.
- Production: `fastapi run` or the server directly; see `deployment.md`.
- OpenAPI docs: keep `/docs` off or behind auth in production when the API is private (`docs_url=None`).

## Litestar and Starlette

- Litestar: same principles; dependencies via `Provide`, DTOs or msgspec `Struct` models for input/output, lifespan via `lifespan=[...]` context managers.
- Plain Starlette: no request validation built in; validate with Pydantic or msgspec explicitly in each endpoint.
