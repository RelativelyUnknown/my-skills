# Async patterns

Each block runs as written on Python 3.12 or later (checked on 3.13, 7 November 2026).

## Structured concurrency and except*

```python
import asyncio

async def work(name: str, delay: float, log: list[str]) -> None:
    try:
        await asyncio.sleep(delay)
        log.append(f"{name} done")
    except asyncio.CancelledError:
        log.append(f"{name} cancelled")
        raise

async def fail() -> None:
    await asyncio.sleep(0.01)
    raise ValueError("boom")

async def main() -> list[str]:
    log: list[str] = []
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(work("slow", 1, log))
            tg.create_task(fail())
    except* ValueError as group:
        log.append(f"{len(group.exceptions)} ValueError")
    return log

assert asyncio.run(main()) == ["slow cancelled", "1 ValueError"]
```

## Bounded fan-out with a Semaphore

```python
import asyncio

async def main() -> int:
    running = peak = 0
    limit = asyncio.Semaphore(3)

    async def call(i: int) -> int:
        nonlocal running, peak
        async with limit:
            running += 1
            peak = max(peak, running)
            await asyncio.sleep(0.01)
            running -= 1
            return i

    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(call(i)) for i in range(20)]
    assert [t.result() for t in tasks] == list(range(20))
    return peak

assert asyncio.run(main()) == 3
```

## Producer and workers with a Queue

```python
import asyncio

async def main() -> list[int]:
    queue: asyncio.Queue[int] = asyncio.Queue(maxsize=2)  # put() waits when full
    results: list[int] = []

    async def worker() -> None:
        while True:
            item = await queue.get()
            try:
                results.append(item * 2)
            finally:
                queue.task_done()

    workers = [asyncio.create_task(worker()) for _ in range(2)]
    for i in range(6):
        await queue.put(i)
    await queue.join()  # every item has been processed
    for w in workers:
        w.cancel()
    await asyncio.gather(*workers, return_exceptions=True)
    return sorted(results)

assert asyncio.run(main()) == [0, 2, 4, 6, 8, 10]
```

## A deadline for a whole request

```python
import asyncio

async def step(seconds: float) -> None:
    await asyncio.sleep(seconds)

async def handle(budget: float) -> str:
    try:
        async with asyncio.timeout(budget):
            await step(0.02)
            await step(10)  # the remaining budget cancels this
    except TimeoutError:
        return "timed out"
    return "ok"

assert asyncio.run(handle(0.1)) == "timed out"
```

## Calling blocking code from async code

```python
import asyncio
import contextvars
import time

request_id = contextvars.ContextVar("request_id", default="-")

def slow_lookup() -> str:
    time.sleep(0.01)  # blocking: keep it off the event loop
    return request_id.get()

async def main() -> str:
    request_id.set("req-1")
    return await asyncio.to_thread(slow_lookup)  # the context is copied to the thread

assert asyncio.run(main()) == "req-1"
```

## Closing an async generator

```python
import asyncio
from contextlib import aclosing

closed = False

async def rows():
    global closed
    try:
        yield 1
        yield 2
    finally:
        closed = True  # the connection or file would be released here

async def main() -> None:
    async with aclosing(rows()) as it:
        async for row in it:
            break  # stop early; aclosing runs the finally block now

asyncio.run(main())
assert closed
```

## A test that cannot hang

```python
import asyncio

async def fetch() -> int:
    await asyncio.sleep(0.01)
    return 42

async def test_fetch() -> None:
    async with asyncio.timeout(1):  # a hang fails the test
        assert await fetch() == 42

asyncio.run(test_fetch())
```
