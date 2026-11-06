---
type: regex
target:
  source: file
  path: "src/shop/settings.py"
pattern: "_instance|__new__|metaclass|@singleton|class \\w*Singleton"
match: not_contains
weight: 2
---

No singleton machinery
