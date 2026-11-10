---
type: llm
focus: last_message
weight: 4
---

PASS if the report says that `labeler.yml` runs on `pull_request_target`, checks out the pull request's own code (the head ref) and runs it (install and tests) while a secret or a privileged token is available, so a contributor from a fork can run their code with it. FAIL if this is missing or described only as a general best-practice note with no statement of what an attacker gains.
