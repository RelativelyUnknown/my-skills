---
type: llm
focus: last_message
weight: 3
---

PASS if the final message either (a) describes a minimal project start the agent created and states the assumptions it made or the decision it needs from the user, or (b) asks between one and three questions, each with a suggested answer, without having built a project. FAIL if it asks more than three questions, or presents a long list of requirements for the user to answer before any work can start.
