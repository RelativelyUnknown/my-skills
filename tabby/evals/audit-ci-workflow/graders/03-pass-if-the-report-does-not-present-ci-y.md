---
type: llm
focus: last_message
weight: 2
---

PASS if the report does NOT present `ci.yml` (the `pull_request` workflow with `contents: read`) as a vulnerability that exposes secrets or a write token to forks. A note that it is fine, a hardening suggestion such as pinning actions to commit SHAs, or not mentioning it all count as PASS. FAIL only if it claims fork code in `ci.yml` can reach secrets or write to the repository.
