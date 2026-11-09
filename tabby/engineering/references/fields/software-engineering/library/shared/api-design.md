# API design

A public name is a promise. Make the common call short, the wrong call hard to write, and every name say what it does. Users will not read its source.

## Before merging a new public name

1. Write the call site first, in a test or the README. Awkward to write means the interface is wrong.
2. Read it aloud: `save(report, overwrite=True)` reads well; `process(x, True)` does not.
3. Trigger the main error: does the message say how to fix the call?

## Surface

- Every public module defines `__all__`. `__init__.py` holds imports and `__all__`, no logic. Export only what users need, and the types they annotate with.
- Flat import paths (`from pkg import Client`); internal modules start with an underscore. A name without one is API: do not expose internal state, return a copy or immutable view (`tuple(self._items)`).

## Functions

- Required arguments are positional; everything optional is keyword-only after `*`.
- Accept the widest type needed (`Iterable` to loop once, `Sequence` to index, `Mapping` to read); return the concrete type callers need.
- No positional booleans. A keyword-only flag that tunes a detail (`overwrite=False`) is fine; a flag that changes what the function does means two functions (`write_csv`, `write_json`).
- `Literal["csv", "json"]` for a small closed set; Enum only if large or shared.
- Signatures show in editor tooltips, so keep them readable: literal defaults (`timeout: float = 30`, never `timeout=DEFAULT_TIMEOUT` or a `None` that secretly means 30); named parameters, not a `**kwargs` pass-through (`Unpack[TypedDict]` for many options); `functools.wraps` or `ParamSpec` on decorators so the signature survives; no parameter named after a builtin (`id`, `type`, `format`, `input`).
- Units in names (`timeout_seconds`) or types (`timedelta`, `Path`). One concept, one name.
- Return a value or raise; `None` only when absence is a normal answer. No `(ok, value)` pairs or status strings. Use stdlib verbs: `load`/`dump`, `parse`/`format`, `get` with a default. Large or lazy results: an iterator named as a noun (`rows()`).

## Classes

- A class is for state across calls or an invariant its methods protect; otherwise functions.
- Required arguments go in `__init__` and are validated there. No two-phase setup (`Client()`, `set_token()`, `connect()`).
- Value objects: `@dataclass(frozen=True)`. Alternative constructor only for a real second input (`Config.from_env()`). Inherit only for a stable "is-a"; for reuse pass an object in. Property for cheap access, method for I/O.

## Errors

- Built-ins for plain misuse: `ValueError`, `TypeError`.
- A package with a public API defines one root exception, `PkgError`, that its errors inherit from; no deeper. Wrap a library exception only to add what the caller needs, with `raise ... from e`; otherwise let it propagate.
- Messages follow [errors.md](../../all/code/errors.md): bad value, valid choices, fix.

## Optional dependencies

- Keep the base install small. A heavy or niche dependency (pyarrow, pandas) goes in an extra in `[project.optional-dependencies]`, never in `dependencies`: `pip install "pkg[parquet]"`. Add it to the dev group so tests run.
- Import it inside the function that needs it. On failure raise `ImportError` from `e`, naming the extra: `pip install "pkg[parquet]"`. Name the extra in the docstring.
- Tests use `pytest.importorskip("pyarrow")` or CI with the extra installed; test the error path by hiding the module: `monkeypatch.setitem(sys.modules, "pyarrow", None)`.

## Typing and logging

- Ship `py.typed`, fully annotate public functions, type-check the package in CI.
- `logging.getLogger(__name__)` ([logging.md](../../all/code/logging.md)); never configure handlers or call `basicConfig`. Only the top-level `__init__.py` adds a `NullHandler`.

## Changing a public name

- New options: keyword-only with defaults (safe in a minor release). Never change a return type in a minor release (`list` to `Iterator`, `T` to `T | None`).
- Rename or remove: keep the old name for at least one minor release as a deprecated alias with `warnings.warn(..., DeprecationWarning, stacklevel=2)` naming the replacement. Update every caller, test, doc, the README and the changelog; the changelog says what users must change.
- Removal is breaking: get approval; versions and changelog rules are in [release.md](release.md).
