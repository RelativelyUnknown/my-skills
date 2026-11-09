# Testing

Tests are the spec. They change only when the spec changes, and every test must be able to fail.

## Never-miss rules (every rigor level)

1. **Never edit, delete, skip or xfail an existing test to get green.** Never weaken an assertion (`is not None` for `== expected`, wider tolerance, looser regex). If a test contradicts the spec, the docstring or the task, stop treating it as yours to fix: leave it untouched, finish the rest of the work, and report the test, the line it contradicts and the change you propose.
2. **A bug fix starts red.** Write the test first, run it, confirm it fails for the right reason (quote the failure), then fix the code, then run the full suite. A test you never saw fail proves nothing.
3. Expected values come from the spec or a hand calculation, never from running the code and pasting its output.
4. Ask of each test: "If I broke the function, would this fail?" If not, it is not a test.
5. No `conftest.py`, plugin or setting that changes outcomes: no skip logic, no added xfail markers, no result rewriting, no `__eq__` override to satisfy an assertion. Shared fixtures in `conftest.py` are fine.
6. Flaky means find the cause. No sleeps, reruns or retry decorators until the cause is known. Do not look up expected outputs in git history or other branches.
7. Before reporting done, run the full suite (targeted runs are fine while iterating).

**Redesign exception.** Only when the task explicitly asks for a redesign, read [redesign.md](redesign.md) first; otherwise rule 1 holds.

## Writing tests (every `rigor` level)

- Put a new test where the project's tests already live and match their naming: existing `tests/test_orders.py` or a flat `tests/` means the new test goes there, not in a new subfolder. With no convention, mirror the package: `src/pkg/billing/invoice.py` pairs with `tests/billing/test_invoice.py`. With the `src` layout, test the importable (installed) package, not the source tree.
- One behavior per test; the name states it: `test_expired_token_raises_auth_error`.
- No `if`, `for` or `try` in a test. Use `pytest.mark.parametrize` with `ids`.
- Go through the public API. Cover empty input, `None`, boundaries, invalid input; check errors with `pytest.raises(Err, match="...")`.
- Do not test the language or libraries, and do not write tests for trivial getters to raise coverage.
- Assert on outputs and behavior, not on a mock having been called.
- Reproducing a failure: smallest input first; keep the failing input as a permanent parametrized case.

## Rigor levels (`rigor`, default `full`)

- `lite`: The rules above. Nothing else is required.
- `full`: Everything in "Full" below, and read [mocking.md](mocking.md) and [fixtures.md](fixtures.md).
- `ultra`: `full`, plus read [property-based.md](property-based.md), [mutation.md](mutation.md) and [gates.md](gates.md) and apply them. Their examples use `uv`; with another runner, use its equivalents.

## Full

- Mock only external boundaries: network, clock, randomness, third-party APIs. Never mock the unit under test. Prefer the real thing: `tmp_path` for files, `monkeypatch` for env and attributes, `caplog`/`capsys` for output, `time-machine` for time, `responses` (requests) or `respx` (httpx) for HTTP. Hand-built fakes for these are worse.
- Isolated and deterministic: no network (`pytest-socket`, `--disable-socket`), no sleeps (control time instead), `pytest-timeout`, `pytest-randomly` to expose order dependence. The suite must run with no secrets and no services.
- Strict config in `pyproject.toml`: `strict = true` (pytest 9+; earlier: `--strict-markers` and `xfail_strict = true`), `filterwarnings = ["error"]`. For a new project use `--import-mode=importlib`; if `test.import_mode` is already `prepend`, leave it and mention it.
- Docstring examples are doctests (`--doctest-modules`). The README's code block is executed by a test.
- Coverage is a floor, not a goal: `--cov=<pkg> --cov-branch --cov-fail-under=<N>`. Read the uncovered lines and branches; add a test only for behavior that matters.
- Async code: use the plugin already in `async` (`pytest-asyncio` or `anyio`); add none unprompted.

## Report

Say which tests you added, changed or removed (with the reason for each change or removal), the commands you ran with their results, and anything you noticed and left alone.
