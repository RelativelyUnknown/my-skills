# Python versions

Use features available at `python.target` and nothing newer. No `sys.version_info` branches, compatibility imports or backports unless a dependency requires them. Do not add `from __future__ import annotations` just for `|` unions. A target below 3.10 is end of life: ask first.

| Needs | Minimum | Older form |
| --- | --- | --- |
| `X \| None`, `match`, `zip(strict=True)`, `dataclass(slots=True, kw_only=True)` | 3.10 | |
| `tomllib`, `datetime.UTC`, `typing.Self`, `StrEnum`, `ExceptionGroup`, `e.add_note()`, `asyncio.TaskGroup`, `asyncio.timeout`, `datetime.fromisoformat` parsing a trailing `Z` | 3.11 | `timezone.utc`; `fromisoformat(s.replace("Z", "+00:00"))` |
| `def f[T]`, `class C[T]`, `type X = ...`, `@typing.override`, `itertools.batched` | 3.12 | `TypeVar`; no `@override`; `while batch := list(islice(it, n))` |
