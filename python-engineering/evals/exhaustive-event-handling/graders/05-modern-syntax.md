---
type: regex
target:
  source: file
  path: "src/shop/events.py"
pattern: "Optional\\[|Union\\[|from typing import[^\\n]*\\b(List|Dict)\\b"
match: not_contains
weight: 1
---

No Optional, Union, List or Dict from typing
