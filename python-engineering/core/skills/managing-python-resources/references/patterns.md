# Resource patterns

Self-contained examples; each block runs as written.

## Contents

- A class-based manager with an idempotent close
- Hand the resources over only if acquisition succeeded
- Roll back on error and on cancellation
- Swallow one documented exception
- Stream with accumulation, an early-exit close and a first-chunk time

## A class-based manager with an idempotent close

```python
from types import TracebackType


class Connection:
    def __init__(self, dsn: str) -> None:
        self._dsn = dsn
        self.open = False

    def connect(self) -> None:
        self.open = True

    def close(self) -> None:
        self.open = False

    def __enter__(self) -> "Connection":
        self.connect()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.close()


with Connection("db://x") as conn:
    assert conn.open
assert not conn.open
```

## Hand the resources over only if acquisition succeeded

```python
from contextlib import ExitStack
from pathlib import Path


def open_all(paths: list[Path]) -> tuple[list, ExitStack]:
    with ExitStack() as stack:
        files = [stack.enter_context(path.open()) for path in paths]
        return files, stack.pop_all()


Path("a.txt").write_text("a")
Path("b.txt").write_text("b")
files, stack = open_all([Path("a.txt"), Path("b.txt")])
with stack:
    assert [f.read() for f in files] == ["a", "b"]
assert all(f.closed for f in files)
```

## Roll back on error and on cancellation

```python
import asyncio
from contextlib import asynccontextmanager


@asynccontextmanager
async def transaction(log: list[str]):
    log.append("begin")
    try:
        yield
    except BaseException:  # includes asyncio.CancelledError
        log.append("rollback")
        raise
    else:
        log.append("commit")


async def main() -> list[str]:
    log: list[str] = []

    async def work() -> None:
        async with transaction(log):
            await asyncio.sleep(10)

    task = asyncio.create_task(work())
    await asyncio.sleep(0.05)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass
    return log


assert asyncio.run(main()) == ["begin", "rollback"]
```

## Swallow one documented exception

```python
class Writer:
    def __init__(self, stream) -> None:
        self._stream = stream

    def __enter__(self) -> "Writer":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        self._stream.close()
        return exc_type is BrokenPipeError  # the client left: expected, not an error
```

## Stream with accumulation, an early-exit close and a first-chunk time

```python
import time
from collections.abc import Iterator


def stream(response, metrics: dict) -> Iterator[str]:
    """Yield chunks; the response closes even if the consumer stops early."""
    chunks: list[str] = []
    start = time.perf_counter()
    try:
        for chunk in response.iter_content():
            if "first_chunk_s" not in metrics:
                metrics["first_chunk_s"] = time.perf_counter() - start
            chunks.append(chunk)
            yield chunk
    finally:
        response.close()
        metrics["text"] = "".join(chunks)


class FakeResponse:
    closed = False

    def iter_content(self):
        yield from ("a", "b", "c")

    def close(self) -> None:
        self.closed = True


response, metrics = FakeResponse(), {}
gen = stream(response, metrics)
next(gen)
gen.close()  # the consumer stopped after one chunk
assert response.closed and metrics["text"] == "a"
```
