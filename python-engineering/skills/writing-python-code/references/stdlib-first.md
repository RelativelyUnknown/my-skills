# Use what exists

Examples, not a boundary. If many Python developers have hit a problem, a standard solution exists; find it before writing your own. Entries marked 3.11+ or 3.12+ follow the table in `python-versions.md`.

| Job | Use | Not |
| --- | --- | --- |
| HTTP errors | `resp.raise_for_status()`; let `HTTPError` propagate | Manual status-code checks |
| HTTP retries | `urllib3.util.Retry` via `HTTPAdapter`, httpx `HTTPTransport(retries=...)` for connection errors, or `tenacity` | Hand-written backoff loops |
| URLs | `urllib.parse`, or the client's `params=` | String concatenation |
| Dates and times | `datetime.fromisoformat` (3.11+ parses `Z`), `strptime` for known formats, `dateutil.parser` for messy input, `zoneinfo` | Regex, naive datetimes, `utcnow()` |
| Paths and files | `pathlib`, `tempfile`, `shutil` | `os.path` string joins |
| Subprocesses | `subprocess.run(..., check=True)`, `shlex` | `os.system` |
| CLI | `argparse`, or click or typer if the project already uses them | Manual `sys.argv` parsing |
| Config and validation | pydantic, `dataclasses`, `tomllib` (3.11+) | Hand-written dict checks |
| Data formats | `json`, `csv`, `html.parser`, `packaging.version` | `line.split(",")` |
| Collections | `Counter`, `defaultdict`, `itertools`, `itertools.batched` (3.12+; older: an `islice` loop) | Manual counting and chunking |
| Caching | `functools.cache` | Hand-rolled memo dicts |
| Concurrency | `concurrent.futures`; `asyncio.TaskGroup`, `asyncio.timeout` (3.11+) | Manual thread bookkeeping |
| Tokens and IDs | `secrets`, `uuid` | `random` for anything security-related |
| Test doubles | `tmp_path`, `monkeypatch`, `time-machine`, `responses` or `respx` | Hand-built fakes for files, time or HTTP |

Quoting for a shell, JSON or CSV uses `shlex.quote`, `json.dumps` or `csv`, never hand-rolled escaping.
