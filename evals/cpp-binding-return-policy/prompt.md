---
tags: [development, native-extension, cpp]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

Our nanobind extension crashes. `c = Grid(4).cell(1); del c` aborts the interpreter with `free(): invalid pointer`, and `Grid(4).cell(10)` returns a cell with a garbage value instead of raising. Fix `src/grid.cpp`. You cannot build here.
