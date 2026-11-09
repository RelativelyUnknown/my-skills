# Errors

- No bare `except:`. No `except Exception:` except at a top-level boundary that logs or reports and then re-raises or exits. Never `except: pass`.
- Catch narrowly, close to the source. Keep `try` blocks short; the success path goes in `else`.
- Never return `None`, `[]`, `{}` or `""` from an except block so the caller appears to work. Absence that is a normal answer is handled by name (`except FileNotFoundError`) and documented.
- Required data crashes when missing: `d["key"]`, not `d.get("key", "")`. No silent fallbacks: no stub imports, no defaults that mask missing config, no mock data in production code.
- No `hasattr`, `getattr` or `isinstance` to paper over an unknown type; find out what the type is.
- Let library exceptions propagate. Add a custom exception only when callers must handle a condition no existing exception expresses; wrap with `raise ... from e`, or attach context with `e.add_note(...)`.
- Error messages name the bad value, the valid choices and the fix: `f"unknown region {region!r}; expected one of {sorted(REGIONS)}"`.

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

A script exits non-zero when any item failed and prints one line per failure; an API answers with the successes and the failures, not an error for the whole request. Retries and timeouts around the calls: [service-snags.md](../../application/shared/service-snags.md).
