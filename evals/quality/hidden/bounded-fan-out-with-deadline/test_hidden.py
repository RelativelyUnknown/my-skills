import asyncio
import functools

import pytest

from crawl.fetch import fetch_all


def sync(fn):
    @functools.wraps(fn)
    def wrapper():
        return asyncio.run(fn())

    return wrapper


@sync
async def test_results_keep_input_order():
    async def one(url):
        await asyncio.sleep(0.03 if url == "a" else 0.0)
        return url.upper()

    assert await fetch_all(["a", "b", "c"], one) == ["A", "B", "C"]


@sync
async def test_limit_is_respected():
    running = peak = 0

    async def one(url):
        nonlocal running, peak
        running += 1
        peak = max(peak, running)
        await asyncio.sleep(0.01)
        running -= 1
        return url

    await fetch_all([str(i) for i in range(30)], one, limit=4)
    assert peak <= 4 and peak >= 2


@sync
async def test_empty_urls():
    async def one(url):
        return url

    assert await fetch_all([], one) == []


@sync
async def test_timeout_raises_and_leaves_nothing_running():
    started = finished = cancelled = 0

    async def one(url):
        nonlocal started, finished, cancelled
        started += 1
        try:
            await asyncio.sleep(5)
            finished += 1
        except asyncio.CancelledError:
            cancelled += 1
            raise

    with pytest.raises(TimeoutError):
        await fetch_all(["a", "b", "c"], one, limit=2, timeout=0.1)
    await asyncio.sleep(0.05)
    assert finished == 0 and cancelled == started


@sync
async def test_exception_in_one_call_propagates():
    async def one(url):
        if url == "bad":
            raise ValueError("boom")
        await asyncio.sleep(0.01)
        return url

    with pytest.raises(Exception):
        await fetch_all(["a", "bad", "c"], one)
