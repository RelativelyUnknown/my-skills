# Service, concurrency, cache and API-contract snags

Read when reviewing request handlers, shared state across `await`, caches, background work or API documentation. Flag a row when its consequence is real: a lost update, a response served to the wrong tenant, a dependency overwhelmed. "Async", "cached" and "thread-safe" are not guarantees by themselves.

## Request concurrency

| Snag | Looks like | Fix | Catch |
| --- | --- | --- | --- |
| Check-then-act across an `await` (blocker when exclusivity matters) | `if key not in cache: value = await load(); cache[key] = value` | Another task can enter between the check and the write. Make it atomic at the authoritative store, or coalesce work per key. Add a lock only to protect a real invariant | Test two overlapping requests for one key and count loads or writes |
| Process-local lock treated as service-wide (blocker when a global invariant depends on it) | An `asyncio.Lock` guards "one at a time" across several workers or threads | `asyncio` locks coordinate tasks in one loop, not threads or processes. Enforce the invariant in the database (transaction, constraint) | Run the test against several workers |
| One `AsyncSession` shared by concurrent tasks (blocker) | One SQLAlchemy session passed into `gather()` tasks | One session per concurrently running task | Test the concurrent path |
| Lock held across remote I/O (wince; blocker if it times out or deadlocks) | A global lock held while awaiting a database or HTTP call | Keep the critical section short; scope the lock to the resource | Load test unrelated keys |
| Unbounded fan-out (blocker under realistic traffic) | `gather()` over every item a caller sent | Bound input size and concurrency: pagination, batches, a semaphore, a bounded queue | Load test with large inputs |
| New HTTP client per call (wince) | `httpx.AsyncClient()` created in a hot path | One client per application lifespan, closed at shutdown | review |
| Retry repeats a side effect (blocker) | A timeout or `5xx` retries a charge, order or email with no deduplication | Define an idempotency key; claim it atomically; store and replay the outcome. Bound retries, back off with jitter, and do not retry at every layer | Send overlapping requests with one key; assert one side effect |
| "Accepted" work exists only in the process (blocker if it must not be lost) | An endpoint returns success after starting an in-memory task | A durable queue or job table, and an accepted-job response. In-process tasks only for best-effort work | Kill the worker after the response |
| Fresh timeout for every downstream call (wince; blocker if the caller's deadline is exceeded) | Three sequential calls each get the full timeout | Carry one deadline; pass the remaining budget; measure with a monotonic clock | Slow the dependencies; assert the whole request respects its budget |

## Caches

| Snag | Looks like | Fix | Catch |
| --- | --- | --- | --- |
| Key omits a dimension the response varies by (blocker; possible data leak) | Cached by URL or ID though it varies by tenant, permissions, locale or query | Put every legitimate input in the key. Take tenant and authorization from trusted server-side identity, not an untrusted header | Same URL across tenants and users |
| Invalidation tag mistaken for isolation (blocker) | Entries tagged by tenant but keyed only by resource ID | Tags are handles for invalidation; isolation belongs in the key | Two tenants with the same ID |
| Per-process cache treated as shared (blocker when freshness matters) | An in-memory dict invalidated on one worker while others keep their copies | State the cache's scope; use a shared cache or a version strategy, or document the bounded inconsistency | Read and invalidate across workers |
| Stampede on a hot key (blocker under load) | Many concurrent misses each query the origin | Coalesce refreshes (single flight); bounded stale-while-revalidate or jittered refresh. In-process single flight does not coordinate workers | Expire one hot key under load; count origin calls |
| Fill can overwrite a newer value (blocker when stale reads break the contract) | A slow reader writes an old value into the cache after a write and invalidation | Versioned values or keys, a reliable invalidation path, or a bounded staleness policy. Cache invalidation is not atomic with the commit | Force the interleaving in a test |
| Cache outage becomes unbounded origin load (blocker under failure) | Every cache timeout falls straight through to the primary store | Bound fallback concurrency; shed load; decide whether stale data is safer | Simulate the outage at peak traffic |
| TTL as the whole freshness policy (wince; blocker if stale data is unsafe) | A magic TTL with no invalidation or maximum age | Decide how stale is allowed; with stale-while-revalidate or stale-on-error, set a hard maximum age | Test expiry, failed refresh and write invalidation |
| Unbounded or high-cardinality cache (wince; blocker if memory can run out) | Per-user or arbitrary query keys in a process dict with no limit | Bound size and lifetime; skip low-reuse keys | Load test with diverse keys |

## API contracts and documentation

| Snag | Looks like | Fix | Catch |
| --- | --- | --- | --- |
| Duplicate-request behaviour undocumented (blocker for retryable writes) | A `POST` is documented without saying whether retries are safe or how keys work | Document the key's scope, retention, payload matching, in-flight behaviour and replayed response, and implement it atomically | Contract-test duplicate and in-flight cases |
| Pagination hides its consistency (wince; blocker for loss or duplication) | Offsets over changing data; opaque cursors with no stated rules | Bound page size, stable ordering, state cursor reuse and concurrent-update behaviour | Insert and delete rows between pages |
| Spec drifts from behaviour (wince; blocker if clients depend on it) | The published spec says one default, limit or error; the handler does another | One source of truth, validated against the running API in CI | Spec validation plus contract tests |
| Concurrency and ownership undocumented (wince; blocker if callers can corrupt state) | A shared client or session with no stated lifetime, sharing or owner | State what may be shared, who closes it and what it costs | Concurrent-use and shutdown tests |
| Comment claims a guarantee the code lacks (blocker if it misleads about safety) | "Thread-safe", "atomic" or "invalidated everywhere" over a process-local lock or best-effort invalidation | Delete the claim, or enforce it. Describe the real scope | Check against multi-task and multi-worker tests |
| Docs example teaches another architecture (wince) | Every example builds a client per call, omits the idempotency key or lists without a limit | Keep examples representative; run them in CI | Execute the snippets |

## Do not flag

A lock is not a smell; a too-broad or wrongly scoped lock is. Cache-aside is fine unless its staleness contradicts the API contract. An in-process background task is fine for small best-effort work, and a snag only when the API promises durable completion. Prefer making the database enforce an invariant over reaching for a distributed lock. `asyncio.gather()` is useful; the snag is unbounded fan-out or wrong assumptions about cancellation and shared state.
