# Snags at boundaries: untrusted input, resources, retries, library code

Read when the code takes untrusted input, uses files, connections or subprocesses, retries, loops over parallel data, or is a library others import. Apply a line only when its condition holds.

## Untrusted input and secrets

- SQL built from data: bind values as parameters; allowlist any dynamic identifier.
- Shell command from input: pass an argument list with `shell=False`; validate the arguments.
- `pickle.loads` or `yaml.load` on external data: use JSON or `yaml.safe_load()`.
- `eval()` or `exec()` on input: parse the data format; `ast.literal_eval()` only when Python literals are meant.
- `verify=False` in production: keep TLS verification on; configure a trusted CA.
- `random` for tokens, a fast hash for passwords: use `secrets`; Argon2, bcrypt or scrypt.
- Credentials in logs, exception messages or URL query strings: redact them; keep them out of URLs.

## Control flow and resources

- `return`, `break` or `continue` in `finally` discards the exception in flight: keep only cleanup there.
- `zip(a, b)` over inputs that must match in length: `zip(..., strict=True)` (3.10+).
- Removing from a list while looping over it skips items: build a new list, or loop over a copy.
- An HTTP body or subprocess result used without checking its status: `raise_for_status()`, `check=True`.
- Retrying forever, retrying every exception, or repeating a write that may have succeeded: bound the attempts, back off with jitter, retry only what is safe to repeat (idempotency: `snags-async-and-services.md`).
- `f = open(...)` closed by a later `f.close()` that an early return or exception skips: use `with`.
- A generator, cursor or `csv.reader` returned from inside the `with` that owns its file: consume it inside, or return an object that closes the resource.
- `status is "ready"`, `n is 1000`: compare values with `==`.

## Library code

- Circular imports: break the cycle, move shared contracts to a lower module, or merge modules that are one responsibility.
- A keyword boolean that switches a function between very different behaviours: two functions, or a named mode type.
- Optional-dependency imports, root-logger configuration, private import paths and checkout-only packaging belong to the library bundle, if installed.

## Tests

- Mock external boundaries, not the logic under test; use `create_autospec` or `spec=` where interface drift would hide a break.
- Control time, randomness, ordering and shared state instead of rerunning a flaky test.
