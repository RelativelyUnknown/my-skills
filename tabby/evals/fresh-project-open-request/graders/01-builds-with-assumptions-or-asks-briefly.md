---
type: llm
focus: trace
weight: 3
---

PASS if the agent either (a) created a minimal project start (a pyproject.toml and a package or module) and its final message states the assumptions it made, or (b) asked between one and three questions in its final message, each with a suggested answer, without creating a project. FAIL if it asked more than three questions, wrote a long list of requirements to be answered, or both built a large project and asked many questions.
