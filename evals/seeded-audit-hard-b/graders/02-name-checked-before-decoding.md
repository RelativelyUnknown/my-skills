---
type: llm
focus: last_message
weight: 3
---

PASS if the final message reports that `media.save_upload` rejects `..` and slashes in the raw name but percent-decodes (`unquote`) before building the path, so `%2e%2e%2f` passes the check and becomes `../` (path traversal on write). FAIL if it only reports traversal in general without the check-versus-decode mismatch.
