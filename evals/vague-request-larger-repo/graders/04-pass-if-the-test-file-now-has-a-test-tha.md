---
type: llm
focus:
  source: file
  path: "tests/test_csv_format.py"
weight: 2
---

PASS if the test file now has a test that exports a customer whose field contains a comma (for example a name like "Acme, Inc.") and checks that the row keeps five columns or that the field is quoted, and the original test `test_writes_header_and_rows` is still present with its expected string unchanged. FAIL otherwise.
