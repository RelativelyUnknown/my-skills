---
tags: [development, native-extension, porting]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

`rank_items` in `python/fastcsv/ranking.py` is about 70% of a run in our profile. Move it to Rust in `src/lib.rs` and keep `fastcsv.rank_items` working for callers. You can't build here, so be careful to write code that compiles against the PyO3 version in `Cargo.toml`.
