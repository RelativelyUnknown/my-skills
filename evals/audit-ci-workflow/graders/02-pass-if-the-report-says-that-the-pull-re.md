---
type: llm
focus: last_message
weight: 3
---

PASS if the report says that the pull request title is inserted into the shell script in `labeler.yml` through `${{ github.event.pull_request.title }}`, so a crafted title can run shell commands (script or expression injection). FAIL if this is not reported.
