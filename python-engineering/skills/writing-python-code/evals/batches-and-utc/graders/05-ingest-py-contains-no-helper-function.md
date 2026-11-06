---
type: llm
focus:
  source: file
  path: "src/orders/ingest.py"
weight: 1
---

PASS if `ingest.py` contains no helper function that only wraps one expression (for example `def _to_utc(s): return datetime.fromisoformat(s)`) and no `utils.py` or `helpers.py` module was created. FAIL otherwise.
