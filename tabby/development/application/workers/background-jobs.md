# Background jobs

Use the queue the project already has (Celery, RQ, Dramatiq, Arq, Taskiq, a cloud queue); do not add a second one, and do not add Celery for one job.

## Choose

- Work the user must not lose, that takes longer than a request, or that retries: a durable queue or a jobs table. Best-effort work that may vanish on a restart (a cache warm-up, a metrics ping): an in-process task (`BackgroundTasks`, `asyncio.create_task`).
- Low volume with a database already: a `jobs` table and a worker, claimed atomically (`UPDATE ... RETURNING`, or `SELECT ... FOR UPDATE SKIP LOCKED` on PostgreSQL). A runnable version is in [background-jobs-patterns.md](background-jobs-patterns.md).
- Time-based work: a scheduler that enqueues; the schedule is not the job.

## Rules

- Delivery is at least once, so a task must be safe to run twice. Give each logical job an idempotency key and make the effect an upsert, a check-then-skip, or a stored outcome. A queue that deduplicates by key narrows the window; it does not remove the need.
- Enqueue after the commit that makes the data visible, not inside the transaction: a fast worker can run before the row exists (`transaction.on_commit` in Django, or an outbox table written in the same transaction).
- Pass ids and small JSON values, not model instances or large payloads; the task reads current state when it runs.
- Retry only errors that can pass (timeouts, 5xx, deadlocks), with exponential backoff and jitter and a maximum number of attempts. A permanent error (bad input) fails at once. Jobs that run out of attempts go to a dead state that someone looks at, with the error kept.
- Set a time limit per task. A lease or visibility timeout must be longer than the longest run: with late acknowledgement, a task that outlives it is delivered to a second worker while the first still runs (Redis broker default: one hour).
- Celery acknowledges before running by default, so a started task never repeats and a worker crash loses it. `acks_late=True` repeats it after a crash, only safe for idempotent tasks; add `reject_on_worker_lost=True` so a killed child is redelivered. Retries: `autoretry_for=(...)`, `retry_backoff=True`, `retry_jitter=True`, `max_retries=n`. Long tasks: `worker_prefetch_multiplier = 1`. (Documentation, not run here.)
- A request that starts a job answers `202 Accepted` with a job id and a status URL. States: `pending`, `running`, `succeeded`, `failed` (and `dead` when attempts ran out). The status endpoint reports the state, the error summary and a link to the result.
- Log the job id, key and attempt on every line; watch queue depth, the age of the oldest job and the failure rate ([observability.md](../shared/observability.md)).
- Tests: call the task function directly for logic; run it eagerly (`task_always_eager` in Celery, a synchronous worker in RQ) for wiring; keep one test against the real broker for serialization and acknowledgement. Test the second delivery: run the task twice and assert one effect.
