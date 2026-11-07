---
type: regex
target: "last_message"
pattern: "CancelledError[^\\n]{0,140}(swallow|pass|ignor|re-?raise|never (stop|exit)|loop)|swallow[^\\n]{0,80}cancel"
flags: i
weight: 1
---

Names: CancelledError swallowed
