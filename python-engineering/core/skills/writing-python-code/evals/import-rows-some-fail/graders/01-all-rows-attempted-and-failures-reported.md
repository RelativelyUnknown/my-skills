---
type: llm
focus:
  source: file
  path: "src/ledger/importer.py"
weight: 3
---

PASS if every row is attempted even after a failure, and the failures are reported together with enough to identify each failed row (an ExceptionGroup, a returned list of failures, or a result object). FAIL if the loop stops at the first error, if failures are only logged and discarded, or if the identity of the failed row is lost.
