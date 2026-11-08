---
tags: [writing-documentation, page-types]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

Document our package `tinyretry` in three files: `docs/tutorial.md` for someone who has never used it, `docs/howto-retry-only-some-errors.md` for someone who already uses it and wants to retry only on certain exceptions, and `docs/reference.md` for the API. `tinyretry` has one public name: the decorator `retry(times=3, backoff_seconds=0.5, on=(Exception,))`. It calls the wrapped function up to `times` times in total, sleeps `backoff_seconds` multiplied by the attempt number between attempts, retries only when the function raises one of the exceptions in `on`, and re-raises the last exception if every attempt fails. Install is `pip install tinyretry`, Python 3.11+.
