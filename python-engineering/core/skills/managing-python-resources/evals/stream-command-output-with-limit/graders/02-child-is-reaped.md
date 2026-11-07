---
type: regex
target:
  source: file
  path: "src/runner/stream.py"
pattern: "with\\s+subprocess\\.Popen|with\\s+Popen|\\.wait\\(|\\.communicate\\("
flags: i
weight: 2
---

The child is reaped (context manager, wait or communicate)
