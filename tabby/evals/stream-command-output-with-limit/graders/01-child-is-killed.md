---
type: regex
target:
  source: file
  path: "src/runner/stream.py"
pattern: "\\.(kill|terminate)\\(\\)"
weight: 3
---

The child process is killed or terminated on timeout
