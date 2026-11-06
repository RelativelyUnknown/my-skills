---
type: regex
target:
  source: file
  path: "src/reports/ingest.py"
pattern: "import \\*|==\\s*None|==\\s*True|timeout or 30|len\\(rows\\)\\s*==\\s*0|dict\\[str,\\s*Any\\]|logger\\.error[^\\n]*\\n\\s*raise|class ReportManager:\\s*\\n\\s*def __init__\\(self\\):\\s*\\n\\s*pass"
match: not_contains
weight: 2
---

Winces are gone: wildcard import, `== None`, `== True`, `timeout or 30`, `len(rows) == 0`, `dict[str, Any]`, log-and-raise, stateless manager
