# Threads, processes and pools

Choose by what the work waits on, then keep the shared state small. `asyncio` has its own pages ([async.md](../application/shared/async.md), [async-patterns.md](../application/shared/async-patterns.md)).

| The work is | Use | Watch for |
| --- | --- | --- |
| Waiting on network or disk, a handful to a few hundred calls | `ThreadPoolExecutor`, or `asyncio` if the project already runs an event loop | A bounded pool (`max_workers`), a timeout on every call, results collected in order or by `as_completed` |
| CPU-bound Python | `ProcessPoolExecutor` | Arguments and results are pickled, so pass small things (a path, an id) and return small things; the entry point needs `if __name__ == "__main__":` because macOS and Windows spawn, not fork |
| CPU-bound in NumPy, pandas, a native extension | Often nothing: many of these release the GIL | Measure single-threaded first ([performance](../performance/index.md)) |
| A free-threaded build (3.13t, 3.14t) | Threads for CPU work | Every dependency must declare support; unsynchronised shared state that the GIL hid now races |

## Rules

- Do not share mutable state between workers if you can pass values in and collect values out. A shared `dict` or `list` mutated from threads needs a lock, or a `queue.Queue`; a counter needs `threading.Lock` (`n += 1` is not atomic).
- Always bound the work: a pool size, a queue `maxsize` (an unbounded queue is a memory leak with a delay), and a deadline. `future.result(timeout=...)` stops waiting, not the work; a thread cannot be killed, so design the task to check a `threading.Event` or to finish in bounded time.
- One failing task must not vanish. Call `future.result()` (or iterate `as_completed`) so the exception is raised; report which inputs failed instead of dropping them or aborting silently ([errors.md](errors.md)).
- Do not fork a process that already holds threads or open connections (database, HTTP clients, locks); create them after the fork, in each worker's initializer. Use `multiprocessing.get_context("spawn")` when unsure.
- Daemon threads are killed at exit mid-write; give a thread you started a way to stop and `join()` it. A `with` block on the executor waits for everything on exit.
- Test the concurrent code path: with the pool size at 1 for determinism, and at least once with several workers and a barrier or a deliberately slow task to expose ordering assumptions. Do not use `sleep` to order events.
- A queue with consumers and retries is a worker system, not a pool: see [background-jobs.md](../application/workers/background-jobs.md).
