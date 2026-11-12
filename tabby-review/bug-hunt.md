# Hunting bugs

A bug hunt asks the code questions and runs the answers. Reading a function and finding it plausible is how reviews miss things. For each unit under review (a function, endpoint, job or changed hunk): write down what it assumes, pick the probes below that apply, run each as a throwaway test or one-liner in a scratch folder (never edit the code under review), and report what you reproduced or can trace to a specific input. A probe you did not run is a suspicion; label it.

## Probes

**Inputs.** Empty, one item, duplicates, a missing key, `None`, zero, negative, very large, `NaN`, whitespace only, a very long string, non-ASCII (accents as combining marks, emoji), different case, a path with spaces or `..`. Dates: naive against aware, a DST change, 29 February, the 31st, month end, a different offset.

**Boundaries.** Off by one at slice and range ends, inclusive against exclusive, `>` against `>=`, the last page of a paginated call, an empty last batch.

**State and order.** Called twice; called in another order; run again after a half-finished first run; the argument mutated by the callee; a mutable default; a module-level cache that outlives the test; an iterator or generator consumed twice; a closure created in a loop that sees the last value.

**State machines.** A status, a pair of booleans or a nullable timestamp that stands for a state is a state machine nobody drew; probe its illegal combinations, repeated events and stuck states with [state-machines.md](state-machines.md).

**Failure halfway.** What if the third of five calls raises? Partial writes, a transaction that spans too little or too much, a resource not closed on the error path, a retry that repeats a side effect, an error swallowed into a default value, a timeout that stops waiting but not the work.

**Contracts.** What do callers rely on that this change alters: the return on empty input (`None` against `[]`), ordering, the exception type, a default, sync against async, a removed or renamed name? Open the callers (`git grep`), do not assume.

**Concurrency.** Check then act; read-modify-write without a lock or a transaction; two workers taking the same job; cancellation during an `await`; shutdown in the middle of a job; a fork after threads started.

**Scale.** A query per item, quadratic work on caller-controlled input, an unbounded list, queue or cache, a whole file read into memory.

## Python traps worth probing

- `is` against `==`; float equality; `round(2.5)` is 2 (banker's rounding); `//` and `%` with negatives; `Decimal` context precision.
- `os.environ` values are strings (`"0"` is truthy); `argparse` `type=bool` turns any non-empty string into `True`; JSON turns integer keys into strings and `float("nan")` into invalid JSON.
- `datetime.utcnow()` is naive; `sorted` with mixed types raises; `sort` is stable and `key=` is called once per item.
- A class with `__eq__` and no `__hash__` is unhashable; `lru_cache` on a method keeps `self` alive; `copy` is shallow.
- `asyncio.gather` without `return_exceptions=True` raises the first error and leaves the other tasks running; a blocking call inside `async def` stalls every task; a task with no reference can be garbage-collected.
- `subprocess.run` without `check=True` ignores failure; `open` without `encoding`; `requests` and `urllib` calls with no timeout; sqlite3 `with` commits but does not close.
- `except Exception` and a default return hide the real failure; `assert` is removed under `-O`.

## Native code (Rust, C, C++, Zig behind Python)

A panic or C++ exception crossing the boundary; `unwrap()` on caller data; integer overflow that wraps in release and panics in debug; `as` casts that truncate; touching a Python object without the GIL, or holding the GIL through a long call; a missing or extra reference count; a buffer that outlives its owner. See [native-boundary.md](native-boundary.md).

## Report

For each finding: file and line, the input or situation, the command you ran and what it printed, and the smallest fix. Suspicions you could not run come last, labelled. If the probes find nothing, say which probes you ran; do not invent findings.
