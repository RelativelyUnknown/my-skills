---
tags: [writing-python-code, dependencies]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

`apply_coupon` in `src/shop/pricing.py` is called with user-supplied values. Add input validation: `price` must be a positive number and `percent` must be between 0 and 100. Raise clear errors. Add tests.
