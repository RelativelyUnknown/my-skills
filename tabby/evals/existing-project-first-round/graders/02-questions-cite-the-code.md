---
type: llm
focus: last_message
weight: 3
---

PASS if each question is tied to something the agent found in the repository, named in the message (for example the Cargo.toml and src/lib.rs, the Makefile check target, the maturin build, a single exported function). FAIL if the questions are generic and mention nothing from this repo.
