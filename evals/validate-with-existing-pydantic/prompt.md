---
tags: [development, dependencies]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Add a `Product` model with `name` (non-empty), `price` (greater than 0) and `tags` (at most 5 strings), and `load_products(raw)` that validates a list of dicts from an API and returns `Product`s. Put them in `src/catalog/products.py`. Add tests.
