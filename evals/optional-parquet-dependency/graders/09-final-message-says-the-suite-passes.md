---
type: llm
focus: last_message
weight: 1
---

PASS if the final message says the suite passes without pyarrow installed, or explains how the pyarrow-dependent test is skipped (`pytest.importorskip`) or isolated. FAIL if the suite is left red because pyarrow is missing.
