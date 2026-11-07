---
type: llm
focus:
  source: file
  path: "src/app/main.py"
weight: 2
---

PASS if loading with several missing or invalid settings raises one error that names all of them (errors are collected, or pydantic's ValidationError is used). FAIL if the code stops at the first problem.
