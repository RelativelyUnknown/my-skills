# Mocking, fixtures and controlling time

## Mocking

A boundary is code you do not own or cannot run in a test: network, clock, randomness, third-party services, the process environment. Everything else runs for real.

- Patch the name where it is looked up, not where it is defined: `monkeypatch.setattr("pkg.client.httpx.get", fake)`.
- Keep mocks honest with `create_autospec(real_function)` or `mock.patch(..., autospec=True)`. A bare `Mock()` accepts any call, so the test passes when the signature changes.
- Assert on the result the unit produces. `fake.assert_called_once_with(...)` alone checks the implementation, not the behavior; use it only when the call is the behavior (for example, a notification that must be sent).
- Prefer a design that needs no patching: pass the dependency in (`def fetch(url, *, client)`), then pass a stub in the test.

```python
# HTTP: httpx -> respx, requests -> responses
def test_fetch_user_raises_on_server_error(respx_mock):
    respx_mock.get("https://api.example.com/users/1").respond(500)
    with pytest.raises(httpx.HTTPStatusError):
        fetch_user(1)
```

## Time, randomness, environment

- Clock: `time-machine` (`@time_machine.travel("2026-11-03 10:00 +0000", tick=False)`), or accept `now: datetime | None = None` in the function and pass a fixed value. Never `time.sleep` to wait for expiry.
- Randomness: accept a `random.Random` (or a seed) and pass `Random(0)`; do not patch `random.random`.
- Environment: `monkeypatch.setenv("TOKEN", "x")`, `monkeypatch.delenv("TOKEN", raising=False)`. Never read real credentials in a test.
- Files: `tmp_path` (a `Path`), never a fixed location.

## Fixtures

- Smallest scope that works: the default `function` scope. Widen to `module` or `session` only for something expensive and read-only.
- Shared fixtures live in the `conftest.py` nearest to their users. A fixture used by one file stays in that file.
- Yield for cleanup:

```python
@pytest.fixture
def db(tmp_path):
    conn = connect(tmp_path / "test.db")
    yield conn
    conn.close()
```

- Factory fixtures build variations without one fixture per case:

```python
@pytest.fixture
def make_user():
    def make(name="ada", *, admin=False):
        return User(name=name, admin=admin)
    return make
```

- No `autouse=True` fixture that changes behavior the test does not mention. Autouse is acceptable for isolation only (for example, clearing an environment variable).
- Parametrize inputs, not setup: if every case needs different setup, they are different tests.
- A fixture that returns a value the test never uses should be `@pytest.mark.usefixtures("name")`.

## Async

Use the plugin in the detected `async` fact. With `pytest-asyncio`, set `asyncio_mode = "auto"` only if the project already does; otherwise mark tests with `@pytest.mark.asyncio`. Do not call `asyncio.run` inside a test body.
