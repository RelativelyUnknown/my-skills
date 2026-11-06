---
name: writing-concurrent-python
description: "Chooses and writes Python concurrency: threads, processes or asyncio, with caps, timeouts, cancellation and per-item error handling. Use when making code concurrent, adding threads or asyncio, fixing a hang or a race, or adding timeouts to parallel work."
argument-hint: "[python=3.12]"
---

# Writing concurrent Python

Profile first (`profiling-python-code`); make code concurrent only when the time goes to waiting or to CPU work that can be split. Use features available at `python.target`.

## Choose

| Work | Use |
| --- | --- |
| Many waits on network or disk, blocking libraries | `ThreadPoolExecutor(max_workers=N)` |
| Many waits, async libraries or an async project | `asyncio` with `asyncio.TaskGroup` (3.11+) |
| One blocking call inside async code | `await asyncio.to_thread(fn, ...)` |
| CPU-bound work | `ProcessPoolExecutor`; the free-threaded build only if every dependency supports it |

## Rules

- **Cap it.** `max_workers=N` or an `asyncio.Semaphore(N)`; never one task per input with no limit.
- **Bound every wait.** `async with asyncio.timeout(s)`, `future.result(timeout=s)`, and `timeout=` on the call itself. A thread cannot be cancelled: after `result(timeout=s)` raises, the call keeps running, so put the timeout on the blocking call when the library allows it and say so when it does not.
- **No fire-and-forget.** Keep a reference to every task you create, or use a `TaskGroup`, which cancels siblings when one fails and leaves nothing running.
- **One failure must not lose the others.** Catch per item inside the worker (or `gather(..., return_exceptions=True)`), collect results and errors, and report the failures at the end.
- **Never block the event loop**: no `time.sleep`, `requests`, or synchronous database drivers in `async def`; use the async equivalent or `to_thread`.
- **Avoid shared mutable state.** Return values from workers; if state must be shared, guard it with a `Lock` or pass it through a `Queue`.
- **Let `CancelledError` propagate**; clean up in `finally`.
- Results arrive out of order. Return them in input order if the caller expects it.

## Report

Say which model you chose and why, the cap and timeout values, what happens to a failed item, and what you could not bound.
