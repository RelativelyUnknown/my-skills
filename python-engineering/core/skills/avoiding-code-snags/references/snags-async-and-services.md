# Snags in async code, request handlers, caches and API contracts

Read when the code is async, serves requests, caches data, runs background work, or documents an API. Apply a line only when its consequence is real: a lost update, a response served to the wrong tenant, a dependency overwhelmed. "Async", "cached" and "thread-safe" are not guarantees by themselves.

## Async

- No blocking calls in `async def` (synchronous network or file I/O, heavy CPU): use an async API, or `asyncio.to_thread` / a process pool.
- Keep a reference to every task you create, or use `asyncio.TaskGroup`; a dropped `create_task(...)` loses its result and its exception.
- Do not swallow `asyncio.CancelledError`: clean up, then re-raise.
- `gather()` with the default `return_exceptions=False` propagates the first exception but leaves the other awaitables running; use `TaskGroup` when siblings should be cancelled.
- One HTTP client per application lifespan (`httpx.AsyncClient()`), not one per call.
- One database session per concurrent task; an `AsyncSession` is not shared across `gather()` tasks.
- Bound fan-out with pagination, batches, a semaphore or a queue; no `gather()` over everything a caller sent.

## Shared state across requests

- Check-then-act across an `await` (`if key not in cache: value = await load(); cache[key] = value`): another task can enter between the two. Make it atomic at the authoritative store, or coalesce per key. Add a lock only to protect a real invariant.
- An `asyncio.Lock` coordinates tasks in one loop, not threads or workers: enforce cross-worker invariants in the database.
- Do not hold a lock across a remote call; scope it to the resource.
- A retry that repeats a charge, order or email needs an idempotency key: claim it atomically, store and replay the outcome, bound the retries, back off with jitter, and retry at one layer only.
- Work the API calls "accepted" must survive a restart: use a durable queue or job table. An in-process task suits best-effort work only.
- One deadline per request: pass the remaining budget to each downstream call, measured with a monotonic clock.

## Caches

- The key holds every input the response varies by (tenant, permissions, locale, query). Take tenant and authorization from trusted server-side identity. Tags invalidate; they do not isolate.
- A per-process cache is per worker: use a shared cache or a version strategy if workers must agree, or state the bounded inconsistency.
- Hot-key expiry: coalesce refreshes (single flight) or refresh with jitter. In-process single flight does not coordinate workers.
- A slow reader can write an old value after a newer write: use versioned values or a bounded staleness policy. Invalidation is not atomic with the commit.
- On a cache outage, bound the fallback to the primary store and shed load.
- TTL is not a freshness policy: decide how stale is allowed, and set a hard maximum age with stale-while-revalidate or stale-on-error.
- Bound cache size and entry lifetime for per-user or high-cardinality keys.

## API contracts and docs

- Document retry behaviour for writes: key scope, retention, payload matching, in-flight handling and the replayed response, and implement it atomically.
- State pagination consistency: stable order, bounded page size, cursor reuse and concurrent-update behaviour.
- Keep one source of truth for the spec, validated against the running API.
- Document the sharing, ownership and cost of shared clients and sessions.
- Delete comments that claim "thread-safe", "atomic" or "invalidated everywhere" unless the code enforces it, and examples that teach another architecture.

Not smells by themselves: a lock (a too-broad one is), cache-aside (unless its staleness contradicts the contract), a best-effort in-process background task, a bounded `gather()`. Prefer making the database enforce an invariant over a distributed lock.
