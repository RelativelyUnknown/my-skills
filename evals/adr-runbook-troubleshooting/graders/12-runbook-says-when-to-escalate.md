---
type: regex
target:
  source: file
  path: "docs/runbooks/stuck-jobs.md"
pattern: "(10 minutes.*#payments-oncall|#payments-oncall.*10 minutes)"
flags: is
weight: 2
---

The runbook says when and whom to escalate to
