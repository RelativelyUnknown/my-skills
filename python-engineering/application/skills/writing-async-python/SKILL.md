---
name: writing-async-python
description: "Structured asyncio: TaskGroup versus gather, deadlines with asyncio.timeout, bounded fan-out with Semaphore and Queue, blocking calls via to_thread, async generators, debug mode, and testing coroutines. Use when writing or fixing asyncio code, adding concurrency, or when a coroutine hangs, leaks or blocks the event loop."
compatibility: "Needs the python-project-facts skill installed in the same folder."
argument-hint: "[python=3.12]"
license: MIT
metadata:
  adapted-from: "wshobson/agents async-python-patterns (MIT, Seth Hobson); see SOURCE.md"
---

# Writing async Python

Run `python3 <this skill's folder>/../python-project-facts/scripts/detect_project.py` once; `python.target` decides whether `TaskGroup` and `asyncio.timeout` (3.11+) are available and `async` names the project's test plugin. If the facts skill is not installed, tell the user once that project facts are assumed and use defaults. Behaviour below was run on Python 3.13.

## When async

- Async pays when many waits on I/O overlap and the libraries are async. CPU-bound work goes to a process pool; a few blocking calls inside an async app go through `asyncio.to_thread` (it copies the current `contextvars`). Match the project: do not add `anyio` or Trio to an asyncio project.
- One `asyncio.run(main())` at the program's entry point. It raises `RuntimeError` inside a running loop, so async code never calls it; sync code that must call async code runs it at the top, not in the middle.

## Rules

- Tasks that belong together run in `async with asyncio.TaskGroup() as tg:`. The first failure cancels the siblings and arrives as an `ExceptionGroup`, caught with `except*`. `asyncio.gather()` raises the first exception but leaves the other awaitables running; with `return_exceptions=True` it returns errors as values that you must check.
- A deadline is `async with asyncio.timeout(seconds):`. It cancels the body and raises `TimeoutError`. One deadline per request or job, set at the edge; inner calls take the time that remains.
- Let `CancelledError` propagate. Timeouts and `TaskGroup` rely on it. Clean up in `finally` or `async with`, then re-raise.
- Bound the fan-out. `asyncio.Semaphore(n)` around the call caps concurrency at `n`. For a stream of work, a `Queue(maxsize=n)` with `n` workers also applies backpressure: workers call `task_done()` in `finally`, the producer awaits `q.join()` after the last `put`, then cancels the workers. Never `gather` an unbounded list.
- An async generator that holds a resource needs `contextlib.aclosing(...)`, or a `break` leaves its `finally` waiting for garbage collection.
- Never block the loop: `time.sleep`, `requests`, a synchronous database driver, a large `json.loads`, a CPU loop. Find offenders with debug mode: `asyncio.run(main(), debug=True)`, `PYTHONASYNCIODEBUG=1` or `python -X dev` log `Executing <Task ...> took 0.25 seconds` for slow steps and warn `coroutine 'x' was never awaited` for a missing `await`.
- Keep a reference to every task you create, or put it in a `TaskGroup`; a task held only by the loop can be garbage collected before it finishes.
- `Lock`, `Queue` and `Event` belong to one loop and are not thread-safe. From another thread use `asyncio.run_coroutine_threadsafe(coro, loop)` or `loop.call_soon_threadsafe`.
- Tests: use the project's plugin (`pytest-asyncio` with `asyncio_mode = "auto"`, or `anyio`), or `unittest.IsolatedAsyncioTestCase`. Wrap the awaited call in `asyncio.timeout(...)` so a hang fails the test instead of freezing the run. Inject the sleep or clock instead of waiting in real time.

Shared HTTP clients, one database session per task and other service-level async rules are in `building-python-web-services` and `avoiding-code-snags`. Runnable examples: [references/patterns.md](references/patterns.md).
