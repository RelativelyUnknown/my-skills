# Code smells

A smell is a habit that looks fine and makes the next reader stop: the code runs, but it is wrong, noisy or misleading. Check each function before you finish it. Each line is the smell, then `→`, then the fix. Report or fix a smell only when you can name the input or situation where the code goes wrong; one outside your diff is out of scope. Library, testing, service and native smells have their own `smells.md` in their folder.

## Wrong results and lost data

- `except Exception: pass`, a default returned from `except`, `raise Exception(...)` → catch the named exception around the one line that can raise; re-raise with `raise ... from e`
- The same error logged and raised → log once, at the boundary, or raise; `logger.exception`, not `logger.error(str(e))`
- `payload.get("name", "")` for required data, `x = x or 30` (replaces `0`) → fail where it is missing: `payload["name"]`; `if x is None`
- `assert` as validation (`python -O` strips it) → `if ...: raise ValueError(...)`
- `return`, `break` or `continue` in `finally` discards the exception in flight → keep only cleanup there
- `zip(a, b)` over inputs that must match in length → `zip(..., strict=True)` (3.10+)
- Removing from a list while looping over it → build a new list, or loop over a copy
- `status is "ready"`, `n is 1000` → `==`; `is` for `None` only
- Mutating an argument the caller passed in → copy it, or return a new value
- A default that is a `DEFAULT_*` constant, a stand-in `None` that secretly means 30, a call (`now=datetime.now()` runs once, at import), or `[]` / `{}` → a literal: `timeout: float = 30`; for a mutable, `None` and create it inside

## Time, files, network, processes

- A network call with no timeout; an HTTP body or subprocess result used unchecked → `timeout=`, `raise_for_status()`, `subprocess.run(..., check=True)`
- `f = open(...)` closed by a later `f.close()` that an early return skips, or `open` without an encoding → `with open(path, encoding="utf-8")`; use any iterator while its file is open
- A generator, cursor or `csv.reader` returned from inside the `with` that owns its file → consume it inside, or return an object that closes the resource
- sqlite3 `with` (it commits but does not close) → close the connection explicitly
- `datetime.utcnow()` or a naive datetime → `datetime.now(UTC)`
- Work at import (environment or file reads, connections, `logging.basicConfig()`, background threads) → do it in a function the caller starts
- Retries that are unbounded, catch every exception, or repeat a write that may have succeeded → bound attempts, back off, retry only what is safe to repeat (idempotency: [application/smells.md](../application/smells.md))
- Secrets in logs, URLs or exception messages; string-built SQL or shell commands; `shell=True` with input; `random` for tokens → parameters, argument lists, `secrets`
- `functools.cache` or `lru_cache` on data that changes (rates, settings, remote state) → a bounded cache with an expiry that matches how fast the data changes

## Signatures

- A decorator without `functools.wraps` → add it, so hover and help keep the real signature
- `**kwargs` pass-through, parameters named `id`, `type` or `format`, a closed set of strings typed `str` → name every parameter; `Literal["a", "b"]`; past two or three parameters, keyword-only
- A flag that changes the return type, a tuple of three or more values, a bare `-> dict` → one return type; a dataclass or `NamedTuple`
- Network or disk I/O in a constructor or property → an explicit method
- `-1`, `""` or `0` standing for "no value", a bare `5` or `86400` in a condition → `X | None` or an exception; a named constant

## Structure

- A class with no state and one method; a one-line wrapper around an expression; a base class, factory or registry with one implementation; `utils.py` or `helpers.py` → a function; the expression; the concrete type; a module named for what it holds
- Booleans that must not all be true together, a `status` string compared in many places, or a nullable timestamp standing for a state → an `Enum`, one function that is the only writer, and the allowed transitions in one table; a database update guards the old state (`WHERE status = 'pending'`)
- Module-level mutable state; `dict[str, Any]` passed around → pass it in; a dataclass or `TypedDict`
- Names like `data`, `result`, `info`, `manager`, `new_`, `v2`; a number that carries meaning → say what the thing is; name the constant
- Defensive code for a case that cannot happen → delete it; search for an existing helper before writing one
- Control flow nested more than three levels (`if` in `for` in `try` in `if`) → guard clauses that return or raise early on the unhappy path, then the main logic flat; extract an inner block (a loop body, a branch of a state machine) into a named function
- A new variant added as a `mode` or `format` flag with branches through the old logic → its own class or function beside the old one, so the old one can be deleted later
- A base class or interface added only to share a constructor argument or remove one repeated line → leave the repetition; every abstraction couples its users, so abstract at three variants or when the work must be deferred or repeated
- A public mutable dataclass whose callers can set a field the rules constrain (a discount above 1) → frozen, or change it through a method that validates; `slots=True` so a stray attribute is an error
- `match` on a plain boolean, or an `if` chain with a dead fallback branch → the simplest expression that states the rule
- A subclass that overrides a method to raise `NotImplementedError` or do nothing, or reaches into parent attributes → composition: a small `Protocol`, the collaborator passed in
- A class that builds its own collaborators (client, store, clock) or branches on optional config → take them in the constructor and wire once at startup; tests pass fakes, and needing `mock.patch` on a private attribute means a dependency should be injected
- Abbreviated or single-letter names, a type in a name, a `Base` or `Abstract` prefix → full words; the general name on the parent and a specific one on the child; a name that is hard to find usually means the structure is wrong

## Comments and docs

- A comment explaining a compound condition → a named variable, or move the condition into a function whose name says it
- Narrating comments (`# Step 1`), commented-out code, a leftover `print`, `TODO` litter → delete
- Conversation residue ("as discussed", "now uses", "previously"), inflated claims ("robust", "production-ready"), a docstring that restates the signature → say what is not obvious, or nothing

Mechanical ones are cheapest in config: ruff `B`, `BLE`, `S`, `DTZ`, `A`, `FBT`, `ANN401`, `SIM115`, `PLW1514`, `RUF006`, `T20`, `TRY`.
