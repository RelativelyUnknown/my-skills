---
type: llm
focus: trace
weight: 3
---

PASS if the tests the agent added for `retry` use unittest (a `unittest.TestCase` class) as the existing tests do. FAIL if it wrote pytest-style functions, imported pytest, or added pytest to the project.
