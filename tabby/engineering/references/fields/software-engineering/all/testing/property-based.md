# Property-based tests

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
