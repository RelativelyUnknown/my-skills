# Testing smells

Same format as [code/smells.md](../code/smells.md): the smell, `→`, the fix. The rules are in [testing.md](testing.md).

- A test that cannot fail (asserts a mock was called, `is not None`, `assert True`) → assert the result or the behaviour
- An expected value pasted from running the code → take it from the spec or a hand calculation
- An existing test edited, skipped or xfailed to get green, or an assertion loosened → fix the code; if the test contradicts the spec, leave it and report it
- A bug fix with no test seen failing first → write the test, run it, see it fail for the right reason, then fix
- `if`, `for` or `try` in a test body → `pytest.mark.parametrize` with `ids`
- `time.sleep`, the real clock, unseeded randomness, real network → control time, seed, mock only the external boundary
- State changed and not restored → `monkeypatch`, `tmp_path`
- A new test in a new folder when the project's tests live elsewhere → put it where the project's tests already live, with their naming
- The unit under test mocked → mock only network, clock, randomness and third-party APIs
- Tests of trivial getters, the language or a library, added to raise coverage → delete them
