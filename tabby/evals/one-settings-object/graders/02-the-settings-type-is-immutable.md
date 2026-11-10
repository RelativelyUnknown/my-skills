---
type: regex
target:
  source: file
  path: "src/shop/settings.py"
pattern: "frozen\\s*=\\s*True|NamedTuple|MappingProxyType"
weight: 2
---

The settings type is immutable
