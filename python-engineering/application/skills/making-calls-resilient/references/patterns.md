# Resilience patterns

Standard library only; each block runs as written (checked 7 November 2026, Python 3.13). Time and randomness are injected so the tests never sleep.

## Contents

- Retry with full jitter and Retry-After
- A circuit breaker with an injected clock
- A bulkhead

## Retry with full jitter and Retry-After

```python
import random
import time
from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class Transient(Exception):
    """A failure worth retrying; retry_after is the server's hint in seconds."""

    retry_after: float | None = None


def retry_call[T](
    fn: Callable[[], T],
    *,
    attempts: int = 4,
    base: float = 0.2,
    cap: float = 10.0,
    sleep: Callable[[float], None] = time.sleep,
    rand: Callable[[], float] = random.random,
) -> T:
    for attempt in range(1, attempts + 1):
        try:
            return fn()
        except Transient as error:
            if attempt == attempts:
                raise
            full_jitter = rand() * min(cap, base * 2**attempt)  # random between 0 and the ceiling
            sleep(min(cap, error.retry_after) if error.retry_after is not None else full_jitter)
    raise AssertionError("unreachable")


calls, sleeps = [], []


def flaky() -> str:
    calls.append(1)
    if len(calls) < 3:
        raise Transient(retry_after=1.5 if len(calls) == 1 else None)
    return "ok"


assert retry_call(flaky, sleep=sleeps.append, rand=lambda: 0.5) == "ok"
assert sleeps == [1.5, 0.5 * 0.2 * 2**2]  # the server's hint, then half the second ceiling (0.4)

calls.clear()
try:
    retry_call(lambda: calls.append(1) or (_ for _ in ()).throw(Transient()), attempts=3, sleep=lambda s: None)
except Transient:
    assert len(calls) == 3  # bounded: three calls, then the error surfaces
```

## A circuit breaker with an injected clock

```python
import time
from collections.abc import Callable


class CircuitOpen(Exception):
    pass


class Breaker:
    """Closed until `threshold` consecutive failures; open for `cooldown` seconds; then one probe."""

    def __init__(self, threshold: int = 5, cooldown: float = 30.0, clock: Callable[[], float] = time.monotonic) -> None:
        self.threshold, self.cooldown, self.clock = threshold, cooldown, clock
        self.failures = 0
        self.opened_at: float | None = None

    def call[T](self, fn: Callable[[], T]) -> T:
        if self.opened_at is not None:
            if self.clock() - self.opened_at < self.cooldown:
                raise CircuitOpen  # fail fast: the dependency is not called
            self.opened_at = None  # half-open: let this call probe
        try:
            result = fn()
        except Exception:
            self.failures += 1
            if self.failures >= self.threshold:  # a failed probe reopens it at once
                self.opened_at = self.clock()
            raise
        self.failures = 0
        return result


now = [0.0]
breaker = Breaker(threshold=2, cooldown=30, clock=lambda: now[0])


def boom() -> None:
    raise OSError("down")


for _ in range(2):
    try:
        breaker.call(boom)
    except OSError:
        pass
try:
    breaker.call(lambda: "never called")
except CircuitOpen:
    pass
now[0] = 31.0  # cooldown over: one probe goes through
assert breaker.call(lambda: "recovered") == "recovered"
assert breaker.failures == 0 and breaker.opened_at is None
```

## A bulkhead

```python
import asyncio


async def main() -> int:
    slots = asyncio.Semaphore(2)  # at most two calls to this dependency at once
    running = peak = 0

    async def call() -> None:
        nonlocal running, peak
        async with slots:
            running += 1
            peak = max(peak, running)
            await asyncio.sleep(0.01)
            running -= 1

    await asyncio.gather(*(call() for _ in range(10)))
    return peak


assert asyncio.run(main()) == 2
```
