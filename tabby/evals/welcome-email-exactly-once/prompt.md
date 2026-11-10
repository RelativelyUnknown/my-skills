---
tags: [development, workers, idempotency]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Add `send_welcome_email(user_id)` to `src/mail/tasks.py`: look up the user in the database from `src/mail/db.py`, send the email with `smtp.send`, and record `welcome_sent_at`. Our queue delivers every job at least once, so this function can be called twice for the same user, even at the same time from two workers. The user must get exactly one email. Add tests, including a duplicate delivery.
