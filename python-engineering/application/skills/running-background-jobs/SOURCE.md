# Source

- Upstream: https://github.com/wshobson/agents
- Path: `plugins/python-development/skills/python-background-jobs/`
- Commit: 4bde3168b43c0655c4d00ea2726e631719908a6d
- Licence: MIT, Copyright (c) 2024 Seth Hobson. The upstream `LICENSE` is kept next to this file and applies to the adapted material.
- Adapted: 7 November 2026.

## What changed

- The upstream body (241 lines) and details (128 lines) are condensed to about 10 rules, a decision section and one runnable example. Celery-specific code listings, task chaining and chords, and the list of alternative queues are dropped; the rules are queue-neutral with the Celery option names that matter.
- Replaced with a runnable, standard-library job table (SQLite): atomic claim with `UPDATE ... RETURNING`, an idempotency key, leases that expire, retry with backoff and jitter, and a dead state. Run with four worker threads: each healthy job ran once, a flaky job succeeded on its third attempt, a broken job ended dead after three, and a lease that ran out was claimed again.
- Celery behaviour (acknowledge before running by default, `acks_late`, `reject_on_worker_lost`, `retry_backoff`, `retry_jitter`, `autoretry_for`, `max_retries`, `worker_prefetch_multiplier`, the one-hour Redis visibility timeout) comes from the Celery documentation (main branch, read 7 November 2026) and was not run here: Celery is not installed in the container.
- The Django `transaction.on_commit` note comes from the Django documentation and was not run.
