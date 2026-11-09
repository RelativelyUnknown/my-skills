---
tags: [writing-python-code, errors]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Add `import_rows(rows)` to `src/ledger/importer.py`: call `import_one(row)` from `src/ledger/store.py` for every row. Some rows are bad, and one bad row must not stop the rest from being imported. When the run is over, the caller must be able to see which rows failed and why. Add tests with a mixed batch.
