---
tags: [documentation, history, operations, troubleshooting]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

Our service `ledgerd` is a Python worker that posts invoices to a ledger API. Write three documents for it.

1. `docs/adr/0007-use-postgres-for-the-job-queue.md`: record our decision to keep jobs in a Postgres table (`jobs`, claimed with `SELECT ... FOR UPDATE SKIP LOCKED`) instead of Redis lists or Amazon SQS. Reasons: we already run Postgres, jobs must survive a restart, and one backup covers everything. Cost: polling adds up to one second of latency and the table needs a vacuum policy. We decided this on 2026-10-14 in the platform meeting.
2. `docs/runbooks/stuck-jobs.md`: how the on-call engineer clears jobs stuck in state `running`. Trigger: the alert "jobs running longer than 15 minutes". Check with `SELECT count(*) FROM jobs WHERE state = 'running' AND leased_until < now();`. Fix: `sudo systemctl restart ledgerd-worker`, then run the check again. If the count has not fallen to 0 within 10 minutes, page the payments team in #payments-oncall.
3. `docs/troubleshooting.md`: three errors people hit. `LedgerTimeout: no response in 30s` (the ledger API is slow; raise `LEDGER_TIMEOUT`, default 30). `IdempotencyConflict: key already used with a different payload` (a job was re-enqueued with edited data; use a new key or restore the original payload). `LeaseExpired: job 4121 lost its lease` (the worker took longer than `LEASE_SECONDS`, default 60; raise it or split the job).
