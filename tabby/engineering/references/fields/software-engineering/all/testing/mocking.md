# Mocking

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

Use the plugin in the detected `async` fact. With `pytest-asyncio`, set `asyncio_mode = "auto"` only if the project already does; otherwise mark tests with `@pytest.mark.asyncio`. Do not call `asyncio.run` inside a test body.
