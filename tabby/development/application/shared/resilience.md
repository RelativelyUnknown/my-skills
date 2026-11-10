# Resilience

Use the retry library the project already has (tenacity, backoff, a client's own retry setting); do not add one for a single call. Checked on Python 3.13 with tenacity 9.2.1, httpx 0.28.1 and requests 2.34.2 on 7 November 2026.

## Rules

- Layers, outside in: a deadline for the whole operation, a timeout on each call, bounded retries inside the deadline, a circuit breaker per dependency, a visible fallback. Retry at one layer only: three layers of three attempts make 27 calls.
- Every call has a timeout. `requests` has none by default (`timeout=None` waits forever); httpx defaults to 5 seconds per phase. Set it explicitly (`httpx.Timeout(10.0, connect=3.0)`) and bound the total with a deadline.
- Retry what can pass: connection errors, timeouts, 408, 429, 502, 503, 504. Never other 4xx or validation errors. A write is retried only with an idempotency key ([smells.md](../smells.md)).
- A call has three outcomes: it worked, it failed, or you do not know. A timeout is the third: the effect may have been applied. Record the intent before the call so an unknown outcome can be resolved later, and never treat a timeout on a write as a failure that is safe to repeat.
- Back off with full jitter: wait a random time between 0 and `min(cap, base * 2**attempt)`. Honour `Retry-After` (seconds or an HTTP date), capped. Three to five attempts; stop when the deadline would pass.
- tenacity: the default raises `RetryError` wrapping the last failure, so pass `reraise=True`; only exceptions named in `retry_if_exception_type` are retried; use `wait_exponential_jitter(multiplier=..., max=...)` (the `initial` argument is deprecated in 9.2.1); log with `before_sleep_log`. Its jitter is added to the delay, not full jitter.
- Under overload, retries add load. Stop retrying when a breaker is open, and cap retries as a share of traffic if many callers retry together.
- A circuit breaker per dependency: closed until N consecutive failures, open for a cool-down (calls fail fast with their own exception), then one probe; a failed probe reopens it. State is per process unless shared. Inject the clock.
- A bulkhead caps concurrent calls to one dependency (`asyncio.Semaphore`, a bounded thread pool) so one slow service cannot use every worker.
- A fallback degrades visibly: stale cache or a default, flagged in the response and counted in a metric. Never report a failed write as success.
- Log each retry at WARNING with the attempt and delay; count retries and breaker transitions ([observability.md](observability.md)).
- Tests inject `sleep`, `rand` and the clock, then assert attempt counts, delays and breaker states. A test that sleeps for real is a flaky test.


