# Source

- Upstream: https://github.com/wshobson/agents
- Path: `plugins/python-development/skills/python-resilience/`
- Commit: 4bde3168b43c0655c4d00ea2726e631719908a6d
- Licence: MIT, Copyright (c) 2024 Seth Hobson. The upstream `LICENSE` is kept next to this file and applies to the adapted material.
- Adapted: 7 November 2026.

## What changed

- The upstream body (195 lines) and details (186 lines) are condensed to about 12 rules and one examples file. The upstream shows a retry decorator, timeout decorator and fault-tolerance decorator stack; the rewrite keeps the ideas (layers, classification, backoff, breakers) and gives runnable standard-library versions with injected time and randomness, so the tests never sleep.
- Run on Python 3.13: the retry helper (the server's `Retry-After` first, then full jitter with a fixed random value, bounded at the attempt limit), the breaker (closed, open, fail fast, one probe after the cool-down, reset on success) and the semaphore bulkhead (peak concurrency 2). With tenacity 9.2.1, httpx 0.28.1 and requests 2.34.2 in a scratch environment (not dependencies of this repository): the default raises `RetryError`, `reraise=True` raises the original error, a non-matching exception is not retried, `wait_exponential_jitter(initial=...)` emits a DeprecationWarning, httpx's default timeout is 5 seconds, `requests` sessions default to `timeout=None`.
- From general practice and the cited services' documentation, not run: the status-code list, the retry-budget idea and `Retry-After` date parsing.
