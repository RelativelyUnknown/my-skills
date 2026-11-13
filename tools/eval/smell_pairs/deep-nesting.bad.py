def load(rows, store):
    saved = 0
    for row in rows:
        if row:
            try:
                if row.get("id"):
                    if row.get("email"):
                        store.save(row)
                        saved += 1
            except KeyError:
                pass
    return saved
