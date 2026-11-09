# Standard library first

Order: the project's own idiom, the standard library, a widely used package, then your own code. Match what the project already uses for validation, HTTP, CLI and config; do not add a second mechanism.

- Read `pyproject.toml` first. Before hand-rolling a utility or adding a package, apply the ladder below: a package for a few lines is as wrong as a regex parser for dates.
- Never regex-parse structured formats: dates, URLs, HTML, JSON, CSV, versions.
- Flag every new dependency in the report, with the reason.

Examples and a rule, not a boundary. A package for a few lines is as wrong as a hand-rolled parser for a hard format. Decide in this order.

1. **The project's own idiom first.** If its code already validates, parses, retries or serialises with a library, use that for new code. Do not add a second mechanism, and do not rewrite working code to switch. A project with pydantic models gets a pydantic model; a project without pydantic does not get it for one function.
2. **Stay in the standard library while the job is small**: roughly under 15 lines, one or two call sites, and none of the hard parts (security, time zones, text formats, network protocols).
3. **A package earns its place** when at least one holds:
   - the job is hard to get right and mistakes are subtle or costly (password hashing, tokens, HTML sanitising, time zones and recurrence, free-form dates, XML from untrusted sources, HTTP with retries and pooling);
   - the same job repeats at three or more places, so one shared mechanism removes more code than it adds;
   - it is the ecosystem standard readers expect (pytest, ruff, httpx for async HTTP);
   - it replaces more code than it adds, counting the tests the hand-rolled version would need.
4. **Weigh the cost.** A dev-only dependency costs users nothing; a runtime one does. A library's dependencies become its users', so keep the base install small and put heavy ones in extras; an application or a single-file script may take more (`# /// script` metadata, PEP 723, declares a script's dependencies inline). Also count install size, import time, transitive packages, licence and maintenance health (see [dependencies.md](../dependencies/dependencies.md)).
5. **Say so when you add one**, with the reason from step 3.

## Validation ladder

- One function, one to three arguments: `if not ...: raise ValueError(f"unknown region {region!r}; expected one of {sorted(REGIONS)}")` in the function
- A few related records you construct yourself: a frozen dataclass with `__post_init__` checks
- Untrusted nested JSON, many models, coercion, error lists, schema output: pydantic, or the validator the project already uses
- A config file: `tomllib` and a dataclass
- Command-line arguments: argparse `type=` and `choices=`

## Common jobs

- HTTP: `urllib.request` for one GET in a script, with `timeout=`. Package when: retries, pooling, async, HTTP/2: httpx or requests, with `raise_for_status()`
- HTTP retries: a loop with a cap, backoff and a named exception. Package when: several call sites, or jitter: `tenacity`, `urllib3.util.Retry` via `HTTPAdapter`, httpx `HTTPTransport(retries=...)` for connection errors
- URLs: `urllib.parse`, or the client's `params=`. Package when: never string concatenation
- Dates and times: `datetime.fromisoformat` (3.11+ parses `Z`), `strptime` for known formats, `zoneinfo`. Package when: free-form text or recurrence: `dateparser`, `python-dateutil`
- Paths and files: `pathlib`, `tempfile`, `shutil`
- Subprocesses: `subprocess.run(..., check=True, timeout=...)`, `shlex`
- CLI: `argparse`. Package when: many subcommands, completion, or the project already uses click or typer
- Data formats: `json`, `csv`, `html.parser`, `packaging.version`, `tomllib`. Package when: YAML, untrusted XML (`defusedxml`), scraping HTML (`beautifulsoup4`); never `line.split(",")`
- Collections: `Counter`, `defaultdict`, `itertools`, `itertools.batched` (3.12+; older: an `islice` loop)
- Caching: `functools.cache`. Package when: expiry, size limits or sharing across processes: `cachetools` or an external cache
- Concurrency: `concurrent.futures`; `asyncio.TaskGroup`, `asyncio.timeout` (3.11+)
- Tokens and IDs: `secrets`, `uuid`; never `random` for anything security-related
- Passwords, encryption: never write your own; use `argon2-cffi`, `bcrypt` or `cryptography`
- Test doubles: `tmp_path`, `monkeypatch`, `unittest.mock`. Package when: dev dependencies are cheap: `time-machine`, `responses`, `respx`

Quoting for a shell, JSON or CSV uses `shlex.quote`, `json.dumps` or `csv`, never hand-rolled escaping. Entries marked 3.11+ or 3.12+ follow `python-versions.md`.
