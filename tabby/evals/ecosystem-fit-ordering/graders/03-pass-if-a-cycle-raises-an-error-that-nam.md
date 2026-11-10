---
type: llm
focus:
  source: file
  path: "src/runner/plan.py"
weight: 2
---

PASS if a cycle raises an error that names the tasks involved (for example by reading the nodes from graphlib.CycleError) rather than a bare or unhelpful message. FAIL otherwise.
