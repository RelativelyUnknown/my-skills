---
type: regex
target:
  source: file
  path: "src/payments/core.py"
pattern: "btc-[\\s\\S]*0\\.01|0\\.01[\\s\\S]*btc-"
weight: 1
---

Crypto is added: 1% fee and `btc-` reference
