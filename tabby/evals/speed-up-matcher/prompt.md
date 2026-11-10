---
tags: [development]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

This is way too slow on our 200k-row files. Make it faster.

```python
# matcher.py
def match(rows, blocked_ids):
    out = []
    for r in rows:
        if r['id'] not in blocked_ids:  # blocked_ids is a list of ~50k ids
            out.append(r)
    return out
```

There's a test in test_matcher.py that must keep passing.
