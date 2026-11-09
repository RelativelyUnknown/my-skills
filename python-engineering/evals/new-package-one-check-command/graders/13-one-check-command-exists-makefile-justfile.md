---
type: regex
target: "files"
pattern: "(^|/)(Makefile|justfile|noxfile\\.py)$"
flags: m
weight: 2
---

One check command exists (Makefile, justfile or noxfile)
