def load(rows, store):
    saved = 0
    for row in rows:
        if not (row and row.get("id") and row.get("email")):
            continue
        store.save(row)
        saved += 1
    return saved
