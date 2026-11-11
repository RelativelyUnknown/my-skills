---
type: llm
focus: trace
weight: 2
arm: with-only
---

PASS if, before finishing, the agent searched the whole repository for HTTP calls (for example grep for requests., httpx., urlopen) to check none was missed, and ran that search more than once or ended with it. FAIL if it only edited the files it already knew about.
