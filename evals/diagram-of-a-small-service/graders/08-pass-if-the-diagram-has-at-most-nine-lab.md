---
type: llm
focus:
  source: file
  path: "docs/architecture.svg"
weight: 2
---

PASS if the diagram has at most nine labelled nodes and every node corresponds to something in this repository: the API, the worker, the Postgres database, the Redis queue, the external payment provider, and at most a client or webhook sender. FAIL if it has more than nine nodes, or shows a component the repository does not contain.
