---
type: llm
focus: last_message
weight: 1
---

PASS if the report proposes a concrete fix for the title injection that passes the value through an environment variable (or otherwise keeps it out of the script text) and a concrete fix for the pull_request_target workflow (do not check out or run the head code there, or move the tests to a `pull_request` workflow without secrets). FAIL if either fix is missing.
