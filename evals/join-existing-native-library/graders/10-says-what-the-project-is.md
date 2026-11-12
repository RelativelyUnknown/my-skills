---
type: llm
focus: last_message
weight: 3
---

PASS if the final message, or a file it says it wrote, correctly states what the repository is (a Python library with a Rust extension built with maturin, exposing a checksum function) and names the command that runs its checks (`make check`), both taken from the repository. FAIL if either is missing or wrong, or if the agent started changing source code instead.
