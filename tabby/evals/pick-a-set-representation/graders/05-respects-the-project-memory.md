---
type: llm
focus: trace
weight: 2
---

PASS if the change respects the project memory in AGENTS.md: no new dependency was added to Cargo.toml (or it asked first), and it accounts for the stated growth (several hundred flags). FAIL if it adds a dependency without asking or ignores the growth.
