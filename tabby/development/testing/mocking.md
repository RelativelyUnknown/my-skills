# Mocking

## Mock or real?

A mock checks what you believe the dependency does; only the real thing checks what it does. Default to real, and fall back one step at a time, only when a reason below forces it:

1. **Real, in process:** your own code, `tmp_path` files, a pure library. Never mock code you own or the unit under test.
2. **Real, local:** the same database engine as production (a container or a local server; SQLite standing in for Postgres hides differences in types, locking and SQL), a local message broker, a cheap subprocess.
3. **A fake you maintain** (an in-memory repository, `respx` or `responses` at the transport): when the real service is outside your control, slow, paid, rate-limited or non-deterministic. A fake is only trusted while a **contract test** runs the same cases against the fake and the real service (a sandbox account, run on a schedule or before release) and both pass.
4. **A stub or `autospec` mock:** only to provoke what the real thing will not do on demand: a timeout, a 500, a full disk, a dropped connection, a partial write. Script it with `side_effect` (below).

Rules that follow:

- Every integration has at least one test against the real thing (marked `integration`, skipped without credentials but run in CI or before release). All-mock suites go green while production breaks.
- Mock at the outermost edge (the HTTP client, the clock), never in the middle of your own code. More than two patches in one test means the design needs the dependency passed in.
- Recorded responses (`vcrpy`) go stale: re-record on a schedule and fail the build when a cassette is older than the limit.
- A Python/native boundary is not a mock point: run the real extension in tests and compare it with the Python reference ([porting.md](../library/native/porting.md)); stub only the native import to test the fallback.
- A bug found in production that a mock hid gets a test against the real thing, not a better mock.

## Boundaries

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

## Retries and failure sequences

Script a dependency's failures with `side_effect` as a list: each call returns or raises the next item. Test the three outcomes that matter, and inject the sleep so the test is instant. Run as written under pytest (7 November 2026).

```python
from unittest.mock import Mock

import pytest

def fetch(client, *, attempts=3, sleep=lambda seconds: None):
    for attempt in range(1, attempts + 1):
        try:
            return client.request()
        except ConnectionError:
            if attempt == attempts:
                raise
            sleep(0.1 * attempt)

def test_succeeds_after_transient_errors():
    client = Mock()
    client.request.side_effect = [ConnectionError, ConnectionError, {"status": "ok"}]

    assert fetch(client) == {"status": "ok"}
    assert client.request.call_count == 3

def test_gives_up_after_the_last_attempt():
    client = Mock()
    client.request.side_effect = ConnectionError

    with pytest.raises(ConnectionError):
        fetch(client)
    assert client.request.call_count == 3

def test_does_not_retry_a_permanent_error():
    client = Mock()
    client.request.side_effect = ValueError("bad input")

    with pytest.raises(ValueError):
        fetch(client)
    assert client.request.call_count == 1
```

## Async

Use the async test plugin the project already has. With `pytest-asyncio`, set `asyncio_mode = "auto"` only if the project already does; otherwise mark tests with `@pytest.mark.asyncio`. Do not call `asyncio.run` inside a test body.
