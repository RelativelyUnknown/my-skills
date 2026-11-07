# Reliability, security, library and test snags

Read when the code handles untrusted input, files or connections, subprocesses, retries, async tasks, tests or package structure. Same severities as the main table. Flag a row only when its condition holds: a smell is evidence to investigate, not proof of a bug. Format: snag (severity): what it looks like → fix (lint rule, when one exists).

## Security at a trust boundary

Flag only when the input is untrusted or the secret is sensitive.

- SQL built from data (blocker): `execute(f"... {value} ...")` → Bind values as parameters; allowlist dynamic identifiers (S608)
- Shell command from input (blocker): `shell=True`, `os.system(...)`, a command string with user text → Argument list, `shell=False`, validated arguments (S602, S605)
- Unsafe deserialization (blocker): `pickle.loads(...)` or `yaml.load(...)` on external data → JSON, or `yaml.safe_load()` (S301, S506)
- Code execution on data (blocker): `eval()` or `exec()` on input → Parse the data format; `ast.literal_eval()` only when Python literals are meant (S307, S102)
- TLS verification off (blocker): `verify=False` in production → Keep it on; configure a trusted CA (S501)
- Weak secrets or password hashing (blocker): `random` for a token; a fast hash for passwords → `secrets`; Argon2, bcrypt or scrypt (S311, S324 (MD5 and SHA-1 only); review)
- Secret outside the source (blocker): Tokens in logs, exception messages or URL query strings → Redact; keep secrets out of URLs (secret scanner; review)

## Control flow and resources

- Exit from `finally` (blocker): `return`, `break` or `continue` in `finally` discards the exception in flight → Keep only cleanup in `finally` (B012)
- `zip()` truncates silently (blocker when lengths must match): `zip(names, emails)` → `zip(..., strict=True)` (3.10+), or check lengths (B905)
- Mutating while iterating (blocker when items can be skipped): `for x in items: items.remove(x)` → Build a new list, or iterate a copy
- Failure status ignored (blocker when success is assumed): HTTP body used without a status check; subprocess result treated as success → `raise_for_status()`; `check=True` or inspect the return code (PLW1510 for `subprocess.run`; review)
- Unbounded or unsafe retry (blocker): Retry forever, retry every exception, or repeat a write that may have succeeded → Bound attempts, back off with jitter, retry only when safe to repeat (idempotency: `snags-services.md`)
- Identity for value equality (wince; blocker if behaviour changes): `status is "ready"`, `n is 1000` → `==`; `is` only for `None` and singletons (F632)

A `with` block does not always close the object: `sqlite3`'s connection context manager commits or rolls back but leaves the connection open. Close it explicitly.

## Async

- Blocking work in `async def` (wince; blocker for a stalled service): Synchronous network or file I/O, or heavy CPU work, in a coroutine → An async API, or `asyncio.to_thread` / a process pool (ASYNC210, ASYNC251; asyncio debug mode)
- Cancellation swallowed (blocker when shutdown matters): `except asyncio.CancelledError: pass` and the loop goes on → Clean up, then re-raise
- `gather()` assumed fail-fast (wince): A comment or logic that expects siblings to be cancelled when one raises → With the default `return_exceptions=False` the first exception propagates and the other awaitables keep running; use `TaskGroup` for cancelling siblings

## Library structure

Library-specific; an application's internal layout matters less. Optional-dependency imports, root-logger configuration, wheel-versus-checkout failures and private import paths belong to `designing-package-apis` and `releasing-python-packages`: flag them in review and cite those skills.

- Circular imports (wince): Two modules need each other to import → Break the cycle, move shared contracts to a lower module, or merge modules that are one responsibility (`import-linter`; review)
- Constructor or property hides cost (wince): `Client()` connects over the network; a property does I/O or mutates state → Make it an explicit method, or document the cost and side effects
- Boolean mode flag (wince): A keyword flag switches a function between substantially different behaviours → Separate functions, or a named mode type (review (FBT covers positional booleans only))

## Tests

- Asserts implementation (wince): Only a mock call is checked; no result or effect → Assert the contract; mock external boundaries, not the logic under test
- Nondeterministic input (wince): Real clock, sleep, randomness, network or unspecified ordering decides the outcome → Inject or freeze time, seed randomness, control dependencies, specify ordering; rerunning diagnoses, it does not fix
- Leaks state (wince): Environment variables, caches, files or databases are not restored → Fixtures with teardown, `monkeypatch`, `tmp_path`
- Mock without a spec (nit): A bare `Mock` drifts from the real interface → `create_autospec` or `spec=` where drift would hide a break

## Do not flag

`zip()` without `strict` when the lengths may differ by design. Deserialization of data you produced yourself. A deliberate retry of an idempotent read. `asyncio.gather()` over a bounded set. A mock at a real external boundary.
