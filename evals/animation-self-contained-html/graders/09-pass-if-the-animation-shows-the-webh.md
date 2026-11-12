---
type: llm
focus:
  source: file
  path: "docs/webhook-flow.html"
weight: 3
---

PASS if the animation shows the webhook entering the API, then being queued, then consumed by the worker, then written to Postgres, in that order, and a reader who sees only the finished picture (no script running) still sees every part and connection. FAIL otherwise.
