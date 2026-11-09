---
type: regex
target:
  source: file
  path: "tests/test_tasks.py"
pattern: "send_welcome_email\\([^)]*\\)[\\s\\S]*send_welcome_email\\("
flags: i
weight: 2
---

A test calls the task twice
