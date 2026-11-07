# Faster libraries

The step after the standard library (`writing-python-code`, `references/stdlib-or-package.md`): what to use when a measured hot path is too slow. If a job is not listed or an entry does not fit the project, follow `finding-replacement-packages.md`. Speed figures are the maintainers' own benchmarks unless noted; your workload decides.

## Contents

- Rules
- Tooling
- Serialization and validation
- HTTP and async
- Text, parsing and regex
- Dates and times
- Numbers, hashing, images
- The interpreter

## Rules

1. **Profile first** (see `profiling-python-code`). Name the function and the number: "`parse_rows` takes 4.1 s of 5 s". No measurement, no swap.
2. **Keep what the project has.** If the project already uses a library for the job, use it. Recommend a replacement in the report; switch only when asked.
3. **The replacement must earn the dependency** (rules in `writing-python-code`): maintained, widely used, license compatible, wheels for every platform the project supports. How to check each is in `finding-replacement-packages.md`.
4. **Same behavior, then speed.** Run the existing tests on the swap. Watch for different return types (`bytes` vs `str`), error types, rounding and time-zone handling.
5. **Report before and after** on the same input, plus any behavior difference.

## Tooling

These are safe defaults for new projects; existing projects keep their tools unless asked.

- pip, pip-tools, virtualenv, pipx, pyenv, poetry → uv: Astral: 10-100x faster installs; lockfile and Python management in one tool. Not when: The organization mandates conda or poetry plugins
- black, isort, flake8, pyupgrade, most pylint checks → ruff (lint + format): One Rust binary; 10-100x faster than the tools it replaces (Astral). Not when: You rely on pylint-only checks; keep pylint for those
- pre-commit → prek: Same config file; about 10x faster, half the disk (maintainer); Home Assistant, Airflow and PDM switched. Not when: A hook needs a pre-commit-only feature
- mypy or pyright, for speed → ty (beta, 0.0.x): Astral: 10x-60x faster than mypy and Pyright uncached. Not when: As the only gate: it is beta. Run it beside the existing checker

## Serialization and validation

- `json` → orjson: Rust; serializes dataclasses, datetimes, UUIDs and NumPy natively; several times faster than `json` (maintainer benchmarks). Not when: Callers need `str` (orjson returns `bytes`); custom `JSONEncoder` subclasses everywhere
- `ujson` → orjson or msgspec: ujson's maintainers put it in maintenance mode and point users to orjson. Not when: 
- pydantic models on a hot decode/encode path → msgspec `Struct`: msgspec benchmarks: decode plus validation many times faster than pydantic v2, with less memory. Not when: FastAPI models, settings, validators and coercion: keep pydantic
- `pickle` between processes or services → msgspec (JSON or MessagePack): Typed, portable, not code-executing. Not when: You must round-trip arbitrary Python objects inside one trusted program

## HTTP and async

- `requests` in async code → httpx `AsyncClient` or aiohttp: Non-blocking; connection pooling; HTTP/2 in httpx. Not when: Sync scripts: `requests` with a `Session` is fine. Note httpx's last release was 0.28.1 (December 2024)
- asyncio's default event loop → uvloop: Maintainer: 2-4x faster loop. Not when: Windows (unsupported); no measured loop overhead
- uvicorn → granian: Rust HTTP server for ASGI/WSGI; maintainer benchmarks show higher throughput. Not when: You need uvicorn-specific features; measure under your real app first
- a new client per request → one shared client per process: Reuses connections and TLS sessions; usually the largest HTTP win. Not when: 

## Text, parsing and regex

- fuzzywuzzy / thefuzz → RapidFuzz: C++ implementation, near drop-in API, MIT license. Not when: 
- BeautifulSoup for parsing speed → selectolax (Lexbor) or lxml: Native parsers, CSS selectors. Not when: Malformed HTML where BeautifulSoup's leniency matters
- `re` on untrusted patterns or input → google-re2 (`re2`): Linear-time matching, no catastrophic backtracking. Not when: You need backreferences or lookaround
- string concatenation in loops → `"".join(parts)`, `io.StringIO`: Avoids quadratic copying. Not when: 

## Dates and times

- arrow, pendulum, `datetime` + `dateutil` → whenever: Rust-backed, DST-safe types; maintainer: 10-100x faster than Pendulum and Arrow. Not when: APIs on both sides expect `datetime`; convert at the edges or keep `datetime`
- `strptime` for ISO 8601 → `datetime.fromisoformat`: C implementation; parses most ISO formats from 3.11. Not when: Non-ISO formats

## Numbers, hashing, images

- Python loops over numbers → NumPy vectorization, then numba `@njit`: Removes interpreter overhead per element. Not when: Object or string data; tiny inputs; first-call JIT time matters
- `hashlib.md5`/`sha*` for non-security keys or checksums → xxhash, blake3, or stdlib `zlib.crc32`: Non-cryptographic hashes are much faster. Not when: Anything security-related: use `hashlib`
- Pillow for bulk resizing of large images → pyvips: Streams images; low memory. Not when: Simple one-off edits. Avoid pillow-simd: it trails mainline Pillow

## The interpreter

- Upgrade CPython: 3.11 averaged about 25% faster than 3.10 (What's New); later releases add smaller gains. Caveat: Check every dependency ships wheels for the new version
- 3.15 experimental JIT (`PYTHON_JIT=1`): What's New: from about 15% slower to over 100% faster depending on workload. Caveat: Experimental; measure your own code
- Free-threaded build (`python3.14t`, `python3.15t`) for CPU-bound threads: Real parallel threads; 3.15 adds a stable ABI (`abi3t`) for extensions. Caveat: Single-thread overhead; any extension without free-threaded wheels re-enables the GIL
- `multiprocessing`/`ProcessPoolExecutor` for CPU-bound work today: Sidesteps the GIL on the standard build. Caveat: Pickling cost; start-up time
