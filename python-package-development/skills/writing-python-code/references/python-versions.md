# Python versions

Use features available at `python.target` and nothing newer. No `sys.version_info` branches, compatibility imports or backports unless a dependency requires them. Do not add `from __future__ import annotations` just for `|` unions; from 3.14 annotations are evaluated lazily without it. A target below 3.11 is end of life (3.10 reached it in October 2026): ask first.

| Needs | Minimum | Older form |
| --- | --- | --- |
| `X \| None`, `match`, `zip(strict=True)`, `dataclass(slots=True, kw_only=True)` | 3.10 | |
| `tomllib`, `datetime.UTC`, `typing.Self`, `StrEnum`, `ExceptionGroup`, `e.add_note()`, `asyncio.TaskGroup`, `asyncio.timeout`, `datetime.fromisoformat` parsing a trailing `Z` | 3.11 | `timezone.utc`; `fromisoformat(s.replace("Z", "+00:00"))` |
| `def f[T]`, `class C[T]`, `type X = ...`, `@typing.override`, `itertools.batched` | 3.12 | `TypeVar`; no `@override`; `while batch := list(islice(it, n))` |
| `copy.replace()`, `@warnings.deprecated`, `typing.TypeIs`, `typing.ReadOnly`, TypeVar defaults | 3.13 | `dataclasses.replace`; `warnings.warn(..., DeprecationWarning, stacklevel=2)`; `TypeGuard` |
| Lazy annotations (no `__future__` import), t-strings (`string.templatelib`), `compression.zstd`, `uuid.uuid7()`, `except A, B:` without parentheses, `concurrent.interpreters`, `Path.copy`/`Path.move` | 3.14 | `from __future__ import annotations`; `shutil.copy2`/`shutil.move` |
| `lazy import` (PEP 810), `frozendict`, `sentinel`, `[*xs for xs in groups]`, UTF-8 as the default encoding, `profiling.sampling`, TypedDict `extra_items` | 3.15 | Plain imports; `types.MappingProxyType`; `object()` sentinels; `itertools.chain.from_iterable`; pass `encoding="utf-8"` explicitly |

Pass `encoding="utf-8"` to `open()` and `Path.read_text()` whenever `python.target` is below 3.15; the default differs by platform until then.
