---
type: llm
focus: last_message
weight: 1
---

PASS if the final message says which checks it ran, in the project's own way (poetry run, python -m unittest, black, flake8), or says it could not run them and why. FAIL if it reports checks that are not the project's (ruff, pytest, uv) as the verification.
