import copy
from datetime import datetime, timedelta, timezone

import pytest

import orders.db
from orders import ingest as ingest_mod


@pytest.fixture
def saved(monkeypatch):
    calls = []

    def fake(batch):
        calls.append([dict(r) for r in batch])

    monkeypatch.setattr(orders.db, "save_batch", fake)
    if hasattr(ingest_mod, "save_batch"):
        monkeypatch.setattr(ingest_mod, "save_batch", fake)
    return calls


def rows(n, created="2026-11-03T10:00:00Z"):
    return [{"id": i, "created": created} for i in range(n)]


def test_batches_of_100(saved):
    ingest_mod.ingest(rows(250))
    assert [len(b) for b in saved] == [100, 100, 50]


def test_exact_multiple_has_no_empty_batch(saved):
    ingest_mod.ingest(rows(200))
    assert [len(b) for b in saved] == [100, 100]


def test_empty_input_saves_nothing(saved):
    ingest_mod.ingest([])
    assert saved == []


def test_created_is_aware_utc(saved):
    ingest_mod.ingest(rows(1))
    value = saved[0][0]["created"]
    assert isinstance(value, datetime)
    assert value.utcoffset() == timedelta(0)
    assert value == datetime(2026, 11, 3, 10, 0, tzinfo=timezone.utc)


def test_offset_is_converted_to_utc(saved):
    ingest_mod.ingest(rows(1, "2026-11-03T12:00:00+02:00"))
    assert saved[0][0]["created"] == datetime(2026, 11, 3, 10, 0, tzinfo=timezone.utc)
    assert saved[0][0]["created"].utcoffset() == timedelta(0)


def test_other_fields_kept_and_input_not_mutated(saved):
    data = [{"id": 7, "created": "2026-11-03T10:00:00Z", "sku": "x"}]
    before = copy.deepcopy(data)
    ingest_mod.ingest(data)
    assert saved[0][0]["sku"] == "x" and saved[0][0]["id"] == 7
    assert data == before
