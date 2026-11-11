---
tags: [development, native-extension, baseline]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

Add `translate(p: Point, dx: float) -> Point` to the Rust extension in `src/lib.rs`: it returns a new `Point` moved by `dx` along x. Export it from the `fastcsv` package and declare it in the stub. You cannot build here, so write code that compiles against the PyO3 version in `Cargo.toml`.
