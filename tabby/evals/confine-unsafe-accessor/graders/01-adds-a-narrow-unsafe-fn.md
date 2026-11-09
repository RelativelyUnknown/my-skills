---
type: llm
focus: trace
weight: 3
---

PASS if the change adds a new unsafe fn (for example get_unchecked) that skips the bounds check, rather than making the existing safe get() unsafe or removing its check. FAIL if the safe get() stops checking bounds, or no unsafe fn is added at all.
