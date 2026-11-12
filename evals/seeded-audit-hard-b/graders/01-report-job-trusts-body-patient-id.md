---
type: llm
focus: last_message
weight: 3
---

PASS if the final message reports that the summary request copies `patient_id` from the request body into the queued job and the job builds that patient's appointments without checking it against the logged-in patient, so any logged-in user can obtain another patient's data. FAIL if it does not connect the request body, the queue message and the job.
