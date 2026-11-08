# Typing patterns

Each block passes `mypy --strict` (mypy 2.4.1, Python 3.13), checked 7 November 2026.

## Generics, aliases and Self (3.12)

```python
from collections.abc import Sequence
from typing import Self

def first[T](xs: Sequence[T]) -> T:
    return xs[0]

class Box[T]:
    def __init__(self, item: T) -> None:
        self.item = item

    def set(self, item: T) -> Self:
        self.item = item
        return self

type Pair[T] = tuple[T, T]
pair: Pair[int] = (first([1]), 2)
```

## Closed sets with exhaustive match

```python
from enum import Enum
from typing import assert_never

class Color(Enum):
    RED = "red"
    BLUE = "blue"

def hex_of(color: Color) -> str:
    match color:
        case Color.RED:
            return "#f00"
        case Color.BLUE:
            return "#00f"
        case _:
            assert_never(color)  # a new member makes mypy fail here
```

## TypedDict and NewType

```python
from typing import NewType, NotRequired, TypedDict

UserId = NewType("UserId", int)

class Config(TypedDict):
    host: str
    port: NotRequired[int]

def port_of(config: Config) -> int:
    return config.get("port", 80)

def load(user: UserId) -> str:
    return str(user)

load(UserId(3))
```

## TypeIs on a sequence

```python
from collections.abc import Sequence
from typing import TypeIs

def is_strs(items: Sequence[object]) -> TypeIs[Sequence[str]]:
    return all(isinstance(item, str) for item in items)

def join(items: Sequence[object]) -> str:
    if is_strs(items):
        return ",".join(items)  # narrowed to Sequence[str]
    return ""
```

## A typed decorator

```python
import functools
from collections.abc import Callable

def logged[**P, R](fn: Callable[P, R]) -> Callable[P, R]:
    @functools.wraps(fn)
    def inner(*args: P.args, **kwargs: P.kwargs) -> R:
        return fn(*args, **kwargs)

    return inner

@logged
def add(a: int, *, b: int = 0) -> int:
    return a + b

add(1, b=2)  # the keyword-only signature is kept; add(1, 2) would fail the check
```

## A callable Protocol and @override

```python
from typing import Protocol, override

class Handler(Protocol):
    def __call__(self, name: str, *, retries: int = 3) -> bool: ...

def run(handler: Handler) -> bool:
    return handler("job", retries=1)

def impl(name: str, *, retries: int = 3) -> bool:
    return bool(name) and retries > 0

run(impl)

class Base:
    def go(self) -> int:
        return 1

class Child(Base):
    @override
    def go(self) -> int:  # a typo in the name fails the check
        return 2
```

## Strict mode, incrementally

```toml
[tool.mypy]
python_version = "3.12"
strict = true
enable_error_code = ["explicit-override"]

[[tool.mypy.overrides]]
module = "pkg.legacy.*"
ignore_errors = true  # shrink this list; do not add new modules to it
```
