# Property-based tests, mutation testing and release-grade gates

Read for `rigor=ultra`. Use the detected `runner` as the command prefix; examples use `uv`.

## Property-based tests (Hypothesis)

Use for round trips (`parse(format(x)) == x`), invariants (output is sorted, length preserved), parsers and many-parameter APIs. Do not use it for external integrations, and keep example-based tests for known edge cases.

```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_sorting_keeps_length_and_is_ordered(xs):
    result = sort_numbers(xs)
    assert len(result) == len(xs)
    assert all(a <= b for a, b in zip(result, result[1:]))
```

- Install as a dev dependency: `uv add --dev hypothesis`. Add `.hypothesis/` to `.gitignore`.
- Defaults: 100 examples, a 200 ms deadline per example. The built-in `ci` profile loads automatically when the `CI` environment variable is set (no deadline, derandomized).
- Local profile: in `conftest.py`, `settings.register_profile("dev", max_examples=50)` then `settings.load_profile("dev")`.
- When Hypothesis finds a failure, keep the shrunk input as an explicit `@example(...)` so it stays covered, then fix the code.
- Properties must be true statements about the spec. Do not restate the implementation inside the test.

## Mutation testing

Coverage shows which lines ran; mutation testing shows which behavior the tests would notice. Run it periodically (before a release, or weekly), not on every commit.

```bash
uv add --dev mutmut
# pyproject.toml
# [tool.mutmut]
# source_paths = ["src/"]
# pytest_add_cli_args_test_selection = ["tests/"]
uv run mutmut run
uv run mutmut browse        # surviving mutants; press r to retest after strengthening a test
```

- Add `mutants/` to `.gitignore`. mutmut needs `fork`, so on Windows run it in WSL.
- A surviving mutant means a missing or weak test. Strengthen the test. Never change the code to kill a mutant.
- Without a mutation tool, do the manual version for any new test: break the function on purpose, confirm the test fails, restore it.

## Lowest-supported dependencies

A library declares lower bounds; test that they are true. One CI job runs `uv run --resolution lowest-direct pytest`, which installs the lowest compatible version of each direct dependency and the latest of everything else. If it fails, either raise the lower bound in `pyproject.toml` or fix the code. (`uv sync` accepts the same `--resolution` flag.)

## Installed-wheel test

Source-tree tests can pass while the built package is broken (missing data files, wrong includes). Test the artifact:

```bash
uv build --wheel -o /tmp/dist
uv venv /tmp/wheel-env
uv pip install --python /tmp/wheel-env/bin/python /tmp/dist/*.whl pytest
/tmp/wheel-env/bin/python -m pytest tests --import-mode=importlib -p no:cacheprovider
```

With `layout=src` and no `pythonpath` setting, the tests import the installed wheel. If the project sets `pythonpath = ["src"]`, run this from a copy of `tests/` outside the repo.

## Coverage gate

Branch coverage with a floor that only ratchets up: `--cov=<pkg> --cov-branch --cov-fail-under=<current-floor>`. Raise the floor when coverage rises. Lower it only with a stated reason.
