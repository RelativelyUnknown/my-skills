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

## Mutation testing

Coverage shows which lines ran; mutation testing shows which behaviour the tests would notice. Run it before a release or weekly, not on every commit: `uv add --dev mutmut`, `[tool.mutmut]` with `source_paths = ["src/"]`, `uv run mutmut run`, `uv run mutmut browse`. `mutants/` in `.gitignore`; mutmut needs `fork` (WSL on Windows).

- A surviving mutant means a missing or weak test: strengthen the test. Never change the code to kill a mutant.
- Without a tool, do it by hand for any new test: break the function on purpose, see the test fail, restore it.

## Release-grade gates

- **Lowest supported dependencies.** A library declares lower bounds; test them: one CI job runs `uv run --resolution lowest-direct pytest`. If it fails, raise the bound in `pyproject.toml` or fix the code.
- **Installed-wheel test.** Source-tree tests can pass while the built package is broken (missing data files, wrong includes): `uv build --wheel -o /tmp/dist`, install it into a fresh venv with pytest, run `pytest tests --import-mode=importlib -p no:cacheprovider`. With the `src` layout and no `pythonpath` setting, the tests import the installed wheel; if the project sets `pythonpath = ["src"]`, run from a copy of `tests/` outside the repo.
- **Coverage floor that only ratchets up:** `--cov=<pkg> --cov-branch --cov-fail-under=<current-floor>`. Raise it when coverage rises; lower it only with a stated reason.

## Redesign exception

Only when the task explicitly asks for a redesign: change the design first, run the tests, then classify each failure. It asserts the old internal shape: rewrite it. It asserts behaviour the spec requires: fix the code. It asserts something the spec never required: ask, or remove it and say why. No skips may remain; the end state is green.
