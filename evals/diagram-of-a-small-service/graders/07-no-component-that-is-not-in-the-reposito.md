---
type: regex
target:
  source: file
  path: "docs/architecture.svg"
pattern: "kafka|rabbitmq|nginx|kubernetes|elasticsearch|mongodb|load ?balancer|\\bS3\\b|CDN|celery"
flags: i
match: not_contains
weight: 3
---

No component that is not in the repository
