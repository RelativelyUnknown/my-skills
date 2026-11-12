---
type: llm
focus: last_message
weight: 3
---

PASS if the final message reports that `files.download` checks the raw name for `..` but opens the Unicode-normalised (NFKC) name, so fullwidth dots or similar characters pass the check and become `..` (path traversal). FAIL if it only reports path traversal in general without the check-versus-use mismatch, or does not mention the normalisation.
