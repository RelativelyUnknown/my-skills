# Faster libraries

Next step after the standard library ([stdlib-first.md](../code/stdlib-first.md)) when a measured hot path is too slow. Job not listed, or entry does not fit: [replacement-packages.md](replacement-packages.md). Speed claims are the maintainers' own; your workload decides.

## Rules

1. **Profile first** ([profiling.md](profiling.md)). Name the function and the number: "`parse_rows` takes 4.1 s of 5 s". No measurement, no swap.
2. **Keep what the project has.** If it already uses a library for the job, use it. Recommend a replacement in the report; switch only when asked.
3. **The replacement earns the dependency**: maintained, widely used, compatible licence, wheels for every supported platform ([stdlib-first.md](../code/stdlib-first.md); checks in [replacement-packages.md](replacement-packages.md)).
4. **Same behavior, then speed.** Run the existing tests on the swap. Watch return types (`bytes` vs `str`), error types, rounding, time zones.
5. **Report before and after** on the same input, plus behavior differences.

## Tooling (defaults for new projects; existing projects keep theirs)

- pip, pip-tools, virtualenv, pyenv, poetry → uv: much faster installs; lockfile and Python management in one tool. Not when: the organization mandates conda or poetry plugins
- black, isort, flake8, pyupgrade → ruff (lint and format): one Rust binary. Not when: you rely on pylint-only checks; keep pylint for those
- pre-commit → prek: same config file, faster. Not when: a hook needs a pre-commit-only feature
- mypy or pyright for speed → ty (beta). Not when: it is the only gate; run it beside the existing checker

## Serialization and validation

- `json`, `ujson` → orjson: Rust; handles dataclasses, datetimes, UUIDs, NumPy natively. Not when: callers need `str` (orjson returns `bytes`), or custom `JSONEncoder` subclasses are everywhere
- pydantic models on a hot encode/decode path → msgspec `Struct`: faster, less memory. Not when: FastAPI models, settings, validators, coercion
- `pickle` between processes or services → msgspec (JSON or MessagePack): typed, portable, no code execution. Not when: round-tripping arbitrary Python objects inside one trusted program

## HTTP and async

- `requests` in async code → httpx `AsyncClient` or aiohttp. Not when: sync scripts; `requests.Session` is fine
- one client per request → one shared client per process: reuses connections and TLS; often the largest HTTP win
- default event loop → uvloop. Not when: Windows, or no measured loop overhead
- uvicorn → granian: Rust ASGI/WSGI server. Not when: you need uvicorn-specific features; measure the real app first

## Text, parsing, regex

- fuzzywuzzy, thefuzz → RapidFuzz: C++, near drop-in
- BeautifulSoup for speed → selectolax or lxml. Not when: malformed HTML where BeautifulSoup's leniency matters
- `re` on untrusted patterns or input → google-re2: linear time, no catastrophic backtracking. Not when: you need backreferences or lookaround

## Dates, numbers, hashing

- arrow, pendulum, `dateutil` → whenever: Rust-backed, DST-safe. Not when: APIs on both sides expect `datetime`; convert at the edges
- `strptime` for ISO 8601 → `datetime.fromisoformat` (most ISO formats from 3.11)
- Python loops over numbers → NumPy vectorization, then numba `@njit`. Not when: object or string data, tiny inputs, first-call JIT time matters
- `hashlib` for non-security keys or checksums → xxhash, blake3, `zlib.crc32`. Not when: anything security-related

## The interpreter

- Upgrade CPython: each release is usually faster. Check every dependency ships wheels for it.
- Free-threaded build (`python3.14t`) for CPU-bound threads: real parallelism. Single-thread overhead; one extension without free-threaded wheels re-enables the GIL.
- `ProcessPoolExecutor` for CPU-bound work on the standard build. Cost: pickling, start-up.
