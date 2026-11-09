# Control-flow snags

Apply a line only when its condition holds.

- `return`, `break` or `continue` in `finally` discards the exception in flight: keep only cleanup there.
- `zip(a, b)` over inputs that must match in length: `zip(..., strict=True)` (3.10+).
- Removing from a list while looping over it skips items: build a new list, or loop over a copy.
- An HTTP body or subprocess result used without checking its status: `raise_for_status()`, `check=True`.
- Retrying forever, retrying every exception, or repeating a write that may have succeeded: bound the attempts, back off with jitter, retry only what is safe to repeat (idempotency: `snags-async-and-services.md`).
- `f = open(...)` closed by a later `f.close()` that an early return or exception skips: use `with`.
- A generator, cursor or `csv.reader` returned from inside the `with` that owns its file: consume it inside, or return an object that closes the resource.
- `status is "ready"`, `n is 1000`: compare values with `==`.
