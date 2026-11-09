# Configuration patterns

## A standard-library loader that reports every problem

Runs as written (checked 7 November 2026, Python 3.13).

```python
import os
import tomllib
from collections.abc import Mapping
from dataclasses import dataclass, field

TRUE = {"1", "true", "yes", "on"}
FALSE = {"0", "false", "no", "off", ""}

class ConfigError(Exception):
    pass

@dataclass(frozen=True)
class Config:
    database_url: str
    api_key: str = field(repr=False)  # a secret stays out of repr and logs
    debug: bool = False
    workers: int = 2

def load(env: Mapping[str, str], file_text: str = "") -> Config:
    """Environment over file over defaults; every problem reported together."""
    file = tomllib.loads(file_text)
    problems: list[str] = []

    def get(name: str) -> str | None:
        return env.get(f"APP_{name.upper()}", file.get(name))

    def required(name: str) -> str:
        value = get(name)
        if value is None:
            problems.append(f"APP_{name.upper()} is missing")
            return ""
        return str(value)

    def integer(name: str, default: int) -> int:
        raw = get(name)
        try:
            return default if raw is None else int(raw)
        except ValueError:
            problems.append(f"APP_{name.upper()}={raw!r} is not an integer")
            return default

    def boolean(name: str, default: bool) -> bool:
        raw = get(name)
        if raw is None:
            return default
        if isinstance(raw, bool):
            return raw
        if raw.lower() in TRUE | FALSE:
            return raw.lower() in TRUE
        problems.append(f"APP_{name.upper()}={raw!r} is not a boolean")
        return default

    config = Config(
        database_url=required("database_url"),
        api_key=required("api_key"),
        debug=boolean("debug", False),
        workers=integer("workers", 2),
    )
    if problems:
        raise ConfigError("; ".join(problems))
    return config

try:
    load({"APP_WORKERS": "x"})
except ConfigError as error:
    assert str(error) == (
        "APP_DATABASE_URL is missing; APP_API_KEY is missing; APP_WORKERS='x' is not an integer"
    )

config = load({"APP_DATABASE_URL": "sqlite://", "APP_API_KEY": "s3cret", "APP_DEBUG": "false"}, "workers = 4")
assert config.debug is False and config.workers == 4 and "s3cret" not in repr(config)
```

## The same settings with pydantic-settings

Needs `pydantic-settings` (2.15.0 here). Run in an environment that has it.

```python
import os

from pydantic import SecretStr, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_", env_file=None, extra="forbid", frozen=True)

    database_url: str
    api_key: SecretStr
    debug: bool = False
    workers: int = 2

os.environ["APP_WORKERS"] = "x"
try:
    Settings()
except ValidationError as error:
    fields = {item["loc"][0] for item in error.errors()}
    assert fields == {"database_url", "api_key", "workers"}  # all three reported together

os.environ.update({"APP_DATABASE_URL": "sqlite://", "APP_API_KEY": "s3cret", "APP_DEBUG": "false", "APP_WORKERS": "4"})
settings = Settings()
assert settings.debug is False and settings.workers == 4
assert "s3cret" not in repr(settings) and settings.api_key.get_secret_value() == "s3cret"
assert Settings(workers=9).workers == 9  # constructor values beat the environment
```
