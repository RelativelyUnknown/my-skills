---
tags: [python-engineering, native-extension]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

Add `checksum(data: bytes) -> int` to the Rust extension in `src/lib.rs` and export it from the `fastcsv` package. It runs a CPU-heavy rolling checksum over `data` (a multiply-and-add loop is fine), and other Python threads must keep running while it works. Add a test. You cannot build here, so be careful to write code that compiles against the PyO3 version in `Cargo.toml`.
