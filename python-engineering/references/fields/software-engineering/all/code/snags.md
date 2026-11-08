# Snags

A snag is a habit that looks fine and makes the next reader stop: the code runs, but it is wrong, noisy or misleading. Check this list before you finish each function.

## Signatures

- Defaults are literals: `timeout: float = 30`. Never a `DEFAULT_*` constant, a stand-in `None` that secretly means 30, a call (`now=datetime.now()` runs once, at import), or `[]` / `{}`.
- Name every parameter: no `**kwargs` pass-through, none called `id`, `type` or `format`. A closed set of strings is `Literal["a", "b"]`. Past two or three parameters, make the rest keyword-only; never a positional boolean.
- A decorator uses `functools.wraps`, so hover and help keep the real signature.
- One return type per function: no flag that changes it, no tuple of three or more values (use a dataclass or `NamedTuple`), no bare `-> dict`.
- Constructors and properties are cheap: no network or disk I/O hidden in `Client()` or a property.

## Errors

- Wrap only the line that can raise, and catch the named exception. Never `except Exception: pass`, never return a default from `except`, never `raise Exception(...)`; re-raise with `raise ... from e`.
- Log once, at the boundary, or raise; not both. Log a caught error with `logger.exception`, not `logger.error(str(e))`.
- Required data fails where it is missing: `payload["name"]`, not `payload.get("name", "")`. No `x = x or 30` (it replaces `0`).
- Validate with `if ...: raise ValueError(...)`, never `assert` (`python -O` strips it).

## Time, files, network, processes

- Every network call has a timeout, and its result is checked: `raise_for_status()`, `subprocess.run(..., check=True)`.
- `open(path, encoding="utf-8")` inside `with`; use any iterator while its file is still open. A sqlite3 `with` commits but does not close the connection.
- Time is timezone-aware: `datetime.now(UTC)`, never `utcnow()`.
- Nothing runs at import: no environment or file reads, connections, `logging.basicConfig()` or background work at module level.
- Retries are bounded, back off, and repeat only operations that are safe to repeat.
- Secrets stay out of logs, URLs and exception messages. No string-built SQL or shell commands, no `shell=True` with input, no `random` for tokens (use `secrets`).

## Structure

- No class with no state and one method (write a function). No one-line wrapper around an expression. No base class, factory or registry with one implementation. No `utils.py` or `helpers.py`.
- No module-level mutable state; pass it in. No `dict[str, Any]` passed around; use a dataclass or `TypedDict`.
- Names say what a thing is: not `data`, `result`, `info`, `manager`, `new_`, `v2`. Name a number that carries meaning.
- No defensive code for cases that cannot happen. Search for an existing helper before writing one.
- Compare values with `==`; use `is` for `None` only. Do not mutate an argument the caller passed in.

## Comments and docs

- Say what is not obvious, or say nothing: no narrating comments (`# Step 1`), no commented-out code, no leftover `print`, no `TODO` litter.
- No conversation residue ("as discussed", "now uses", "previously") or inflated claims ("robust", "production-ready"). Do not restate the signature in the docstring.

## Tests

- A test must be able to fail: assert the result, not that a mock was called. No sleeps, real clock or unseeded randomness; restore anything you change (`monkeypatch`, `tmp_path`).

Mechanical ones are cheapest in config: enable ruff `B`, `BLE`, `S`, `DTZ`, `A`, `FBT`, `ANN401`, `SIM115`, `PLW1514`, `RUF006`, `T20`, `TRY`.
