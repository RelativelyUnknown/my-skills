---
type: llm
focus:
  source: file
  path: "docs/architecture.svg"
weight: 2
---

PASS if the diagram has at most nine labelled nodes and every node corresponds to something in this repository (the API, the worker, the Postgres database, the Redis queue, the external payment provider). FAIL if it has more than nine, or invents a component.
