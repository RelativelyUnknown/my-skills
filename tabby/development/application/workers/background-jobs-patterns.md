# Background job patterns

## A jobs table with an atomic claim, leases and backoff

Standard library only; the block runs as written (checked 9 November 2026). On PostgreSQL the claim is `SELECT ... FOR UPDATE SKIP LOCKED` inside one transaction. A job whose lease ran out is claimed again, which is the at-least-once guarantee: the handler must be idempotent.

```python
import random
import sqlite3
import tempfile
import threading
import time
from collections.abc import Callable
from pathlib import Path

MAX_ATTEMPTS = 3

SCHEMA = """
CREATE TABLE jobs (
    id INTEGER PRIMARY KEY,
    key TEXT UNIQUE NOT NULL,          -- idempotency key: one row per logical job
    payload TEXT NOT NULL,
    state TEXT NOT NULL DEFAULT 'pending',   -- pending, running, succeeded, dead
    attempts INTEGER NOT NULL DEFAULT 0,
    run_after REAL NOT NULL DEFAULT 0,
    lease_until REAL
)
"""

def connect(path: Path) -> sqlite3.Connection:
    db = sqlite3.connect(path, isolation_level=None, timeout=10)
    db.row_factory = sqlite3.Row
    return db

def enqueue(db: sqlite3.Connection, key: str, payload: str) -> None:
    db.execute("INSERT OR IGNORE INTO jobs (key, payload) VALUES (?, ?)", (key, payload))

def claim(db: sqlite3.Connection, now: float, lease: float = 30) -> sqlite3.Row | None:
    """Atomically take one due job. A job whose lease ran out is taken again (at-least-once)."""
    return db.execute(
        """
        UPDATE jobs SET state = 'running', attempts = attempts + 1, lease_until = ?
        WHERE id = (
            SELECT id FROM jobs
            WHERE (state = 'pending' AND run_after <= ?) OR (state = 'running' AND lease_until < ?)
            ORDER BY run_after, id LIMIT 1
        )
        RETURNING id, key, payload, attempts
        """,
        (now + lease, now, now),
    ).fetchone()

def finish(db: sqlite3.Connection, job: sqlite3.Row, now: float, error: Exception | None) -> None:
    if error is None:
        db.execute("UPDATE jobs SET state = 'succeeded' WHERE id = ?", (job["id"],))
    elif job["attempts"] >= MAX_ATTEMPTS:
        db.execute("UPDATE jobs SET state = 'dead' WHERE id = ?", (job["id"],))  # dead-letter: look at it by hand
    else:
        delay = min(60.0, 0.01 * 2 ** job["attempts"]) * random.uniform(0.5, 1.5)  # backoff with jitter
        db.execute("UPDATE jobs SET state = 'pending', run_after = ? WHERE id = ?", (now + delay, job["id"]))

def work(path: Path, handler: Callable[[str, str], None], stop: threading.Event) -> None:
    db = connect(path)
    while not stop.is_set():
        job = claim(db, time.time())
        if job is None:
            time.sleep(0.005)
            continue
        try:
            handler(job["key"], job["payload"])
        except Exception as error:  # noqa: BLE001 - any failure is a retry or a dead job
            finish(db, job, time.time(), error)
        else:
            finish(db, job, time.time(), None)

with tempfile.TemporaryDirectory() as tmp:
    db = connect(Path(tmp, "jobs.db"))
    db.execute(SCHEMA)
    enqueue(db, "crashy", "x")
    enqueue(db, "crashy", "again")  # same key: ignored
    assert db.execute("SELECT count(*) FROM jobs").fetchone()[0] == 1
    # A worker that dies keeps its lease until it runs out; then the job is taken again.
    first = claim(db, now=1000.0, lease=5)
    assert first is not None and first["attempts"] == 1
    assert claim(db, now=1002.0) is None  # lease still valid
    again = claim(db, now=1006.0)
    assert again is not None and again["attempts"] == 2
    for _ in range(MAX_ATTEMPTS):  # failures back off, then dead-letter
        job = claim(db, now=2000.0)
        if job:
            finish(db, job, 2000.0, RuntimeError("boom"))
    print("ok")
```

## Enqueue after commit

From the Django documentation (not run here): `transaction.on_commit(lambda: send_receipt.delay(order.pk))` runs the callback only after the surrounding transaction commits, and not at all if it rolls back. Without Django, write the job row in the same transaction as the data (an outbox table) and let a worker or relay pick it up.
