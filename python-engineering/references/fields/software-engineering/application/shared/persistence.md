# Persistence: SQLAlchemy 2.x, SQLModel, Alembic

## Models

```python
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    status: Mapped[str] = mapped_column(String(20))
    lines: Mapped[list["OrderLine"]] = relationship(back_populates="order")
```

- 2.x style only: `Mapped[...]` and `mapped_column`, `select()` statements, `session.execute(...)`/`session.scalars(...)`. No legacy `session.query(...)` in new code.
- Constraints in the schema (`nullable=False`, unique constraints, foreign keys, check constraints), not only in Pydantic.

## Sessions

```python
engine = create_async_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_session() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as session:
        yield session
```

- One engine per process, created at import or in the lifespan; one session per request through a dependency.
- The service decides the transaction boundary: `async with session.begin():` around a unit of work, or an explicit `commit()`.
- `expire_on_commit=False` for async sessions, so attributes stay readable after commit.
- Async code never triggers lazy loading; load relationships explicitly with `selectinload`/`joinedload` in the query.
- Use an async driver with async sessions (`asyncpg`, `psycopg` 3 async, `aiosqlite`); a sync driver blocks the event loop.

## Queries

- Filter by owner or tenant in the query itself (`select(Order).where(Order.id == order_id, Order.owner_id == user_id)`).
- Paginate with keyset pagination (`WHERE id > :last_id ORDER BY id LIMIT :n`) for large tables; offset pagination degrades with depth.
- Batch inserts and updates with `insert(...).values([...])` or `session.add_all`; no per-row commits.
- Never build SQL with f-strings; use bound parameters (`text("... WHERE id = :id")`, `.params(id=...)`).

## SQLModel

SQLModel combines a SQLAlchemy model and a Pydantic model in one class. Keep table models (`table=True`) separate from API input and output models, or the API exposes every column.

## Migrations (Alembic)

- Every schema change ships a migration generated with `alembic revision --autogenerate -m "..."` and then read: autogenerate misses renames (it sees drop plus add), some type changes, server defaults and constraints on some backends.
- Never edit a migration that has run in a shared environment; add a new one.
- Run migrations as a separate deployment step (a job or init container), not on application startup, where several workers race.
- Zero-downtime changes go in phases: add a nullable column and deploy code that writes both; backfill; switch reads; drop the old column later.
- Test migrations: upgrade from an empty database to head in CI, and `alembic check` (Alembic 1.9+) to catch models without migrations.
