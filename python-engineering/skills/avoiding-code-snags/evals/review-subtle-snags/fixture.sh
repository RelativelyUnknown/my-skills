#!/usr/bin/env bash
# Builds the fixture project for the `review-subtle-snags` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname src/svc/jobs.py)"
cat > src/svc/jobs.py <<'__FIXTURE_EOF__'
"""Background jobs for the billing service."""
import asyncio
import csv
import sqlite3
import subprocess

import httpx
import requests


def do(job_id): ...
async def _load(key): ...
async def refresh(i): ...
async def notify(job): ...
def q(i): ...


def stream_rows(path):
    with open(path, encoding="utf-8") as fh:
        return csv.reader(fh)


def load_config(path):
    f = open(path, encoding="utf-8")
    text = f.read()
    if not text.strip():
        return {}
    f.close()
    return text


def pair_up(names, emails):
    return list(zip(names, emails))


def drop_expired(jobs):
    for job in jobs:
        if job["expired"]:
            jobs.remove(job)
    return jobs


def run_cleanup(cmd):
    subprocess.run(cmd)


def fetch_balance(url):
    return requests.get(url, timeout=10).json()["balance"]


def is_ready(status):
    return status is "ready"


def parse(text):
    try:
        header, body = text.split("\n", 1)
        rows = [r.split(",") for r in body.splitlines()]
        total = sum(int(r[2]) for r in rows)
        return {"header": header, "total": total}
    except (ValueError, IndexError):
        return None


def process(job_id):
    try:
        return do(job_id)
    finally:
        return None


_profiles = {}
_reports = {}


async def get_profile(user_id):
    if user_id not in _profiles:
        _profiles[user_id] = await _load(user_id)
    return _profiles[user_id]


async def get_report(tenant, url):
    if url not in _reports:
        _reports[url] = await _load((tenant, url))
    return _reports[url]


async def refresh_all(ids):
    # If one refresh fails, the others are cancelled.
    return await asyncio.gather(*[refresh(i) for i in ids])


async def fire(job):
    asyncio.create_task(notify(job))


async def worker(queue):
    while True:
        try:
            await queue.get()
        except asyncio.CancelledError:
            pass


async def totals(session, ids):
    return await asyncio.gather(*(session.execute(q(i)) for i in ids))


async def fetch_json(url):
    async with httpx.AsyncClient() as client:
        r = await client.get(url, timeout=10)
        r.raise_for_status()
        return r.json()


_lock = asyncio.Lock()


async def charge_once(order):
    # Thread-safe and cluster-safe: only one worker can charge an order at a time.
    async with _lock:
        return await _load(order)


async def charge_with_retry(client, order):
    for _ in range(3):
        try:
            return await client.post("/charge", json=order, timeout=5)
        except httpx.TimeoutException:
            continue


def count_rows(db):
    conn = sqlite3.connect(db)
    try:
        with conn:
            return conn.execute("select count(*) from jobs").fetchone()[0]
    finally:
        conn.close()


def pair_checked(a, b):
    return list(zip(a, b, strict=True))


async def refresh_bounded(ids, limit=10):
    sem = asyncio.Semaphore(limit)

    async def one(i):
        async with sem:
            return await refresh(i)

    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(one(i)) for i in ids]
    return [t.result() for t in tasks]
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
