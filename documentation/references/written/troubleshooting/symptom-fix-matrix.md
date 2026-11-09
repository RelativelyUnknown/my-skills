# Symptom and fix matrix

For a reader who has an error in front of them. Key every row by the exact text they see, so they can search for it.

| Symptom (exact message) | Cause | Fix |
| --- | --- | --- |
| `LedgerTimeout: no response in 30s` | The API is slow | Raise `LEDGER_TIMEOUT` (default 30) |

- One row per distinct symptom. Quote the message verbatim in code font, including numbers that vary only if they matter.
- Cause in one clause, fix as an action with the exact setting or command. A long fix links to a how-to guide instead of growing the cell.
- Order rows by how often people hit them, or alphabetically for an error-code catalogue (code, meaning, fix).
- A decision that needs several questions is an FAQ tree: question, then the answer or the next question, one level per heading.
- Say what to do when none of the rows match: where to report it and what to include.
