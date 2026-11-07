# Errors and validation

Rules beyond the ones in `SKILL.md`: where to validate, how to keep the cause, and what to do when one item in a batch fails. Each block runs as written (Python 3.13, 7 November 2026).

## Contents

- Parse once, at the edge
- Keep the cause and add context
- A batch where some items fail

## Parse once, at the edge

Turn raw input into a domain type where it enters, and raise one error that says what was expected and what arrived. Inner code then takes the typed value and does not re-check it. Convert library errors once, at the layer boundary, not at every call site.

```python
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation


@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str

    @classmethod
    def parse(cls, raw: str) -> "Money":
        try:
            number, currency = raw.split()
            return cls(Decimal(number), currency)
        except (ValueError, InvalidOperation) as error:  # only the lines that can fail are inside
            raise ValueError(f"expected '<amount> <CURRENCY>' like '12.50 EUR', got {raw!r}") from error


assert Money.parse("12.50 EUR") == Money(Decimal("12.50"), "EUR")
try:
    Money.parse("twelve")
except ValueError as error:
    assert "got 'twelve'" in str(error)
```

## Keep the cause and add context

`raise ... from error` keeps the original as `__cause__` and shows both tracebacks. `raise ... from None` hides the context; use it only when the original is noise for the caller. `error.add_note("...")` (3.11+) adds context to an exception you re-raise without wrapping it in a new type.

```python
from pathlib import Path


def load(path: str) -> str:
    try:
        return Path(path).read_text(encoding="utf-8")
    except FileNotFoundError as error:
        error.add_note(f"while loading the settings file {path!r}")
        raise


try:
    load("/nonexistent/settings.toml")
except FileNotFoundError as error:
    assert error.__notes__ == ["while loading the settings file '/nonexistent/settings.toml'"]


def wrapped() -> None:
    try:
        int("x")
    except ValueError as error:
        raise RuntimeError("bad config value") from error


try:
    wrapped()
except RuntimeError as error:
    assert isinstance(error.__cause__, ValueError)
```

## A batch where some items fail

Decide first whether the batch is all or nothing. If it is not, process every item, collect the failures, and report them together at the end; do not stop at the first one and do not swallow them. `ExceptionGroup` (3.11+) carries all of them, and `except*` handles them by type.

```python
from collections.abc import Callable, Iterable


def process_all[T](items: Iterable[T], handle: Callable[[T], None]) -> int:
    done = 0
    errors: list[Exception] = []
    for item in items:
        try:
            handle(item)
        except Exception as error:  # noqa: BLE001 - collected and re-raised below
            error.add_note(f"item: {item!r}")
            errors.append(error)
        else:
            done += 1
    if errors:
        raise ExceptionGroup(f"{len(errors)} of {done + len(errors)} items failed", errors)
    return done


def handle(n: int) -> None:
    if n % 2:
        raise ValueError(n)


try:
    process_all(range(5), handle)
except* ValueError as group:
    assert [e.args[0] for e in group.exceptions] == [1, 3]
```

A script exits non-zero when any item failed and prints one line per failure; an API answers with the successes and the failures, not an error for the whole request. Retries and timeouts around the calls belong to the application bundle, if installed.
