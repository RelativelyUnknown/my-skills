---
type: tool_order
before:
  tool: Bash
  input_match: "pytest"
after:
  tool: Edit
  input_match: "src/pricing"
weight: 1
---

pytest was run before the source was edited
