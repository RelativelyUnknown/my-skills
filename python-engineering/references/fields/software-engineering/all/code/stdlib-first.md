# Standard library first

Order: the project's own idiom, the standard library, a widely used package, then your own code. Read `pyproject.toml` first. A package for a few lines is as wrong as a regex parser for dates. Never regex-parse structured formats: dates, URLs, HTML, JSON, CSV, versions. Flag every new dependency in the report, with the reason.

1. **The project's own idiom first.** If its code already validates, parses, retries or serialises with a library, use that. Do not add a second mechanism or rewrite working code to switch. A project with pydantic models gets a pydantic model; a project without it does not get it for one function.
2. **Stay in the standard library while the job is small**: roughly under 15 lines, one or two call sites, none of the hard parts (security, time zones, text formats, network protocols).
3. **A package earns its place** when at least one holds:
   - the job is hard to get right and mistakes are subtle or costly (password hashing, tokens, HTML sanitising, time zones and recurrence, free-form dates, untrusted XML, HTTP with retries and pooling);
   - the same job repeats at three or more places;
   - it is the ecosystem standard readers expect (pytest, ruff, httpx for async HTTP);
   - it replaces more code than it adds, counting the tests a hand-rolled version needs.
4. **Weigh the cost.** A dev-only dependency costs users nothing; a runtime one does. A library's dependencies become its users', so keep the base install small and put heavy ones in extras; an application or single-file script may take more (PEP 723 `# /// script` declares a script's dependencies inline). Also count install size, import time, transitive packages, licence, maintenance health ([dependencies.md](../dependencies/dependencies.md)).
5. **Say so when you add one**, with the reason from step 3.

## Validation ladder

- One function, one to three arguments: `if not ...: raise ValueError(f"unknown region {region!r}; expected one of {sorted(REGIONS)}")`
- A few related records you construct: a frozen dataclass with `__post_init__` checks
- Untrusted nested JSON, many models, coercion, error lists, schema output: pydantic, or the project's validator
- Config file: `tomllib` and a dataclass. Command-line arguments: argparse `type=` and `choices=`

## Common jobs

- HTTP: `urllib.request` for one GET in a script, with `timeout=`. Package when: retries, pooling, async, HTTP/2: httpx or requests, with `raise_for_status()`
- HTTP retries: a loop with a cap, backoff and a named exception. Package when: several call sites or jitter: `tenacity`, `urllib3.util.Retry`, httpx `HTTPTransport(retries=...)`
- URLs: `urllib.parse` or the client's `params=`; never string concatenation
- Dates and times: `datetime.fromisoformat` (3.11+ parses `Z`), `strptime`, `zoneinfo`. Package when: free-form text or recurrence: `dateparser`, `python-dateutil`
- Paths and files: `pathlib`, `tempfile`, `shutil`. Subprocesses: `subprocess.run(..., check=True, timeout=...)`, `shlex`
- CLI: `argparse`. Package when: many subcommands, completion, or the project uses click or typer
- Data formats: `json`, `csv`, `html.parser`, `packaging.version`, `tomllib`. Package when: YAML, untrusted XML (`defusedxml`), scraping HTML (`beautifulsoup4`); never `line.split(",")`
- Collections: `Counter`, `defaultdict`, `itertools`, `itertools.batched` (3.12+; older: an `islice` loop)
- Caching: `functools.cache`. Package when: expiry, size limits, sharing across processes: `cachetools` or an external cache
- Concurrency: `concurrent.futures`; `asyncio.TaskGroup`, `asyncio.timeout` (3.11+)
- Tokens and IDs: `secrets`, `uuid`; never `random` for security. Passwords, encryption: never write your own; `argon2-cffi`, `bcrypt`, `cryptography`
- Test doubles: `tmp_path`, `monkeypatch`, `unittest.mock`. Package when: dev dependencies are cheap: `time-machine`, `responses`, `respx`

Quote for a shell, JSON or CSV with `shlex.quote`, `json.dumps`, `csv`; never hand-rolled escaping. Version-gated entries follow `python-versions.md`.
