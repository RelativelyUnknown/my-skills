---
type: regex
target:
  source: file
  path: "tests/test_core.py"
pattern: "def test_collapses_runs\\(\\):\\s*\\n\\s*assert slugify\\(\"A  B\"\\) == \"a--b\""
weight: 2
---

The existing contradicting test is untouched
