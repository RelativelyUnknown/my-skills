# Rigor: property-based, mutation, release gates, redesign

Read the section you need. `ultra` rigor reads all of it; `full` does not.

## Property-based tests (Hypothesis)

Use for round trips (`parse(format(x)) == x`), invariants (output sorted, length preserved), parsers and many-parameter APIs. Not for external integrations; keep example-based tests for known edge cases.

```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_sorting_keeps_length_and_is_ordered(xs):
    result = sort_numbers(xs)
    assert len(result) == len(xs)
    assert all(a <= b for a, b in zip(result, result[1:]))
```

- Dev dependency: `uv add --dev hypothesis`; `.hypothesis/` in `.gitignore`. The `ci` profile loads when `CI` is set; a local profile: `settings.register_profile("dev", max_examples=50)` in `conftest.py`.
- A failure found: keep the shrunk input as an explicit `@example(...)`, then fix the code. A property is a true statement about the spec, never a restatement of the implementation.
- Pick the strongest property the code supports: roundtrip or oracle over idempotence, over an invariant, over "does not crash". Idempotence is the one that finds canonicalisers that re-escape their own output (checked: `quote(s, safe=...)` without `%` in `safe` turns `a b` into `a%20b` and then `a%2520b`). A decoder test with `st.binary()` should accept only the documented error and let anything else fail; a pack/unpack pair that slices `data[6:6+n]` without a length check passes a roundtrip and silently returns a truncated body for short input (checked), so add that case by hand.
- A property that asserts nothing: restating the implementation (`add(a, b) == a + b`), or filters that discard nearly everything. Put constraints in the strategy (`st.integers(min_value=1)`, `st.builds`, `st.composite`), keep `assume()` for relations between values already drawn, and read the health-check warning (self-contradictory `assume`s raise `FailedHealthCheck`, checked). `f(x) == f(x)` is a real test only where `f` can vary: serialising a dict or set, hashing, the clock.
- Pin known edges with `@example` (empty, one element, duplicates, zero, negative, the maximum). Set `deadline=None` for anything slow, or a slow machine turns into a flaky suite that someone deletes.
- No property in sight is often an arrangement problem: pull the calculation out of the I/O (extract the pure core), add the missing inverse, build a value and then render it, return a new value instead of mutating, pass the limit in instead of reading a global. Do it only if the property you gain is stronger than "no crash".
- A shrunk counterexample is one of three things. Check what the code promises, in order of authority: the external spec, type hints, the docstring, the existing tests, and last the function's name. Violates a stated guarantee: code bug (quote the guarantee). Breaks a stated precondition: the strategy is too broad. Contradicts the docstring or types: the property is wrong. Never decided: ask, it is not a bug report. `a == b` with different hashes is a bug without any grounding, because the language requires them to agree.

## Mutation testing

Coverage shows which lines ran; mutation testing shows which behaviour the tests would notice. Run it before a release or weekly, not on every commit: `uv add --dev mutmut`, `[tool.mutmut]` with `source_paths = ["src/"]`, `uv run mutmut run`, `uv run mutmut browse`. `mutants/` in `.gitignore`; mutmut needs `fork` (WSL on Windows).

- A surviving mutant means a missing or weak test: strengthen the test. Never change the code to kill a mutant. It is not by itself a bug in the code; it is a pointer to where nothing checks, so read that code and reproduce a failure before calling anything a bug.
- Read survivors by what the code does, not by the operator: one in an authorisation check or a money calculation outweighs ten in a log line. A kill rate hides this, so list survivors; a high number is not adequacy.
- Call a survivor equivalent only after checking the types, reachability, whether the value is ever used, and trying to build an input that tells the two apart. `x > 0` and `x != 0` are the same for an unsigned value and different for a signed one; `>` against `>=` is equivalent only where the boundary value cannot occur, and "no test reaches it" does not show that. Removing a log line or an event is a test gap (low priority), not an equivalent.
- Without a tool, do it by hand for any new test: break the function on purpose, see the test fail, restore it.

## Release-grade gates

- **Lowest supported dependencies.** A library declares lower bounds; test them: one CI job runs `uv run --resolution lowest-direct pytest`. If it fails, raise the bound in `pyproject.toml` or fix the code.
- **Installed-wheel test.** Source-tree tests can pass while the built package is broken (missing data files, wrong includes): `uv build --wheel -o /tmp/dist`, install it into a fresh venv with pytest, run `pytest tests --import-mode=importlib -p no:cacheprovider`. With the `src` layout and no `pythonpath` setting, the tests import the installed wheel; if the project sets `pythonpath = ["src"]`, run from a copy of `tests/` outside the repo.
- **Coverage floor that only ratchets up:** `--cov=<pkg> --cov-branch --cov-fail-under=<current-floor>`. Raise it when coverage rises; lower it only with a stated reason.

## Redesign exception

Only when the task explicitly asks for a redesign: change the design first, run the tests, then classify each failure. It asserts the old internal shape: rewrite it. It asserts behaviour the spec requires: fix the code. It asserts something the spec never required: ask, or remove it and say why. No skips may remain; the end state is green.

## Determinism and fault injection

From TigerBeetle's simulator and fuzzers, and Ghostty's fuzz harnesses:

- Take every source of nondeterminism as a parameter: a clock, a `random.Random(seed)` (never the global one), file and network access behind small interfaces. One seed reproduces a run; print it on failure and give a one-command reproducer.
- Randomise the configuration and the fault rates per seed (swarm testing) instead of fixed knobs, and inject faults the code must survive: a failing write, a dropped message, a failed allocation at the native boundary.
- Check liveness as well as safety: after the faults stop, the system must converge.
- A fuzz crash becomes a named regression test. Compare a fast path against a plain reference path on the same corpus (a differential test).
- An exhaustive integrity check that is too slow for production runs in test and debug builds, and has its own tests that corrupt the data on purpose.
- Run a short fuzz pass in CI and a long one on a schedule, and keep a canary case that fails on purpose to prove the harness still fails.

