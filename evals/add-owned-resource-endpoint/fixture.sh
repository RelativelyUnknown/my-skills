#!/usr/bin/env bash
# Builds a small FastAPI app with auth and an async SQLAlchemy session in the empty workspace.
set -euo pipefail
mkdir -p app tests
cat > pyproject.toml <<'__FIXTURE_EOF__'
[project]
name = "shopapi"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = ["fastapi>=0.115", "sqlalchemy[asyncio]>=2.0", "aiosqlite"]

[dependency-groups]
dev = ["pytest", "pytest-asyncio", "httpx", "ruff", "mypy"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
__FIXTURE_EOF__
touch app/__init__.py
cat > app/models.py <<'__FIXTURE_EOF__'
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(index=True)
    total: Mapped[int]
    internal_notes: Mapped[str] = mapped_column(default="")
__FIXTURE_EOF__
cat > app/main.py <<'__FIXTURE_EOF__'
from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.models import Base

engine = create_async_engine("sqlite+aiosqlite:///shop.db")
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

app = FastAPI()


class User:
    def __init__(self, id: int) -> None:
        self.id = id


async def get_session() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as session:
        yield session


async def get_current_user(x_user_id: Annotated[int | None, Header()] = None) -> User:
    if x_user_id is None:
        raise HTTPException(status_code=401, detail="authentication required")
    return User(x_user_id)


SessionDep = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@app.on_event("startup")
async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
__FIXTURE_EOF__
cat > tests/test_placeholder.py <<'__FIXTURE_EOF__'
def test_placeholder() -> None:
    assert True
__FIXTURE_EOF__
git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
