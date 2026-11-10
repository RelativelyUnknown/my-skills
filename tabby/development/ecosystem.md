# The ecosystem, job by job

What a senior engineer knows without looking it up: for each job, what the language already provides, what the community treats as standard, and where each stops fitting. Use it with the ladder in [code/reuse.md](code/reuse.md), then check the installed versions and the Python target before relying on any of it ([workflow/checking-apis.md](workflow/checking-apis.md)).

Python rows were run on Python 3.13.18 on 10 November 2026 where they say so; library names and the Rust, C++ and Zig lists are from knowledge of the ecosystem and were not run here.

## Python

| Job | Standard library | Community standard | Stops fitting when |
| --- | --- | --- | --- |
| Order tasks by dependency | `graphlib.TopologicalSorter` (raises `CycleError`, run) | | you need a graph database |
| Batch, group, count, dedupe | `itertools.batched` (3.12+), `collections.Counter`, `dict.fromkeys` for ordered dedupe (run) | | the data does not fit in memory: a data frame or a database |
| Statistics, search, top-n | `statistics.fmean`, `quantiles`, `bisect.insort`, `heapq.nlargest` (run) | numpy, pandas or polars for arrays and tables | arrays of millions: numpy |
| Split command lines, quote | `shlex.split`, `shlex.quote` (run) | | never hand-roll quoting |
| Compare or fuzzy-match text | `difflib.unified_diff`, `get_close_matches` (run) | rapidfuzz for speed at scale | large corpora |
| Config files | `tomllib` (3.11+, read-only, run) | PyYAML for YAML | you must write TOML back |
| Time zones, ISO dates | `zoneinfo`, `datetime.fromisoformat` (3.11+ parses `Z`) | python-dateutil, dateparser for free-form text | recurrence rules, human phrases |
| Files and processes | `pathlib`, `tempfile`, `shutil`, `subprocess.run(check=True, timeout=...)` | | |
| One HTTP GET in a script | `urllib.request` with `timeout=` | | retries, pooling, HTTP/2, async: httpx or requests |
| HTTP in an application | | httpx (sync and async), requests (sync) | |
| Retries with backoff | a loop with a cap and a named exception | tenacity, `urllib3.util.Retry` | several call sites or jitter |
| Parse CLI arguments | `argparse` | click, typer | many subcommands, completion |
| Validate input | `if ... raise`, frozen dataclass | pydantic | see the validation ladder in `code/reuse.md` |
| Caching | `functools.cache` (run) | cachetools (expiry, size), Redis (shared) | several processes or workers |
| Concurrency | `concurrent.futures`, `asyncio.TaskGroup` and `asyncio.timeout` (3.11+) | anyio | CPU-bound: processes; free-threaded builds |
| Tokens, IDs, secrets | `secrets`, `uuid` | | passwords and encryption: argon2-cffi, bcrypt, cryptography |
| Tables in a file or database | `csv`, `sqlite3` | SQLAlchemy, psycopg, asyncpg | many relationships and migrations: an ORM and Alembic |
| Tests | `unittest`, `unittest.mock` | pytest, time-machine, respx or responses, hypothesis | |

## Three runtime facts that decide designs

- **Import time counts.** A command-line tool pays it on every run. Measure with `python -X importtime -c "import json"` (it prints per-module microseconds; run). Import heavy libraries inside the function that needs them.
- **The GIL.** Threads do not run Python bytecode in parallel in the default build: use processes for CPU-bound work, threads or asyncio for waiting on I/O. Free-threaded builds exist from 3.13 (`sys._is_gil_enabled()` reports which you have; it printed `True` on the default build used here); a library supports them only if its extension modules say so.
- **What crosses a process boundary must be picklable.** `pickle.dumps(lambda x: x)` raises `PicklingError` (run), so a lambda or a local function cannot go to a `ProcessPoolExecutor`. Pass module-level functions and plain data.

## Other languages (not run here)

- **Rust:** the standard library is small by design; the community standard is the norm. serde (serialization), thiserror for library errors and anyhow for applications, clap (CLI), tokio (async runtime), rayon (data parallelism), tracing (logs). PyO3 and maturin for Python bindings.
- **C++:** the standard library, then fmt, abseil or Boost components; nanobind or pybind11 for Python bindings ([library/native/cpp.md](library/native/cpp.md)).
- **C:** the standard library and the platform; libraries are linked, not copied; the CPython C API or cffi for Python.
- **Zig:** the standard library is the ecosystem for now; Ziggy Pydust for Python bindings ([library/native/zig.md](library/native/zig.md)).
