#!/usr/bin/env bash
# Builds the fixture project for the `diagram-of-a-small-service` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname README.md)"
cat > README.md <<'__FIXTURE_EOF__'
# billhook

Takes payment webhooks, stores them and settles invoices.

Run it locally with `docker compose up`.
__FIXTURE_EOF__
mkdir -p "$(dirname docker-compose.yml)"
cat > docker-compose.yml <<'__FIXTURE_EOF__'
services:
  api:
    build: .
    command: uvicorn billhook.api:app --host 0.0.0.0 --port 8000
    ports: ["8000:8000"]
    environment:
      DATABASE_URL: postgresql://billhook@db/billhook
      QUEUE_URL: redis://queue:6379/0
    depends_on: [db, queue]
  worker:
    build: .
    command: python -m billhook.worker
    environment:
      DATABASE_URL: postgresql://billhook@db/billhook
      QUEUE_URL: redis://queue:6379/0
      PAYMENTS_URL: https://api.paywise.example
    depends_on: [db, queue]
  db:
    image: postgres:17
  queue:
    image: redis:8
__FIXTURE_EOF__
mkdir -p "$(dirname src/billhook/__init__.py)"
cat > src/billhook/__init__.py <<'__FIXTURE_EOF__'

__FIXTURE_EOF__
mkdir -p "$(dirname src/billhook/api.py)"
cat > src/billhook/api.py <<'__FIXTURE_EOF__'
"""HTTP API: receives webhooks, stores them, enqueues a settle job."""
from fastapi import FastAPI

from billhook import jobs, store

app = FastAPI()


@app.post("/webhooks/payment")
def receive(payload: dict[str, object]) -> dict[str, str]:
    event_id = store.save_event(payload)
    jobs.enqueue("settle", event_id)
    return {"status": "accepted"}


@app.get("/invoices/{invoice_id}")
def invoice(invoice_id: int) -> dict[str, object]:
    return store.load_invoice(invoice_id)
__FIXTURE_EOF__
mkdir -p "$(dirname src/billhook/worker.py)"
cat > src/billhook/worker.py <<'__FIXTURE_EOF__'
"""Worker: takes settle jobs from the queue, asks the payment provider, updates the invoice."""
import os

import httpx

from billhook import jobs, store


def settle(event_id: int) -> None:
    event = store.load_event(event_id)
    response = httpx.get(f"{os.environ['PAYMENTS_URL']}/charges/{event['charge']}", timeout=10)
    response.raise_for_status()
    store.mark_invoice_paid(event["invoice"], response.json()["amount"])


if __name__ == "__main__":
    for event_id in jobs.consume("settle"):
        settle(event_id)
__FIXTURE_EOF__
mkdir -p "$(dirname src/billhook/store.py)"
cat > src/billhook/store.py <<'__FIXTURE_EOF__'
"""Postgres access (psycopg). Tables: events, invoices."""
__FIXTURE_EOF__
mkdir -p "$(dirname src/billhook/jobs.py)"
cat > src/billhook/jobs.py <<'__FIXTURE_EOF__'
"""Redis list used as the job queue: enqueue() pushes, consume() blocks and pops."""
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
