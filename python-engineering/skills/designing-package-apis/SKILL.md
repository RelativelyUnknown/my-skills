---
name: designing-package-apis
description: "Designs the public surface of a Python library: exports, __all__, signatures, exceptions, optional dependencies, logging, typing, deprecation. Use when adding, renaming, changing or removing a public function, class, exception or extra, or when a user-facing error or import path changes."
argument-hint: "[python=3.12 types=mypy]"
---

# Designing package APIs

A public name is a promise. Make the common call short, the wrong call hard to write, and every name say what the thing does. People who use the package did not write it and will not read its source.

## Start

Run `python3 <this skill's folder>/scripts/detect_project.py` from the project root (`python.target`, `types`, `layout`, `tools.missing`; `# default` means nothing was found). Arguments (`key=value` after the skill name) override detected facts. Use idioms available at `python.target`. Changing a public API (rename, removal, changed return type) needs the user's approval; adding is safe.

## Before merging a new public name

1. Write the call site first, in a test or the README. If it is awkward to write, the interface is wrong.
2. Read it aloud: `save(report, overwrite=True)` reads clearly; `process(x, True)` does not.
3. Trigger the main error on purpose. Does the message tell the user how to fix the call?

## Surface

- Every public module defines `__all__`. `__init__.py` holds imports and `__all__` and no logic. Export only what users need, and re-export the types they annotate with.
- Keep import paths flat (`from pkg import Client`). Prefix internal modules with an underscore.
- Attributes without a leading underscore are API; do not expose internal state. Return a copy or an immutable view (`tuple(self._items)`), not the internal list.

## Functions

- Required arguments are positional. Everything optional is keyword-only after `*`.
- Accept the widest type the function needs (`Iterable` if it loops once, `Sequence` if it indexes, `Mapping` if it only reads); return the concrete type callers need.
- No positional booleans. A keyword-only flag that tunes a detail (`overwrite=False`) is fine; a flag that changes what the function does means two functions (`write_csv`, `write_json`).
- `Literal["csv", "json"]` for a small closed set of strings; an Enum only when the set is large or shared.
- Signatures are read in an editor's hover tooltip, so keep them readable: literal defaults (`timeout: float = 30`, never `timeout=DEFAULT_TIMEOUT`, and never `None` that secretly means 30); named parameters instead of a `**kwargs` pass-through (`Unpack[TypedDict]` when there are many options); `functools.wraps` or `ParamSpec` on decorators so the original signature survives; no parameter named after a builtin (`id`, `type`, `format`, `input`).
- Put units in names (`timeout_seconds`) or let the type carry them (`timedelta`, `Path`). One concept, one name across the package.
- Return a value or raise; return `None` only when absence is a normal answer. No `(ok, value)` pairs or status strings. Use the stdlib's verbs: `load`/`dump`, `parse`/`format`, `get` with a default. Large or lazy results are an iterator named as a noun (`rows()`).

## Classes

- A class exists for state that persists across calls or an invariant its methods protect; otherwise write functions.
- Required arguments go in `__init__` and are validated there. No two-phase setup (`Client()`, then `set_token()`, then `connect()`).
- Value objects are `@dataclass(frozen=True)`. Add an alternative constructor only for a real second input (`Config.from_env()`). Inherit only for a stable "is-a"; for reuse, pass an object in. Property for cheap access, method when it does I/O.

## Errors

- Built-ins for plain misuse: `ValueError` for a bad value, `TypeError` for a wrong type.
- A package with a public API defines one root exception, `PkgError`, that its own errors inherit from; go no deeper. Wrap a library exception only to add information the caller needs, with `raise ... from e`; otherwise let it propagate.
- Messages follow the error-message rule in `writing-python-code`: bad value, valid choices, fix.

## Optional dependencies

- Keep the base install small. A heavy or niche dependency (pyarrow, pandas, ...) goes in an extra in `[project.optional-dependencies]`, never in `dependencies`: `pip install "pkg[parquet]"`. Add it to the dev group too so tests can run.
- Import it inside the function that needs it, not at module top. If the import fails, raise `ImportError` chained with `from e`, with a message that names the extra: `pip install "pkg[parquet]"`. Name the extra in the function's docstring.
- Tests for such a function use `pytest.importorskip("pyarrow")` or run with the extra installed in CI; the error path is tested by hiding the module with `monkeypatch.setitem(sys.modules, "pyarrow", None)`.

## Typing and logging

- Ship `py.typed`, annotate every public function completely, and run the type checker on the package in CI.
- Library code uses `logging.getLogger(__name__)` (see `writing-python-code`, `references/logging-and-security.md`) and never configures handlers or calls `basicConfig`. The top-level `__init__.py` adds a `NullHandler` to the package logger, and nowhere else.

## Changing a public name

- New options are keyword-only with defaults, which is safe in a minor release. Do not change a return type in a minor release (`list` to `Iterator`, `T` to `T | None`).
- Renaming or removing: keep the old name working for at least one minor release as a deprecated alias that emits `DeprecationWarning` naming the replacement (`warnings.warn(..., DeprecationWarning, stacklevel=2)`). Update every caller, test, doc, the README and the changelog; the changelog entry says what users must change.
- Removal is a breaking change: get approval, and see `releasing-python-packages` for the version and changelog rules.
