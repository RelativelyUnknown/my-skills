---
type: llm
focus: last_message
weight: 3
---

PASS if the final message reports that `schedule.view` caches a per-patient response under a key made only of the path and the week, so one patient's appointments are served to others. FAIL if it does not identify the missing patient in the cache key.
