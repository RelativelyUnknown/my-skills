# Source

- Upstream: https://github.com/wshobson/agents
- Path: `plugins/python-development/skills/async-python-patterns/`
- Commit: 4bde3168b43c0655c4d00ea2726e631719908a6d
- Licence: MIT, Copyright (c) 2024 Seth Hobson. The upstream `LICENSE` is kept next to this file and applies to the adapted material.
- Adapted: 7 November 2026.

## What changed

- The upstream body (295 lines) and details (440 lines) are condensed to about 12 rules and one examples file. The primer on the event loop, coroutines and futures, the web-scraping, database and WebSocket examples, and the connection-pool and batching tips are dropped (they restate library documentation or live in the web-services skill).
- Added after running each one on Python 3.13: a `TaskGroup` failure cancels siblings and surfaces as an `ExceptionGroup` caught with `except*`; plain `gather()` leaves the other awaitables running; `asyncio.timeout` cancels the body and raises `TimeoutError`; a `Semaphore` caps the peak at its limit; `Queue.join` with workers; `to_thread` copies `contextvars`; `aclosing` runs an async generator's `finally` on `break`; `asyncio.run` inside a running loop raises `RuntimeError`; the never-awaited warning; debug mode logging a slow step.
- From the asyncio documentation, not run: the weak-reference warning for tasks, the thread-safety of `Lock`/`Queue`/`Event` and the `run_coroutine_threadsafe` bridge, and the test-plugin options.
