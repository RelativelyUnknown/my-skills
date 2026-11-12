# Hunting bugs

A bug hunt asks the code questions and runs the answers. Reading a function and finding it plausible is how reviews miss things. Built from the review skills listed in `THIRD_PARTY_NOTICES.md` and checked against running code where marked.

**Rules.**

- Start from what the project says must always be true (AGENTS.md, CLAUDE.md, `## Tabby`, ADRs, docstrings that state a rule, the tests that guard a past bug). A change that violates a stated invariant is a bug even when the code looks reasonable.
- Assume the change is broken and look for how. Distrust the comment, the commit message and the tests that say it is not: ask which assertions would still pass if the code were wrong, and whether a test was loosened to go green.
- Every finding is a failure scenario: an input or sequence, the bad outcome, and a `file:line`. "This could be cleaner" is not a finding.
- Run what you can as a throwaway test or one-liner in a scratch folder; never edit the code under review. A probe you did not run is a suspicion, and is labelled.
- Try to refute each candidate before you report it; the default is refuted. Say "traced" or "ran", not "probably" or "likely"; where you cannot tell, say so and what would settle it.

## Follow the calls (the assumption audit)

For each function under review write down what must be true on entry (the argument's trust level, state read, who the caller is, the clock), what it promises on every path, and what it calls. Then read each callee in full and follow every path through it, not only the one that succeeds. A name is not a check: `session_lookup` suggests the session is live while it compares only the ID. For each assumption say what makes it true; if nothing does, write **nothing enforces it**. Those are the best leads. Keep a list of open questions instead of guessing.

Shapes this finds in Python:

- A lookup that matches identity but ignores state (`get(id=...)` returns a soft-deleted, closed or expired row).
- A function that returns success without setting what it was meant to set, or sets an out-value on the happy path only.
- One of two callers runs outside the lock or transaction the callee assumes. Two handlers that read-modify-write the same row with no transaction are coupled even though neither calls the other.
- A helper whose name and result disagree: `check_restricted(user, perm)` returns `True` when the user *has* the permission; a `return True` on the fall-through path; `or` where `and` was meant; an inverted `if not`.
- `None == None`: `order.owner_id == current_user.id` is `True` when an anonymous user and a guest order both have no ID (checked).
- The same adjustment applied in two places for one event (a balance reduced when the exit is requested and again when it is processed).

## Probes

**Inputs.** Empty, one item, duplicates, a missing key, `None`, zero, negative, very large, `NaN`, whitespace only, very long, non-ASCII (combining marks, emoji), different case, a path with spaces or `..`. Dates: naive against aware, a DST change, 29 February, the 31st, month end, another offset.

**Boundaries.** Off by one at slice and range ends, inclusive against exclusive, `>` against `>=`, the last page of a paginated call, an empty last batch.

**State and order.** Called twice; called in another order; run again after a half-finished first run; the argument mutated by the callee; a mutable default; a module-level cache that outlives the test; an iterator consumed twice; a closure built in a loop.

**Status fields.** A status, a pair of booleans or a nullable timestamp that stands for a state: probe illegal combinations, repeated events and stuck states ([state-machines.md](state-machines.md)).

**Failure halfway.** The third of five calls raises: partial writes, a transaction too narrow or too wide, a resource not closed on the error path, a retry that repeats a side effect, an error swallowed into a default, a timeout that stops waiting but not the work, a secret cleared because of a transient failure.

**Contracts.** What do callers rely on that the change alters: the result on empty input (`None` or `[]`), ordering, the exception type, a default, sync against async, a removed name? Open the callers (`git grep`). Across a boundary: a signature changed on one side but not the other, a new route or command not registered, a missing permission, a migration without the matching code, docs that claim behaviour the code lacks.

**Concurrency.** Check then act; read-modify-write without a lock or transaction; two workers taking the same job; cancellation during an `await`; shutdown mid-job; a fork after threads started. Name the race window (microseconds or seconds), whether an attacker can widen it (a slow disk or network call, load, a symlink swapped between check and open), and whether a second thread or process can reach the data at all. Separate "impossible", "practically infeasible" and "feasible".

**Scale.** A query per item, quadratic work on caller-controlled input, an unbounded list, queue or cache, a whole file read into memory, a client created per request that should be shared.

**Unchecked results.** `subprocess.run` without `check=True`, an HTTP response whose status is never looked at, a function that returns an error value the caller ignores.

**Python traps.** Language behaviours that bite, each checked on 3.13: [python-traps.md](python-traps.md).

## Probing with properties and mutations

- Turn a hunch into a property and let a library look for the counter-example: a round trip (`decode(encode(x)) == x`), idempotence (`f(f(x)) == f(x)`), an invariant after every operation (totals match, no duplicates, sorted), or agreement with a slow obvious version. Hypothesis shrinks a failure to the smallest input. Keep the property as a test when it finds something.
- Check the tests would notice: break the line you suspect (flip a comparison, drop a branch) and run them. If they still pass, they do not cover it, and nothing "verified" rests on them.

## Native code (Rust, C, C++, Zig behind Python)

A panic or C++ exception crossing the boundary; `unwrap()` on caller data; integer overflow that wraps in release and panics in debug; `as` casts that truncate; touching a Python object without the GIL, or holding it through a long call; a missing or extra reference count; a buffer that outlives its owner. See [native-boundary.md](native-boundary.md).

## Report

Open with the most likely way this breaks in production, in one sentence, then the findings. For each: file and line, the input or situation, the command you ran and what it printed, the smallest fix. Suspicions you could not run come last, labelled. Close with what you could not verify and why. If the probes find nothing, say which you ran; do not invent findings.
