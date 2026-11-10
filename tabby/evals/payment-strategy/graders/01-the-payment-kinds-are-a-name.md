---
type: llm
focus:
  source: file
  path: "src/payments/core.py"
weight: 2
---

PASS if adding a new payment kind now means adding one function (or one small entry) in one place: the kinds are dispatched through a mapping from name to callable, a `match` statement, or an equally direct lookup, and `process_payment` no longer grows an `if`/`elif` branch per kind. FAIL if the `if`/`elif` chain remains, or if each kind is a class in an inheritance hierarchy with a factory or registry object to pick one.
