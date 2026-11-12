from ledger.importer import import_rows


def test_good_rows_imported_and_failures_visible(monkeypatch):
    seen = []
    import ledger.store as store
    import ledger.importer as imp

    def fake(row):
        if row.get("amount") is None or row["amount"] < 0:
            raise ValueError(f"bad amount in row {row.get('id')}")
        seen.append(row["id"])

    monkeypatch.setattr(store, "import_one", fake)
    if hasattr(imp, "import_one"):
        monkeypatch.setattr(imp, "import_one", fake)
    rows = [{"id": 1, "amount": 5}, {"id": 2, "amount": -1}, {"id": 3, "amount": 7}, {"id": 4, "amount": None}]
    try:
        result = import_rows(rows)
    except Exception as e:
        result = e
    assert seen == [1, 3]
    text = repr(result)
    assert "bad amount in row 2" in text and "bad amount in row 4" in text


def test_all_good_reports_no_failures():
    result = import_rows([{"id": 1, "amount": 1}])
    assert "bad amount" not in repr(result)


def test_empty_batch():
    import_rows([])


def test_unexpected_error_type_does_not_stop_the_rest(monkeypatch):
    import ledger.store as store
    import ledger.importer as imp

    seen = []

    def fake(row):
        if row["id"] == 2:
            raise KeyError("x")
        seen.append(row["id"])

    monkeypatch.setattr(store, "import_one", fake)
    if hasattr(imp, "import_one"):
        monkeypatch.setattr(imp, "import_one", fake)
    try:
        import_rows([{"id": 1}, {"id": 2}, {"id": 3}])
    except Exception:
        pass
    assert seen == [1, 3]
